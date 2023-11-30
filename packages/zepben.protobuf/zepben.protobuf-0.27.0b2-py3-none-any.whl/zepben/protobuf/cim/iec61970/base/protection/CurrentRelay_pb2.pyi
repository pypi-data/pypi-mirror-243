from zepben.protobuf.cim.iec61970.base.protection import ProtectionEquipment_pb2 as _ProtectionEquipment_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CurrentRelay(_message.Message):
    __slots__ = ["pe", "currentLimit1", "inverseTimeFlagNull", "inverseTimeFlagSet", "timeDelay1"]
    PE_FIELD_NUMBER: _ClassVar[int]
    CURRENTLIMIT1_FIELD_NUMBER: _ClassVar[int]
    INVERSETIMEFLAGNULL_FIELD_NUMBER: _ClassVar[int]
    INVERSETIMEFLAGSET_FIELD_NUMBER: _ClassVar[int]
    TIMEDELAY1_FIELD_NUMBER: _ClassVar[int]
    pe: _ProtectionEquipment_pb2.ProtectionEquipment
    currentLimit1: float
    inverseTimeFlagNull: _struct_pb2.NullValue
    inverseTimeFlagSet: bool
    timeDelay1: float
    def __init__(self, pe: _Optional[_Union[_ProtectionEquipment_pb2.ProtectionEquipment, _Mapping]] = ..., currentLimit1: _Optional[float] = ..., inverseTimeFlagNull: _Optional[_Union[_struct_pb2.NullValue, str]] = ..., inverseTimeFlagSet: bool = ..., timeDelay1: _Optional[float] = ...) -> None: ...
