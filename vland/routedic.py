from enum import Enum

class ServerPush(Enum):
    NewPosition = 'NewPosition'
    OnMove = 'OnMove'
    Exit = 'Exit'
    SpaceClose = 'SpaceClose'
    Animation = 'Animation'
    SendNearMessage = 'SendNearMessage'
    SendGlobalMessage = 'SendGlobalMessage'
    SendEventMessage = 'SendEventMessage'
    SendPrivateMessage = 'SendPrivateMessage'
    PrepareGameRoute = "PrepareGame"
    TriggerInteractiveObjectRoute = "TriggerInteractiveObject"
    FinishGameRoute = "FinishGame"
    GameTriggerSpecialAreaRoute = "GameTriggerSpecialArea"
    GameTriggerInteractiveRoute = "GameTriggerInteractive"
    OpenVideo = 'OpenVideo'
    CloseVideo = 'CloseVideo'

class ApiRoute(Enum):
    CHANGE_SPACE_STATUS = "connector.api.changespacestatus"
    CHANGE_EVENT_STATUS = "connector.api.changeeventstatus"
    DELETE_CHAT_MESSAGE = "connector.api.deletechatmessage"
    CHANGE_BGM = "connector.api.changebgm"
    BROADCAST_EVENT_SPECIAL_EFFECTS = "connector.api.broadcasteventspecialeffects"
    GET_PLAYER_INFO = "connector.api.getplayerinfo"
    CHANGE_PLAYER_POSITION = "connector.api.changeplayerposition"
    CHANGE_PLAYER_DIRECTION = "connector.api.changeplayerdirection"
    CHANGE_PLAYER_ANIMATION = "connector.api.changeplayeranimation"
    CHANGE_PLAYER_MOVE_MODE = "connector.api.changeplayermovemode"
    CHANGE_PLAYER_FOLLOW = "connector.api.changeplayerfollow"
    CHANGE_PLAYER_AVATAR = "connector.api.changeplayerimage"
    ADD_PLAYER_LISTENER = "connector.api.addplayerlistener"
    REMOVE_PLAYER_LISTENER = "connector.api.removeplayerlistener"
    CONNECT_SPACE = "connector.connector.connectspace"
    JOIN = "logic.space.join"

    GET_SPACE_MAP_INFO = "connector.api.getspacemapinfo"
    ADD_SPACE_MAP_BIRTH = "connector.api.addspacemapbirth"
    REMOVE_SPACE_MAP_BIRTH = "connector.api.removespacemapbirth"
    ADD_SPACE_MAP_OBSTACLE = "connector.api.addspacemapobstacle"
    REMOVE_SPACE_MAP_OBSTACLE = "connector.api.removespacemapobstacle"
    ADD_SPACE_MAP_LANDMARK = "connector.api.addspacemaplandmark"
    REMOVE_SPACE_MAP_LANDMARK = "connector.api.removespacemaplandmark"
    ADD_SPACE_MAP_PORTAL = "connector.api.addspacemapportal"
    REMOVE_SPACE_MAP_PORTAL = "connector.api.removespacemapportal"
    ADD_SPACE_MAP_GRIDMATERIAL = "connector.api.addspacemapgridmaterial"
    CLEAR_SPACE_MAP_GRIDMATERIAL = "connector.api.clearspacemapgridmaterial"

    INIT_GAME = "connector.api.initgame"
    PRESTART_GAME = "connector.api.prestartgame"
    GAME_COUNT_DOWN = "connector.api.gamecountdown"
    UPDATE_GAME_RANK_LIST = "connector.api.updategameranklist"
    STOP_GAME = "connector.api.stopgame"
    GAME_TOAST = "connector.api.gametoast"
    FINISH_GAME = "connector.api.finishgame"
    GAME_EFFECT = "connector.api.gameinteractiveeffect"

    CHANGE_SPEED = "connector.api.changemovespeed"
    CHANGE_SPACE_SETTING = "connector.api.changespacesetting"
    GET_SPECIAL_AREA_INFO = "connector.api.getspecialareaplayerinfo"
    SHOW_WIDHET = "connector.api.showwidget"
    ROBOT_JOIN = "connector.api.robotjoin"
    ROBOT_MOVE = "connector.api.robotmove"
    ROBOT_EXIT = "connector.api.robotexit"

