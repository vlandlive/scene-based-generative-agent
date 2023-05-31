import websocket
import json
import datetime

import threading

from vland.nanoprotocol import Protocol

Message = Protocol.Message
Package = Protocol.Package

class Emitter:
    def init(self, obj=None):
        if obj:
            return self.mixin(obj)

    def mixin(self, obj):
        # 将Emitter类的属性添加到obj对象中
        for key in Emitter.__dict__:
            obj[key] = Emitter.__dict__[key]
        return obj

    def on(self, event, fn):

        # print("onononon", event, event.value)
        event = event.value
        # 初始化_callbacks字典
        self._callbacks = self._callbacks if hasattr(self, '_callbacks') else {}
        # 将fn添加到指定event的回调列表中
        self._callbacks[event] = self._callbacks[event] if event in self._callbacks else []
        self._callbacks[event].append(fn)

        return self

    def once(self, event, fn):
        # 定义只会被调用一次的回调函数
        def on(*args):
            self.off(event, on)
            fn(*args)
        on.fn = fn
        # 将只会被调用一次的回调函数添加到指定event的回调列表中
        self.on(event, on)
        return self

    def off(self, event=None, fn=None):
        # 初始化_callbacks字典
        self._callbacks = self._callbacks if hasattr(self, '_callbacks') else {}
        # remove all
        # 清空所有回调列表
        if not event:
            self._callbacks = {}
            return self
        # remove specific event
        # 清空指定event的回调列表
        if event in self._callbacks:
            # remove all handlers for event
            # 清空指定event的所有回调函数
            if not fn:
                del self._callbacks[event]
                return self
            # remove specific handler for event
            # 清空指定event的特定回调函数
            callbacks = self._callbacks[event]
            for i in range(len(callbacks)):
                cb = callbacks[i]
                if cb == fn or cb.fn == fn:
                    del callbacks[i]
                    break
        return self

    def emit(self, event, *args):
        # 初始化_callbacks字典

        # print("emit", event, *args)
        self._callbacks = self._callbacks if hasattr(self, '_callbacks') else {}
        # 调用指定event的回调函数
        callbacks = self._callbacks[event] if event in self._callbacks else []
        for cb in callbacks:
            cb(*args)
        return self

    def listeners(self, event):
        # 初始化_callbacks字典
        self._callbacks = self._callbacks if hasattr(self, '_callbacks') else {}
        # 返回指定event的回调函数列表
        return self._callbacks[event] if event in self._callbacks else []

    def hasListeners(self, event):
        # 检查指定event是否有回调函数
        return len(self.listeners(event)) > 0


RES_OK = 200
RES_FAIL = 500
RES_OLD_CLIENT = 501
routeMap = {}  # map from request id to route
dict = {}
abbrs = {}  # code to route string

reqId = 0
callbacks = {}

handshakeBuffer = {
    "sys": { "type": "python-websocket", "version": "0.0.1", "res": {} },
    "user": {}
}

sendTime = 0
delay = 0
initCallback = None
heartbeatInterval = 0
heartbeatTimeout = 0
handshakeCallback = None
nextHeartbeatTimeout = 0
heartbeatTimeoutId = None
heartbeatId = None
gapThreshold = 100;  # heartbeat gap threashold

DEFAULT_MAX_RECONNECT_ATTEMPTS = 10





