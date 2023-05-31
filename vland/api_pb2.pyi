from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DANCE_1: AnimationType
DANCE_10: AnimationType
DANCE_2: AnimationType
DANCE_3: AnimationType
DANCE_4: AnimationType
DANCE_5: AnimationType
DANCE_6: AnimationType
DANCE_7: AnimationType
DANCE_8: AnimationType
DANCE_9: AnimationType
DESCRIPTOR: _descriptor.FileDescriptor
DOWN: DirectionType
FLY_MODE: MoveMode
Guest: Identity
HELLO_B: AnimationType
HELLO_F: AnimationType
HELLO_P: AnimationType
JUMP_B: AnimationType
JUMP_F: AnimationType
JUMP_P: AnimationType
LEFT: DirectionType
NORMAL: StatusType
NORMAL_MODE: MoveMode
Normal: Identity
OFFLINE: StatusType
RIGHT: DirectionType
Role_1: RoleType
Role_2: RoleType
Role_3: RoleType
Role_4: RoleType
Role_5: RoleType
SIT_B: AnimationType
SIT_F: AnimationType
SIT_P: AnimationType
STAND_B: AnimationType
STAND_F: AnimationType
STAND_P: AnimationType
UP: DirectionType
WALK_B: AnimationType
WALK_F: AnimationType
WALK_P: AnimationType

class AddPlayerListenerCmd(_message.Message):
    __slots__ = ["eventId", "listenerId", "pidArr", "signal", "spaceId"]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    LISTENERID_FIELD_NUMBER: _ClassVar[int]
    PIDARR_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    eventId: str
    listenerId: str
    pidArr: _containers.RepeatedScalarFieldContainer[str]
    signal: int
    spaceId: str
    def __init__(self, eventId: _Optional[str] = ..., spaceId: _Optional[str] = ..., listenerId: _Optional[str] = ..., pidArr: _Optional[_Iterable[str]] = ..., signal: _Optional[int] = ...) -> None: ...

