from struct import pack, unpack


class Datatype(object):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def encode(self):
        pass

    @classmethod
    def decode(cls, data):
        pass

    def hex(self):
        return f'0x{int.from_bytes(self.encode(), "big"):0{len(self)}X}'

    def __repr__(self):
        out = f'{self.__class__.__name__}(data={self.data}, len={len(self)})'
        return out


class Byte(Datatype):
    @classmethod
    def decode(cls, data):
        byte_data = unpack(f'!{len(data)}s', data)
        return cls(*byte_data)

    def encode(self):
        return pack(f'!{len(self)}s', self.data)


class Boolean(Datatype):
    @classmethod
    def decode(cls, data):
        bool_data = unpack('!?', data)
        return cls(*bool_data)

    def encode(self):
        if self.data:
            return b'\x01'
        return b'\x00'

    def __len__(self):
        return 1


class UInt32(Datatype):
    @classmethod
    def decode(cls, data):
        uint_data = unpack('!I', data)
        return cls(*uint_data)

    def encode(self):
        return pack('!I', self.data)

    def __len__(self):
        return 4


class UInt64(Datatype):
    @classmethod
    def decode(cls, data):
        uint_data = unpack('!Q', data)
        return cls(*uint_data)

    def encode(self):
        return pack('!Q', self.data)

    def __len__(self):
        return 8


class String(Datatype):
    @classmethod
    def decode(cls, data):
        size = unpack('!I', data[:4])
        string_data = unpack(f'!{size}s', data[4:])
        return cls(*string_data)

    def encode(self):
        return pack(f'!I{len(self)}s', len(self), self.data)

    def __len__(self):
        return 4+len(self.data)


class MPInt(Datatype):
    @classmethod
    def decode(cls, data):
        size = unpack('!I', data[:4])
        str_data = unpack(f'!{size}s', data[4:])
        mpint_data = int.from_bytes(*str_data, 'big', True)
        return cls((size, mpint_data))

    def encode(self):
        size, mpint_data = self.data
        return pack(f'I{size}s', size, mpint_data.to_bytes(size, 'big', True))

    def __len__(self):
        return 4+self.data[0]


class NameList(Datatype):
    @classmethod
    def decode(cls, data):
        size = unpack('!I', data[:4])
        packed_list_data = unpack(f'!{size}s', data[4:])
        unpacked_list_data = packed_list_data[0].split(b',', -1)
        return cls((size, unpacked_list_data))

    def encode(self):
        size, unpacked_list_data = self.data
        packed_list_data = b','.join(unpacked_list_data)
        return pack(f'!I{size}s', size, packed_list_data)

    def __len__(self):
        return 4+self.data[0]

