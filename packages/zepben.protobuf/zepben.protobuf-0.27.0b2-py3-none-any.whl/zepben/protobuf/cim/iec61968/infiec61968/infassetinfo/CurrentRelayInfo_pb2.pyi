from zepben.protobuf.cim.iec61968.assets import AssetInfo_pb2 as _AssetInfo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CurrentRelayInfo(_message.Message):
    __slots__ = ["ai", "curveSetting", "recloseDelays"]
    AI_FIELD_NUMBER: _ClassVar[int]
    CURVESETTING_FIELD_NUMBER: _ClassVar[int]
    RECLOSEDELAYS_FIELD_NUMBER: _ClassVar[int]
    ai: _AssetInfo_pb2.AssetInfo
    curveSetting: str
    recloseDelays: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, ai: _Optional[_Union[_AssetInfo_pb2.AssetInfo, _Mapping]] = ..., curveSetting: _Optional[str] = ..., recloseDelays: _Optional[_Iterable[float]] = ...) -> None: ...
