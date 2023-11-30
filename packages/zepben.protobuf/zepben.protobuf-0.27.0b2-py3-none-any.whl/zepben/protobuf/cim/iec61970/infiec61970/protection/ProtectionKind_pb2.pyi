from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ProtectionKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN: _ClassVar[ProtectionKind]
    EF: _ClassVar[ProtectionKind]
    SEF: _ClassVar[ProtectionKind]
    OC: _ClassVar[ProtectionKind]
    IOC: _ClassVar[ProtectionKind]
    IEF: _ClassVar[ProtectionKind]
    REF: _ClassVar[ProtectionKind]
UNKNOWN: ProtectionKind
EF: ProtectionKind
SEF: ProtectionKind
OC: ProtectionKind
IOC: ProtectionKind
IEF: ProtectionKind
REF: ProtectionKind
