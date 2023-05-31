import requests
import base64
import threading
import time
import random
import asyncio

import os
# python3 protubuf error: expected bytes, bytearray found
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = "python"

from vland.api_pb2 import GetPlayerInfoCmd, GetSpecialAreaPlayerInfoCmd, ConnectSpaceReq, AddPlayerListenerCmd, Position, MovePosition
from vland.api_pb2 import RobotJoinInfo, RobotJoinCmd, RobotExitCmd, RobotMoveCmd
from vland.api_pb2 import Pids, PlayerPositionInfos, Error, GameTriggerSpecialAreaNotice
from vland.nanoclient import Nano
from vland.routedic import ApiRoute, ServerPush, RouteDic

class VlandAPI:
    areaList = None

    def __init__(self, wsconfig):
        self.wsconfig = wsconfig
        self.nano = Nano()
        self._init_nano()
        # 
        self.monitor_players(signal="01000100", callback=self.wsconfig["listener"])

    '''
    Get all the data of the space
    '''    
    def get_map_info(self):
        url = "https://us-api.vland.live"
        
        route = '/sdk/space/expand/' + self.wsconfig["spaceId"]
        headers = {
            "APIKEY": base64.b64encode(self.wsconfig["apiKey"].encode('utf-8')).decode('utf-8')
        }

        response = requests.get(url+route, headers=headers)
        data = response.json()
        return data["data"]

    '''
    Get the data of the specified user in the space
    '''    
    def get_player_info(self, pidArr, callback):
        data = GetPlayerInfoCmd()

        data.eventId = self.wsconfig["eventId"]
        data.spaceId = self.wsconfig["spaceId"]
        for i in pidArr: data.pidArr.append(i)
        buffer = data.SerializeToString()
        self.nano.request(ApiRoute.GET_PLAYER_INFO, buffer, lambda response: callback(self._player_infos_decoder(response)))   

    '''
    Create robots to the space according to user information
    '''
    def add_robot(self, playerInfo, callback=None):
        robot = RobotJoinInfo()
        
        robot.RobotId = playerInfo["pid"]
        robot.RobotName = playerInfo["name"]
        robot.Avatar = self._get_avatar(playerInfo["avatar"])
        robot.X = playerInfo["birth"][0]
        robot.Y = playerInfo["birth"][1]

        data = RobotJoinCmd()
        data.EventId = self.wsconfig["eventId"]
        data.SpaceId = self.wsconfig["spaceId"]
        data.joinInfoArr.append(robot)

        buffer = data.SerializeToString()
        if callback:
            self.nano.request(ApiRoute.ROBOT_JOIN, buffer, lambda response: callback(self._error_decoder(response)))  
        else:
            self.nano.request(ApiRoute.ROBOT_JOIN, buffer)  

    '''
    Clear all robots in the space
    '''
    def clear_robot(self, callback=None):
        data = RobotExitCmd()
        data.EventId = self.wsconfig["eventId"]
        data.SpaceId = self.wsconfig["spaceId"]

        buffer = data.SerializeToString()
        if callback:
            self.nano.request(ApiRoute.ROBOT_EXIT, buffer, lambda response: callback(self._error_decoder(response)))  
        else:
            self.nano.request(ApiRoute.ROBOT_EXIT, buffer)  

    '''
    Monitor the information of everyone in the space
    PlayerJoinSignal      = 00000001
    PlayerLeaveSignal     = 00000010
    PlayerMoveSignal      = 00000100
    PlayerTransferSignal  = 00001000
    PlayerAnimationSignal = 00010000
    PlayerSendMsgSignal   = 00100000
    PlayerGameSignal      = 01000000
    RobotViewSignal       = 10000000
    '''
    def monitor_players(self, signal, callback):
        data = ConnectSpaceReq()
        data.EventId = self.wsconfig["eventId"]
        data.SpaceId = self.wsconfig["spaceId"]
        data.Pid = self.wsconfig["apiId"] + "X"
        buffer = data.SerializeToString()
        self.nano.request(ApiRoute.CONNECT_SPACE, buffer)  

        data2 = AddPlayerListenerCmd()
        data2.eventId = self.wsconfig["eventId"]
        data2.spaceId = self.wsconfig["spaceId"]
        data2.listenerId = self.wsconfig["apiId"] + "X"
        data2.signal = int(signal, 2)
        # for i in pidArr: data2.pidArr.append(i)
        buffer2 = data2.SerializeToString()

        self.nano.request(ApiRoute.ADD_PLAYER_LISTENER, buffer2)  

        if ((int(signal, 2) & 1) == 1):
            self.nano.on(ServerPush.NewPosition, lambda data: self._on_join_handler(data, callback))
        if ((int(signal, 2) & 2) == 2):
            self.nano.on(ServerPush.Exit, lambda data: self._on_exit_handler(data, callback))
        if ((int(signal, 2) & 4) == 4):
            try:
                self.nano.on(ServerPush.OnMove, lambda data: self._on_move_handler(data, callback))
            except Exception as e:
                print("3. ", e)
        if ((int(signal, 2) & 8) == 8):
            self.nano.on(ServerPush.OnMove, lambda data: self._on_move_handler(data, callback))
        if ((int(signal, 2) & 16) == 16):
            self.nano.on(ServerPush.Animation, lambda data: self._on_common_handler(data, callback))
        if ((int(signal, 2) & 32) == 32):
            self.nano.on(ServerPush.SendNearMessage, lambda data: self._on_common_handler(data, callback))
            self.nano.on(ServerPush.SendGlobalMessage, lambda data: self._on_common_handler(data, callback))
            self.nano.on(ServerPush.SendEventMessage, lambda data: self._on_common_handler(data, callback))
            self.nano.on(ServerPush.SendPrivateMessage, lambda data: self._on_common_handler(data, callback))

        if ((int(signal, 2) & 64) == 64):
            self.nano.on(ServerPush.PrepareGameRoute, lambda data: self._on_common_handler(data, callback))
            self.nano.on(ServerPush.FinishGameRoute, lambda data: self._on_common_handler(data, callback))
            self.nano.on(ServerPush.GameTriggerSpecialAreaRoute, lambda data: self._on_trigger_area_handler(data, callback))
            self.nano.on(ServerPush.GameTriggerInteractiveRoute, lambda data: self._on_common_handler(data,callback))

        if ((int(signal, 2) & 128) == 128):
            self.nano.on(ServerPush.OpenVideo, lambda data: self._on_robot_view_enter_handler(data, callback))
            self.nano.on(ServerPush.CloseVideo, lambda data: self._on_robot_view_leave_handler(data, callback))

        # self.nano.on(ServerPush.SpaceClose, lambda data: self._on_space_close(data, callback))

    '''
    Get the list of regions that exist in the scene
    '''
    def get_space_areas(self):
        mapData = self.get_map_info()
        areas = mapData["specialAreas"]
        names = []
        datas = {}
        areaList = {}
        for area in areas:
            names.append(area["name"])
            datas[area["name"]] = area
            
        areaList["names"] = names
        areaList["datas"] = datas
        areaList["width"] = mapData["width"]
        areaList["height"] = mapData["high"]
        self.areaList = areaList
        return areaList
    
    '''
    Born in a specified location based on user information
    '''
    def born_in_space(self, playerInfo, area = None, callback=None):
        if not self.areaList:
            self.get_space_areas()
        if not area or area not in self.areaList["names"]:
            area = random.choice(self.areaList["names"])
        coordinates = self.calculated_position(area)

        playerInfo["birth"] = coordinates
        self.add_robot(playerInfo, callback)

    '''
    Get random coordinates in the specified area
    '''
    def calculated_position(self, name):
        if not self.areaList:
            self.get_space_areas()
        if name not in self.areaList["names"]:
            name = random.choice(self.areaList["names"])

        locationNum = random.choice(self.areaList["datas"][name]["locations"])
        coordinates = [locationNum % self.areaList["width"], locationNum // self.areaList["width"]]
        return coordinates

    '''
    Control the robot to move or talk
    '''
    def operate_robot(self, pid, area, message="", callback=None):
        coordinates = self.calculated_position(area)
        data = RobotMoveCmd()
        data.EventId = self.wsconfig["eventId"]
        data.SpaceId = self.wsconfig["spaceId"]
        data.RobotId = pid
        data.X = coordinates[0]
        data.Y = coordinates[1]
        data.ChatMessage = message

        buffer = data.SerializeToString()
        if callback:
            self.nano.request(ApiRoute.ROBOT_MOVE, buffer, lambda response: callback(self._error_decoder(response)))  
        else:
            self.nano.request(ApiRoute.ROBOT_MOVE, buffer)  
    
    '''
    Get all users in the specified area
    '''
    async def get_all_in_area(self, area, callback=None):
        if not self.areaList:
            self.get_space_areas()
        if not area or area not in self.areaList["names"]:
            area = random.choice(self.areaList["names"])

        index = int(self.areaList["datas"][area]["index"])
        data = GetSpecialAreaPlayerInfoCmd()
        data.eventId = self.wsconfig["eventId"]
        data.spaceId = self.wsconfig["spaceId"]
        data.index = index

        buffer = data.SerializeToString()

        future = asyncio.Future()
        def _pids_decoder(data):
            result = {}
            response = Pids()
            response.ParseFromString(data)
            result["name"] = area
            result["data"] = []
            for pid in response.Pid:
                result["data"].append(pid)
            future.set_result(result)

        self.nano.request(ApiRoute.GET_SPECIAL_AREA_INFO, buffer, _pids_decoder)  
        while not future.done():  # 等待future完成
            await asyncio.sleep(0.5)

        return await future

    '''
    Initialize nano websocket
    '''
    def _init_nano(self):
        host = "wss://us-game.vland.live"
    
        params = {
            "host": host,
            "path": "?apiId={wsconfig.apiId}&eventId={wsconfig.eventId}&key={wsconfig.apiKey}",
            "dict": RouteDic
        }
        self.nano.init(params, print("connect success"))

        heartbeart = threading.Thread(target=self._send_heart_beat, daemon=True)
        heartbeart.start()
        socket = threading.Thread(target=self.nano.socket.run_forever, daemon=True)
        socket.start()
        time.sleep(2)

    '''
    Send a heartbeat every 6s to ensure the websocket connection
    '''
    def _send_heart_beat(self):
        while True:
            self.nano.sendHeartBeat()
            time.sleep(6)

    '''
    Obtain vland avatar information according to the number
    '''
    def _get_avatar(self, index):
        return "back/cs/outfit/" + str(index) + "/show.png?timestamp=" + str(int(round(time.time() * 1000))) + "&code=1-" + str(index)

    def _on_join_handler(self, data, callback):
        type = "join"
        result = {}
        response = Position()
        response.ParseFromString(data)
        result["type"] = type
        result["data"] = response
        callback(result)
    
    def _on_move_handler(self, data, callback):
        type = "move"
        result = {}
        response = MovePosition()
        response.ParseFromString(data)
        result["type"] = type
        result["data"] = response
        callback(result)
    
    def _on_trigger_area_handler(self, data, callback):
        type = "area"
        result = {}
        response = GameTriggerSpecialAreaNotice()
        response.ParseFromString(data)
        result["type"] = type
        result["data"] = response
        callback(result)
        

    def _on_common_handler(self, data, callback):
        callback(data)

    def _on_exit_handler(self, data, callback):
        response = MovePosition()
        response.ParseFromString(data)
        callback(response)

    def _player_infos_decoder(self, data):
        # 解析字节序列
        type = "get_player_info"
        response = PlayerPositionInfos()
        response.ParseFromString(data)
        # print(response) 
        return {type: type, response: response}

    def _error_decoder(self, data):
        # 解析字节序列
        type = "error"
        response = Error()
        response.ParseFromString(data)
        # print(response)
        return {type: type, response: response}