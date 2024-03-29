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


class AddAccount(object):
    """
    Attributes:
     - id
     - currencySymbol
     - genre
     - accountType
     - pairId

    """


    def __init__(self, id=None, currencySymbol=None, genre=None, accountType=None, pairId=None,):
        self.id = id
        self.currencySymbol = currencySymbol
        self.genre = genre
        self.accountType = accountType
        self.pairId = pairId

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
                if ftype == TType.I64:
                    self.id = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.currencySymbol = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.genre = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I32:
                    self.accountType = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I32:
                    self.pairId = iprot.readI32()
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
        oprot.writeStructBegin('AddAccount')
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.I64, 1)
            oprot.writeI64(self.id)
            oprot.writeFieldEnd()
        if self.currencySymbol is not None:
            oprot.writeFieldBegin('currencySymbol', TType.STRING, 2)
            oprot.writeString(self.currencySymbol.encode('utf-8') if sys.version_info[0] == 2 else self.currencySymbol)
            oprot.writeFieldEnd()
        if self.genre is not None:
            oprot.writeFieldBegin('genre', TType.I32, 3)
            oprot.writeI32(self.genre)
            oprot.writeFieldEnd()
        if self.accountType is not None:
            oprot.writeFieldBegin('accountType', TType.I32, 4)
            oprot.writeI32(self.accountType)
            oprot.writeFieldEnd()
        if self.pairId is not None:
            oprot.writeFieldBegin('pairId', TType.I32, 5)
            oprot.writeI32(self.pairId)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.id is None:
            raise TProtocolException(message='Required field id is unset!')
        if self.currencySymbol is None:
            raise TProtocolException(message='Required field currencySymbol is unset!')
        if self.genre is None:
            raise TProtocolException(message='Required field genre is unset!')
        if self.accountType is None:
            raise TProtocolException(message='Required field accountType is unset!')
        if self.pairId is None:
            raise TProtocolException(message='Required field pairId is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(AddAccount)
AddAccount.thrift_spec = (
    None,  # 0
    (1, TType.I64, 'id', None, None, ),  # 1
    (2, TType.STRING, 'currencySymbol', 'UTF8', None, ),  # 2
    (3, TType.I32, 'genre', None, None, ),  # 3
    (4, TType.I32, 'accountType', None, None, ),  # 4
    (5, TType.I32, 'pairId', None, None, ),  # 5
)
fix_spec(all_structs)
del all_structs