class Nano(Emitter):
    socket = None

    def init(self, params, cb):
        self.initCallback = cb
        host = params['host']
        # port = params['port']
        path = params['path']
        self.encode = self.defaultEncode
        self.decode = self.defaultDecode

        self.dict = params['dict']

        url = host

        self.connect(params, url, cb)

    def defaultDecode(self, data):

        global routeMap
        # print("-----decode-----", data)
        try:
            msg = Message.decode(data)
            # print("decode1", msg, msg['id'], routeMap[msg["id"]])
            # 如果消息有id
            if msg["id"] > 0:
            # 从routeMap中获取对应的route
                msg["route"] = routeMap[msg["id"]]
            # 从routeMap中删除已经获取到的route
                del routeMap[msg["id"]]
                # 如果route不存在，直接返回
                if not msg["route"]:
                    return None
            
            # 解压缩消息体
            msg["body"] = self.deCompose(msg)["body"]

            # print("decode2", msg)
            # 返回解析后的消息对象
            return msg
        except Exception as e:
            print("decode >>>>>>>>>>>>>>>>", e) 
    
    def defaultEncode(self, reqId, route, msg):
        # print("test11111",self.dict)
        # 根据reqId是否存在来判断消息类型
        type = Message.TYPE_REQUEST if reqId else Message.TYPE_NOTIFY
        # 初始化压缩路由的标志位
        compressRoute = 0

        # 如果缩写字典中存在对应的路由
        if self.dict and self.dict[route]:
            # 将路由替换为缩写的路由
            route = self.dict[route]
            # 设置压缩路由的标志位
            compressRoute = 1    
    
        # 初始化压缩消息体的标志位和新消息对象
        zip = False
        newmsg = msg
        

        # 调用Message类的encode方法编码消息
        buffer = Message.encode(reqId, type, compressRoute, route, newmsg, zip)
        # print("?1231231??", reqId)

        # 返回编码后的消息字节数组
        return buffer

    def connect(self, params, url, cb):
        params = params or {}
        maxReconnectAttempts = DEFAULT_MAX_RECONNECT_ATTEMPTS
        reconnectUrl = url

        def on_open(ws):
            obj = Package.encode(Package.TYPE_HANDSHAKE, Protocol.strencode(json.dumps(handshakeBuffer)))
            # print("first handshake", obj)
            self.send(obj)
            # print("connect success")
            return 200

        def on_message(ws, message):
            # print("message: ", message )
            global nextHeartbeatTimeout, heartbeatTimeout
            try:
                self.processPackage(Package.decode(message))
            except Exception as e:
                print("on_message>>>>>>>>>>>>>>>>", e)   
            if heartbeatTimeout:
                nextHeartbeatTimeout = datetime.datetime.now().timestamp() * 1000 + heartbeatTimeout
            # print("recive", Package.decode(message))
            

        def on_error(ws, error):
            self.emit('io-error', error)
            print("on_error>>>>>>>>>>>>>>>>>>>>", error)
            return 500

        def on_close(ws, code, msg):
            ws.close()
            ws = None
                
            self.emit('close', ws)
            self.emit('disconnect', ws)

        ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
        self.socket = ws
        # ws.run_forever()

    # 发送一次消息 并且带有回调函数
    def request(self, route, msg, cb=None):
        global reqId, routeMap
        try: 
            # print("<><><><><><<<<<<<<<<<<<<<<<_________", cb, callable(msg), route)
            if cb is None and callable(msg):
                cb = msg
                msg = {}
            else:
                msg = msg or {}

            route = route or msg['route']

            if not route:
                return
        except Exception as e:
            print('deve nano.request error1', e)
        
        try:
            reqId += 1
            self.sendMessage(reqId, route, msg)
            # print("发送完消息了", route)
            callbacks[reqId] = cb
            routeMap[reqId] = route
        except Exception as e:
            print('deve nano.request error2', e)

    # 发送一次消息 没有带有回调函数
    def notify(self, route, msg):
        msg = msg or {}
        try:
            self.sendMessage(0, route, msg)
        except Exception as e:
            print('deve nano.notify error', e)

    def sendMessage(self, reqId, route, msg):
        
        # print("sendMessage", route)

        try:
            if self.encode:
                # msg = self.encode(reqId, route, msg, True)
                msg = self.encode(reqId, route, msg)
        except Exception as e:
            print('sendMessage error2', e)
        
        packet = Package.encode(Package.TYPE_DATA, msg)
        # print("<<<<<<", packet)
        self.send(packet)

    def sendHeartBeat(self):
        self.heartbeat()
        


    def heartbeat(self):
        global heartbeatInterval, heartbeatTimeoutId, heartbeatId, nextHeartbeatTimeout, sendTime, heartbeatTimeout
        
        if not heartbeatInterval:   
            # no heartbeat
            return
        obj = Package.encode(Package.TYPE_HEARTBEAT, "")

        if heartbeatTimeoutId:
            heartbeatTimeoutId.cancel()
            heartbeatTimeoutId = None
        if heartbeatId:
            # already in a heartbeat interval
            return
        
        try:    
            heartbeatId = None
            self.send(obj)
            sendTime = datetime.datetime.now().timestamp() * 1000
            nextHeartbeatTimeout = datetime.datetime.now().timestamp() * 1000 + heartbeatTimeout

            heartbeatTimeoutId = threading.Timer(heartbeatTimeout / 1000, self.heartbeatTimeoutCb)
            heartbeatTimeoutId.start()

            # print("<><><>heartbeat", heartbeatTimeout, sendTime, nextHeartbeatTimeout, heartbeatTimeoutId)
        except Exception as e:
            print('heartbeat error', e)
       

    def heartbeatTimeoutCb(self):   
            global gapThreshold, nextHeartbeatTimeout, heartbeatTimeoutId
            gap = nextHeartbeatTimeout - datetime.datetime.now().timestamp() * 1000
            print("?<<>>><?<>?>?>?<<", nextHeartbeatTimeout, datetime.datetime.now().timestamp() * 1000, gap)
            if gap > gapThreshold:
                heartbeatTimeoutId = threading.Timer(heartbeatTimeout / 1000, gap)
            else:
                self.emit('heartbeat timeout')
                self.disconnect()    


    def disconnect(self):
       
        global heartbeatId, heartbeatTimeoutId
        # print("?<<>>><?<>?>?>?<<", self.socket, self.socket.close)
        if self.socket:
            if self.socket.close:
                self.socket.close()
            self.socket = None
        if heartbeatId:
            heartbeatId.cancel()
            heartbeatId = None
        if heartbeatTimeoutId:
            heartbeatTimeoutId.cancel()
            heartbeatTimeoutId = None

    def end(self):
        self.socket.close()    

    def deCompose(self, msg):
        
        global abbrs

        try:            
            # 获取route
            route = msg["route"]
            # 如果路由被压缩
            if msg["compressRoute"]:
                # 从缩写字典中获取完整的路由
                if route in abbrs:
                    route = msg["route"] = abbrs[route]
                else:
                    return {}
                
            # print("route", route, abbrs[route], msg["route"])
                
        except Exception as error:
            print("deCompose error", error)
        # 返回解析后的消息对象
        return msg
    
    def processPackage(self, msgs):
        global delay

        handlers = {
            Package.TYPE_HANDSHAKE: self.handshake,
            Package.TYPE_HEARTBEAT: self.heartbeat,
            Package.TYPE_HANDSHAKE_ACK: self.handshakeack,
            Package.TYPE_DATA: self.onData,
            Package.TYPE_KICK: self.onKick
        }
        if isinstance(msgs, list):
            # print(">>>>>>>>>>>>>>>>???????????????")
            for msg in msgs:
                handlers[msg["type"]](self, msg["body"])
        else:
            # print("processPackage", msgs['type'])
            if msgs['type'] == Package.TYPE_HEARTBEAT:
                if sendTime != 0:
                    currentTime = datetime.datetime.now().timestamp() * 1000
                    delay = currentTime - sendTime
                return
            handlers[msgs['type']](msgs['body'])

    
    def processMessage(self, msg):
        if not msg.get('id'):
            # server push message
            self.emit(msg.get('route'), msg.get('body'))
            return
        
        # if have an id then find the callback function with the request
        cb = callbacks.get(msg.get('id'))
        # print("processMessage", cb, msg.get('id'), callbacks.get(msg.get('id')))

        try:

            del callbacks[msg.get('id')]
            if not callable(cb):
                return

            cb(msg.get('body'))


        except Exception as error:
            print("processMessage error", error)


    def send(self, packet):
        # print("send??????", packet, type(packet), memoryview(packet))
        try:
            if self.socket:
                self.socket.send(memoryview(packet))

        except Exception as error:
            print("send error", error)
    
    def handshake(self, data):
        
        data = json.loads(Protocol.strdecode(data))

        if data['code'] == RES_OLD_CLIENT:
            self.emit('error', 'client version not fullfill')
            return
        if data['code'] != RES_OK:
            self.emit('error', 'handshake fail')
            return
        
        self.handshakeInit(data)
        
        obj = Package.encode(Package.TYPE_HANDSHAKE_ACK, "")
        heatObj = Package.encode(Package.TYPE_HEARTBEAT, "")
        self.send(obj)
        self.send(heatObj)
        if initCallback:
            initCallback(self.socket)
            

    def handshakeack(self, data):
        print('handshakeack success')

    def onData(self, data):
        # print("-----ondata-----", self.decode)

        try:
            msg = data
            if self.decode:
                # print("123123123")
                msg = self.decode(msg)
                
            self.processMessage(msg)
        except Exception as error:
            print("ondata error", error, "\n\n")


    def onKick(self, data):
        data = json.loads(Protocol.strdecode(data))
        self.emit('onKick', data)

    def handshakeInit(self, data):
        global heartbeatInterval, heartbeatTimeout
        # print("handshake", data['sys']['heartbeat'])
        if data['sys'] and data['sys']['heartbeat']:
            heartbeatInterval = data['sys']['heartbeat'] * 1000 # heartbeat interval
            heartbeatTimeout = heartbeatInterval * 2 # max heartbeat timeout
        else:
            heartbeatInterval = 0
            heartbeatTimeout = 0
        
        self.initData(data)
        if callable(handshakeCallback):
            handshakeCallback(data['user'])


    def initData(self, data):   
        global dict, abbrs
        if not data or not data['sys']:
            return
        dict = dict or data['sys']['dict']
        if dict:
            dict = dict
            abbrs = {}
            for route in dict:
                abbrs[dict[route]] = route
        # global.nano = self
        # global.socket = self.socket
        # print("<><><<><><><><><><><><>", self)


# nano = Nano()




# def callback_function(data):
#     print("Received data:", data)

# print(nano)

# nano.on("test", callback_function)

# nano.emit('test', 'Hello World')