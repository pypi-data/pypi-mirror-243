from zepben.protobuf.cim.iec61970.base.core import Equipment_pb2 as _Equipment_pb2
from zepben.protobuf.cim.iec61970.infiec61970.protection import PowerDirectionKind_pb2 as _PowerDirectionKind_pb2
from zepben.protobuf.cim.iec61970.infiec61970.protection import ProtectionKind_pb2 as _ProtectionKind_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtectionEquipment(_message.Message):
    __slots__ = ["eq", "relayDelayTime", "protectionKind", "protectedSwitchMRIDs", "directableNull", "directableSet", "powerDirection"]
    EQ_FIELD_NUMBER: _ClassVar[int]
    RELAYDELAYTIME_FIELD_NUMBER: _ClassVar[int]
    PROTECTIONKIND_FIELD_NUMBER: _ClassVar[int]
    PROTECTEDSWITCHMRIDS_FIELD_NUMBER: _ClassVar[int]
    DIRECTABLENULL_FIELD_NUMBER: _ClassVar[int]
    DIRECTABLESET_FIELD_NUMBER: _ClassVar[int]
    POWERDIRECTION_FIELD_NUMBER: _ClassVar[int]
    eq: _Equipment_pb2.Equipment
    relayDelayTime: float
    protectionKind: _ProtectionKind_pb2.ProtectionKind
    protectedSwitchMRIDs: _containers.RepeatedScalarFieldContainer[str]
    directableNull: _struct_pb2.NullValue
    directableSet: bool
    powerDirection: _PowerDirectionKind_pb2.PowerDirectionKind
    def __init__(self, eq: _Optional[_Union[_Equipment_pb2.Equipment, _Mapping]] = ..., relayDelayTime: _Optional[float] = ..., protectionKind: _Optional[_Union[_ProtectionKind_pb2.ProtectionKind, str]] = ..., protectedSwitchMRIDs: _Optional[_Iterable[str]] = ..., directableNull: _Optional[_Union[_struct_pb2.NullValue, str]] = ..., directableSet: bool = ..., powerDirection: _Optional[_Union[_PowerDirectionKind_pb2.PowerDirectionKind, str]] = ...) -> None: ...