RouteDic = {
    ServerPush.NewPosition: 20002,
    ServerPush.OnMove: 20004,
    ServerPush.Exit: 20026,
    ServerPush.SpaceClose: 20080,
    ServerPush.Animation: 20023,
    ServerPush.SendNearMessage: 20011,
    ServerPush.SendGlobalMessage: 20012,
    ServerPush.SendEventMessage: 20066,
    ServerPush.SendPrivateMessage: 20013,
    ServerPush.PrepareGameRoute: 21036,
    ServerPush.FinishGameRoute: 21037,
    ServerPush.GameTriggerSpecialAreaRoute: 21038,
    ServerPush.GameTriggerInteractiveRoute: 21039,
    ServerPush.OpenVideo:20005,
    ServerPush.CloseVideo:20006,

    ApiRoute.CONNECT_SPACE: 10001,
    ApiRoute.JOIN: 10002,
    ApiRoute.CHANGE_SPACE_STATUS: 60002,
    ApiRoute.CHANGE_EVENT_STATUS: 60003,
    ApiRoute.DELETE_CHAT_MESSAGE: 60004,
    ApiRoute.CHANGE_BGM: 60005,
    ApiRoute.BROADCAST_EVENT_SPECIAL_EFFECTS: 60006,
    ApiRoute.GET_PLAYER_INFO: 60011,
    ApiRoute.CHANGE_PLAYER_POSITION: 60012,
    ApiRoute.CHANGE_PLAYER_DIRECTION: 60013,
    ApiRoute.CHANGE_PLAYER_ANIMATION: 60014,
    ApiRoute.CHANGE_PLAYER_MOVE_MODE: 60015,
    ApiRoute.CHANGE_PLAYER_AVATAR: 60016,
    ApiRoute.CHANGE_PLAYER_FOLLOW: 60017,
    ApiRoute.ADD_PLAYER_LISTENER: 60018,
    ApiRoute.REMOVE_PLAYER_LISTENER: 60019,

    ApiRoute.GET_SPACE_MAP_INFO: 60031,
    ApiRoute.ADD_SPACE_MAP_BIRTH: 60032,
    ApiRoute.REMOVE_SPACE_MAP_BIRTH: 60033,
    ApiRoute.ADD_SPACE_MAP_OBSTACLE: 60034,
    ApiRoute.REMOVE_SPACE_MAP_OBSTACLE: 60035,
    ApiRoute.ADD_SPACE_MAP_LANDMARK: 60036,
    ApiRoute.REMOVE_SPACE_MAP_LANDMARK: 60037,
    ApiRoute.ADD_SPACE_MAP_PORTAL: 60038,
    ApiRoute.REMOVE_SPACE_MAP_PORTAL: 60039,
    ApiRoute.ADD_SPACE_MAP_GRIDMATERIAL: 60040,
    ApiRoute.CLEAR_SPACE_MAP_GRIDMATERIAL: 60041,

    ApiRoute.INIT_GAME: 60050,
    ApiRoute.PRESTART_GAME: 60051,
    ApiRoute.GAME_COUNT_DOWN: 60052,
    ApiRoute.UPDATE_GAME_RANK_LIST: 60053,
    ApiRoute.STOP_GAME: 60054,
    ApiRoute.GAME_TOAST: 60055,
    ApiRoute.FINISH_GAME: 60056,
    ApiRoute.GAME_EFFECT: 60057,
    ApiRoute.CHANGE_SPEED: 60058,
    ApiRoute.CHANGE_SPACE_SETTING: 60059,
    ApiRoute.GET_SPECIAL_AREA_INFO:60060,
    ApiRoute.SHOW_WIDHET:60061,
    ApiRoute.ROBOT_JOIN:60091,
    ApiRoute.ROBOT_MOVE:60092,
    ApiRoute.ROBOT_EXIT:60093,
}