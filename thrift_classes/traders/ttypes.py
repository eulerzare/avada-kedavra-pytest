#
# Autogenerated by Thrift Compiler (0.21.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys
import thrift_classes.base.ttypes

from thrift.transport import TTransport
all_structs = []


class AddTrader(object):
    """
    Attributes:
     - uniqueId

    """


    def __init__(self, uniqueId=None,):
        self.uniqueId = uniqueId

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.uniqueId = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('AddTrader')
        if self.uniqueId is not None:
            oprot.writeFieldBegin('uniqueId', TType.STRING, 1)
            oprot.writeString(self.uniqueId.encode('utf-8') if sys.version_info[0] == 2 else self.uniqueId)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.uniqueId is None:
            raise TProtocolException(message='Required field uniqueId is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class AddTraderResponse(object):
    """
    Attributes:
     - status
     - message
     - uniqueId

    """


    def __init__(self, status=None, message=None, uniqueId=None,):
        self.status = status
        self.message = message
        self.uniqueId = uniqueId

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.status = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.message = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.uniqueId = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('AddTraderResponse')
        if self.status is not None:
            oprot.writeFieldBegin('status', TType.I32, 1)
            oprot.writeI32(self.status)
            oprot.writeFieldEnd()
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 2)
            oprot.writeString(self.message.encode('utf-8') if sys.version_info[0] == 2 else self.message)
            oprot.writeFieldEnd()
        if self.uniqueId is not None:
            oprot.writeFieldBegin('uniqueId', TType.STRING, 3)
            oprot.writeString(self.uniqueId.encode('utf-8') if sys.version_info[0] == 2 else self.uniqueId)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(AddTrader)
AddTrader.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'uniqueId', 'UTF8', None, ),  # 1
)
all_structs.append(AddTraderResponse)
AddTraderResponse.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'status', None, None, ),  # 1
    (2, TType.STRING, 'message', 'UTF8', None, ),  # 2
    (3, TType.STRING, 'uniqueId', 'UTF8', None, ),  # 3
)
fix_spec(all_structs)
del all_structs
