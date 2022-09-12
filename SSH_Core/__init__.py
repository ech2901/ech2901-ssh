from struct import pack, unpack, error


class Datatype(object):

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
    def __init__(self, data: bytes):
        if type(data) is bytes:
            self.data = data
        else:
            raise ValueError

    @classmethod
    def decode(cls, data):
        byte_data = unpack(f'!{len(data)}s', data)
        return cls(*byte_data)

    def encode(self):
        return pack(f'!{len(self)}s', self.data)


class Boolean(Datatype):
    def __init__(self, data: bool):
        if type(data) is bool:
            self.data = data
        else:
            raise ValueError

    @classmethod
    def decode(cls, data):
        bool_data = unpack('!?', data)
        return cls(*bool_data)

    def encode(self):
        if type(self.data) is bool:
            return pack('!?', self.data)
        raise error

    def __len__(self):
        return 1


class UInt32(Datatype):
    def __init__(self, data: int):
        if type(data) is int:
            if data < 0:
                raise ValueError(f'Less than 0: {data}')
            if data.bit_length() > 32:
                raise ValueError(f'More than 32 bits: {data} Bits: {data.bit_length()}')
            self.data = data
        else:
            raise ValueError(f'Not an int: {data} Type: {type(data)}')

    @classmethod
    def decode(cls, data):
        uint_data = unpack('!I', data)
        return cls(*uint_data)

    def encode(self):
        return pack('!I', self.data)

    def __len__(self):
        return 4


class UInt64(Datatype):
    def __init__(self, data: int):
        if type(data) is int:
            if data < 0:
                raise ValueError
            if data.bit_length() > 64:
                raise ValueError
            self.data = data
        else:
            raise ValueError

    @classmethod
    def decode(cls, data):
        uint_data = unpack('!Q', data)
        return cls(*uint_data)

    def encode(self):
        return pack('!Q', self.data)

    def __len__(self):
        return 8


class String(Datatype):
    def __init__(self, data: bytes):
        if type(data) is bytes:
            self.data = data.decode()
        else:
            raise ValueError

    @classmethod
    def decode(cls, data):
        size = unpack('!I', data[:4])
        string_data = unpack(f'!{size}s', data[4:])
        return cls(*string_data)

    def encode(self):
        return pack(f'!I{len(self)}s', len(self), self.data.encode())

    def __len__(self):
        return 4+len(self.data)


class MPInt(Datatype):
    def __init__(self, size: int, data: int):
        UInt32(size)  # Same tests needed, so initialize only to test
        self.size = size
        if ((data.bit_length() + 7) // 8) == size:
            self.data = data
        else:
            raise ValueError

    @classmethod
    def decode(cls, data):
        size, _ = unpack('!I', data[:4])
        str_data, _ = unpack(f'!{size}s', data[4:])
        mpint_data = int.from_bytes(str_data, 'big', True)
        return cls(size, mpint_data)

    def encode(self):
        return pack(f'I{self.size}s', self.size, self.data.to_bytes(self.size, 'big', True))

    def __len__(self):
        return 4+self.size


class NameList(Datatype):
    def __init__(self, size: int, data: list):
        UInt32(size)
        if isinstance(data, list):
            self.data = data
        else:
            raise ValueError

    @classmethod
    def decode(cls, data):
        size, _ = unpack('!I', data[:4])
        packed_list_data = unpack(f'!{size}s', data[4:])
        unpacked_list_data = packed_list_data[0].split(b',', -1)
        return cls(size, unpacked_list_data)

    def encode(self):
        size, unpacked_list_data = self.data
        packed_list_data = b','.join(unpacked_list_data)
        return pack(f'!I{size}s', size, packed_list_data)

    def __len__(self):
        return 4+self.data[0]