class ConnectSpaceReq(_message.Message):
    __slots__ = ["EventId", "Pid", "SpaceId"]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    EventId: str
    PID_FIELD_NUMBER: _ClassVar[int]
    Pid: str
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    SpaceId: str
    def __init__(self, SpaceId: _Optional[str] = ..., Pid: _Optional[str] = ..., EventId: _Optional[str] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ["Code", "Metadata", "Msg"]
    class MetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CODE_FIELD_NUMBER: _ClassVar[int]
    Code: str
    METADATA_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    Metadata: _containers.ScalarMap[str, str]
    Msg: str
    def __init__(self, Code: _Optional[str] = ..., Msg: _Optional[str] = ..., Metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GameTriggerSpecialAreaNotice(_message.Message):
    __slots__ = ["name", "pid"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    name: str
    pid: str
    def __init__(self, pid: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetPlayerInfoCmd(_message.Message):
    __slots__ = ["eventId", "pidArr", "spaceId"]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    PIDARR_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    eventId: str
    pidArr: _containers.RepeatedScalarFieldContainer[str]
    spaceId: str
    def __init__(self, eventId: _Optional[str] = ..., spaceId: _Optional[str] = ..., pidArr: _Optional[_Iterable[str]] = ...) -> None: ...

class GetSpecialAreaPlayerInfoCmd(_message.Message):
    __slots__ = ["eventId", "index", "spaceId"]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    eventId: str
    index: int
    spaceId: str
    def __init__(self, eventId: _Optional[str] = ..., spaceId: _Optional[str] = ..., index: _Optional[int] = ...) -> None: ...

class MovePosition(_message.Message):
    __slots__ = ["Pid", "Transfer", "X", "Y"]
    PID_FIELD_NUMBER: _ClassVar[int]
    Pid: str
    TRANSFER_FIELD_NUMBER: _ClassVar[int]
    Transfer: bool
    X: int
    X_FIELD_NUMBER: _ClassVar[int]
    Y: int
    Y_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, Pid: _Optional[str] = ..., X: _Optional[int] = ..., Y: _Optional[int] = ..., Transfer: bool = ...) -> None: ...

class Pid(_message.Message):
    __slots__ = ["Pid"]
    PID_FIELD_NUMBER: _ClassVar[int]
    Pid: str
    def __init__(self, Pid: _Optional[str] = ...) -> None: ...

class Pids(_message.Message):
    __slots__ = ["Pid"]
    PID_FIELD_NUMBER: _ClassVar[int]
    Pid: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, Pid: _Optional[_Iterable[str]] = ...) -> None: ...

class PlayerPositionInfos(_message.Message):
    __slots__ = ["positionArr"]
    POSITIONARR_FIELD_NUMBER: _ClassVar[int]
    positionArr: _containers.RepeatedCompositeFieldContainer[Position]
    def __init__(self, positionArr: _Optional[_Iterable[_Union[Position, _Mapping]]] = ...) -> None: ...

class Position(_message.Message):
    __slots__ = ["A", "Angle", "B", "D", "I", "Identity", "IsRaiseHand", "MoveMode", "Pets", "Pid", "RealName", "RoleName", "RoleType", "S", "X", "Y", "Z"]
    A: AnimationType
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    A_FIELD_NUMBER: _ClassVar[int]
    Angle: int
    B: bool
    B_FIELD_NUMBER: _ClassVar[int]
    D: DirectionType
    D_FIELD_NUMBER: _ClassVar[int]
    I: str
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    ISRAISEHAND_FIELD_NUMBER: _ClassVar[int]
    I_FIELD_NUMBER: _ClassVar[int]
    Identity: Identity
    IsRaiseHand: bool
    MOVEMODE_FIELD_NUMBER: _ClassVar[int]
    MoveMode: MoveMode
    PETS_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    Pets: _containers.RepeatedScalarFieldContainer[str]
    Pid: str
    REALNAME_FIELD_NUMBER: _ClassVar[int]
    ROLENAME_FIELD_NUMBER: _ClassVar[int]
    ROLETYPE_FIELD_NUMBER: _ClassVar[int]
    RealName: str
    RoleName: str
    RoleType: RoleType
    S: StatusType
    S_FIELD_NUMBER: _ClassVar[int]
    X: int
    X_FIELD_NUMBER: _ClassVar[int]
    Y: int
    Y_FIELD_NUMBER: _ClassVar[int]
    Z: int
    Z_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, Pid: _Optional[str] = ..., RealName: _Optional[str] = ..., X: _Optional[int] = ..., Y: _Optional[int] = ..., Z: _Optional[int] = ..., Angle: _Optional[int] = ..., D: _Optional[_Union[DirectionType, str]] = ..., A: _Optional[_Union[AnimationType, str]] = ..., S: _Optional[_Union[StatusType, str]] = ..., B: bool = ..., I: _Optional[str] = ..., MoveMode: _Optional[_Union[MoveMode, str]] = ..., IsRaiseHand: bool = ..., Identity: _Optional[_Union[Identity, str]] = ..., Pets: _Optional[_Iterable[str]] = ..., RoleName: _Optional[str] = ..., RoleType: _Optional[_Union[RoleType, str]] = ...) -> None: ...

class RemovePlayerListenerCmd(_message.Message):
    __slots__ = ["eventId", "listenerId", "pidArr", "spaceId"]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    LISTENERID_FIELD_NUMBER: _ClassVar[int]
    PIDARR_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    eventId: str
    listenerId: str
    pidArr: _containers.RepeatedScalarFieldContainer[str]
    spaceId: str
    def __init__(self, eventId: _Optional[str] = ..., spaceId: _Optional[str] = ..., listenerId: _Optional[str] = ..., pidArr: _Optional[_Iterable[str]] = ...) -> None: ...

class RobotExitCmd(_message.Message):
    __slots__ = ["EventId", "RobotIdArr", "SpaceId"]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    EventId: str
    ROBOTIDARR_FIELD_NUMBER: _ClassVar[int]
    RobotIdArr: _containers.RepeatedScalarFieldContainer[str]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    SpaceId: str
    def __init__(self, EventId: _Optional[str] = ..., SpaceId: _Optional[str] = ..., RobotIdArr: _Optional[_Iterable[str]] = ...) -> None: ...

class RobotJoinCmd(_message.Message):
    __slots__ = ["EventId", "SpaceId", "joinInfoArr"]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    EventId: str
    JOININFOARR_FIELD_NUMBER: _ClassVar[int]
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    SpaceId: str
    joinInfoArr: _containers.RepeatedCompositeFieldContainer[RobotJoinInfo]
    def __init__(self, EventId: _Optional[str] = ..., SpaceId: _Optional[str] = ..., joinInfoArr: _Optional[_Iterable[_Union[RobotJoinInfo, _Mapping]]] = ...) -> None: ...

class RobotJoinInfo(_message.Message):
    __slots__ = ["Avatar", "RobotId", "RobotName", "X", "Y"]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    Avatar: str
    ROBOTID_FIELD_NUMBER: _ClassVar[int]
    ROBOTNAME_FIELD_NUMBER: _ClassVar[int]
    RobotId: str
    RobotName: str
    X: int
    X_FIELD_NUMBER: _ClassVar[int]
    Y: int
    Y_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, RobotId: _Optional[str] = ..., RobotName: _Optional[str] = ..., Avatar: _Optional[str] = ..., X: _Optional[int] = ..., Y: _Optional[int] = ...) -> None: ...

class RobotMoveCmd(_message.Message):
    __slots__ = ["ChatMessage", "EventId", "RobotId", "SpaceId", "X", "Y"]
    CHATMESSAGE_FIELD_NUMBER: _ClassVar[int]
    ChatMessage: str
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    EventId: str
    ROBOTID_FIELD_NUMBER: _ClassVar[int]
    RobotId: str
    SPACEID_FIELD_NUMBER: _ClassVar[int]
    SpaceId: str
    X: int
    X_FIELD_NUMBER: _ClassVar[int]
    Y: int
    Y_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, EventId: _Optional[str] = ..., SpaceId: _Optional[str] = ..., RobotId: _Optional[str] = ..., X: _Optional[int] = ..., Y: _Optional[int] = ..., ChatMessage: _Optional[str] = ...) -> None: ...

class RoleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Identity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class MoveMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class StatusType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class AnimationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DirectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
