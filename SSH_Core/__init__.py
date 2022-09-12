from struct import pack, unpack, error


class Datatype(object):

    def __len__(self):
        return self.size

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
            self.size = len(data)
            self.data = data
        else:
            raise TypeError(f'data is not bytes, is {type(data)}')

    @classmethod
    def decode(cls, data: bytes):
        byte_data, _ = unpack(f'!{len(data)}s', data)
        return cls(byte_data)

    def encode(self):
        return pack(f'!{self.size}s', self.data)


class Boolean(Datatype):
    def __init__(self, data: bool):
        if type(data) is bool:
            self.size = 1
            self.data = data
        else:
            raise TypeError(f'data is not bool, is {type(data)}')

    @classmethod
    def decode(cls, data):
        bool_data, _ = unpack('!?', data)
        return cls(bool_data)

    def encode(self):
        if type(self.data) is bool:
            return pack('!?', self.data)
        raise error


class UInt32(Datatype):
    def __init__(self, data: int):
        if type(data) is int:
            if data < 0:
                raise ValueError(f'data is less than 0: {data}')
            if data.bit_length() > 32:
                raise ValueError(f'data is more than 32 bits: {data} Bits: {data.bit_length()}')
            self.size = 4
            self.data = data
        else:
            raise TypeError(f'data is not int, is {type(data)}')

    @classmethod
    def decode(cls, data):
        uint_data, _ = unpack('!I', data)
        return cls(uint_data)

    def encode(self):
        return pack('!I', self.data)


class UInt64(Datatype):
    def __init__(self, data: int):
        if type(data) is int:
            if data < 0:
                raise ValueError(f'data is less than 0: {data}')
            if data.bit_length() > 64:
                raise ValueError(f'data is more than 64 bits: {data} Bits: {data.bit_length()}')
            self.size = 8
            self.data = data
        else:
            raise TypeError(f'data is not int, is {type(data)}')

    @classmethod
    def decode(cls, data):
        uint_data, _ = unpack('!Q', data)
        return cls(uint_data)

    def encode(self):
        return pack('!Q', self.data)


class String(Datatype):
    def __init__(self, data: str):
        if type(data) is str:
            self.str_size = len(data)
            self.size = 4+self.str_size
            self.data = data
        else:
            raise TypeError(f'data is not str, is {type(data)}')

    @classmethod
    def decode(cls, data):
        size = unpack('!I', data[:4])
        string_data, _ = unpack(f'!{size}s', data[4:])
        return cls(string_data.decode())

    def encode(self):
        return pack(f'!I{self.str_size}s', self.str_size, self.data.encode())


class MPInt(Datatype):
    def __init__(self, data: int):
        if type(data) is int:
            self.int_byte_size = (data.bit_length()+7)//8
            self.size = self.int_byte_size+4
            self.data = data
        else:
            raise TypeError(f'data is not int, is {type(data)}')

    @classmethod
    def decode(cls, data):
        size, _ = unpack('!I', data[:4])
        str_data, _ = unpack(f'!{size}s', data[4:])
        mpint_data = int.from_bytes(str_data, 'big', signed=True)
        return cls(mpint_data)

    def encode(self):
        return pack(
            f'I{self.int_byte_size}s',
            self.int_byte_size,
            self.data.to_bytes(self.int_byte_size, 'big', signed=True)
        )


class NameList(Datatype):
    def __init__(self, *data, size: int=None):
        for index, str_data in enumerate(data):
            if type(str_data) is not str:
                raise TypeError(f'data[{index}] is not str, is {type(str_data)}')
        self.data = data

        if type(size) is int:
            if size < 0:
                raise ValueError(f'size is less than 0, is {size}')
            if size.bit_length() > 32:
                raise ValueError(f'size is more than 32 bits, is {size.bit_length()} bits')
            self.data_size = size
        elif type(size) is not None:
            raise TypeError(f'size is not None or int, is {type(size)}')
        else:
            self.data_size = len(','.join(self.data))

        self.size = 4+self.data_size

    @classmethod
    def decode(cls, data):
        size, _ = unpack('!I', data[:4])
        packed_list_data, _ = unpack(f'!{size}s', data[4:])
        unpacked_list_data = packed_list_data.decode().split(',', -1)
        return cls(unpacked_list_data)

    def encode(self):
        data = ','.join(self.data).encode()
        return pack(f'!I{self.data_size}s', self.data_size, data)



