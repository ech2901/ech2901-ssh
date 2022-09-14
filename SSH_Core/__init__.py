from struct import pack, unpack, error
from typing import Any


class Datatype(object):
    """
    Base class representation of a datatype used by ssh protocol
    """

    data: Any
    size: int

    def __len__(self) -> int:
        """
        Return the total length of the object that gets encoded
        :return:
        """
        return self.size

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        pass

    @classmethod
    def decode(cls, data: bytes):
        """
        Unpack a bytes object so that it's data can be stored
        :param data: bytes
        :return: Datatype subclass
        """
        pass

    def hex(self) -> str:
        """
        Return hex representation of the data in a string
        :return: string representation of the data (IE: 0xDEADBEEF)
        """
        return f'0x{int.from_bytes(self.encode(), "big"):0{len(self)}X}'

    def __repr__(self) -> str:
        """
        Return a string representation of the data
        :return: "Dataclass(data=self.data, len=self.size)"
        """
        out = f'{self.__class__.__name__}({self.data=}, {self.size=})'
        return out


class Byte(Datatype):
    def __init__(self, data: bytes):
        """
        Create a Byte representation for ssh protocol.
        Does not have to be ASCII formatted.
        :param data: bytes Required
        """
        if type(data) is bytes:
            self.size = len(data)
            self.data = data
        else:
            raise TypeError(f'data is not bytes, is {type(data)}')

    @classmethod
    def decode(cls, data: bytes):
        """
        unpack a bytes object so that it's data can be stored as a bytes object
        :param data: bytes
        :return: Byte instance
        """
        byte_data, _ = unpack(f'!{len(data)}s', data)
        return cls(byte_data)

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        return pack(f'!{self.size}s', self.data)


class Boolean(Datatype):
    def __init__(self, data: bool):
        """
        Create a Boolean representation for ssh protocol.
        This can only ever be True or False
        :param data: bool Required
        """
        if type(data) is bool:
            self.size = 1
            self.data = data
        else:
            raise TypeError(f'data is not bool, is {type(data)}')

    @classmethod
    def decode(cls, data):
        """
        unpack a bytes object so that it's data can be stored as a bool object
        :param data: bytes
        :return: Boolean instance
        """
        bool_data, _ = unpack('!?', data)
        return cls(bool_data)

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        Booleans can only ever be encoded as b'\x00' or b'\x01' for False an True respectively.
        :return: bytes
        """
        if type(self.data) is bool:
            return b'\x01' if self.data else b'\x00'
        raise error


class UInt32(Datatype):
    def __init__(self, data: int):
        """
        Create a UInt32 representation for ssh protocol.
        data cant only be a positive integer that is at most 32 bits.
        :param data: int Required
        """
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
        """
        unpack a bytes object so that it's data can be stored as an int object
        unpacking the data as an unsigned long int ( 4 bytes of data )
        :param data: bytes
        :return: UInt32 instance
        """
        uint_data, _ = unpack('!I', data)
        return cls(uint_data)

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        return pack('!I', self.data)


class UInt64(Datatype):
    def __init__(self, data: int):
        """
        Create a UInt64 representation for ssh protocol.
        data cant only be a positive integer that is at most 64 bits.
        :param data: int Required
        """
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
        """
        unpack a bytes object so that it's data can be stored as an int object
        unpacking the data as an unsigned long long int ( 8 bytes of data )
        :param data: bytes
        :return: UInt64 instance
        """
        uint_data, _ = unpack('!Q', data)
        return cls(uint_data)

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        return pack('!Q', self.data)


class String(Datatype):
    def __init__(self, data: str):
        """
        Create a String representation for ssh protocol.
        data cant only be a str object
        :param data: str Required
        """
        if type(data) is str:
            self.str_size = len(data)
            self.size = 4+self.str_size
            self.data = data
        else:
            raise TypeError(f'data is not str, is {type(data)}')

    @classmethod
    def decode(cls, data):
        """
        unpack a bytes object so that it's data can be stored as an str object
        The first 4 bytes are the length of the string.
        Then, bytes 5 through [size] is the actual string data.
        The max size is 4,294,967,295 characters
        :param data: bytes
        :return: String instance
        """
        size = unpack('!I', data[:4])
        string_data, _ = unpack(f'!{size}s', data[4:])
        return cls(string_data.decode())

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        return pack(f'!I{self.str_size}s', self.str_size, self.data.encode())


class MPInt(Datatype):
    def __init__(self, data: int):
        """
        Create a MPInt representation for ssh protocol.
        data can only be an int, signed or unsigned.
        The max size is up to 4,294,967,295 bytes long
        :param data: str Required
        """
        if type(data) is int:
            self.data_size = (data.bit_length()+7)//8
            self.size = self.data_size+4
            self.data = data
        else:
            raise TypeError(f'data is not int, is {type(data)}')

    @classmethod
    def decode(cls, data):
        """
        unpack a bytes object so that it's data can be stored as an int object
        The first 4 bytes are the length of the int to unpack in bytes.
        Then, bytes 5 through [size] is the actual int data, with MSB signing the data.
        :param data: bytes
        :return: MPInt instance
        """
        size, _ = unpack('!I', data[:4])
        str_data, _ = unpack(f'!{size}s', data[4:])
        mpint_data = int.from_bytes(str_data, 'big', signed=True)
        return cls(mpint_data)

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        return pack(
            f'I{self.data_size}s',
            self.data_size,
            self.data.to_bytes(self.data_size, 'big', signed=True)
        )


class NameList(Datatype):
    def __init__(self, *data):
        """
        Create a NameList representation for ssh protocol.
        data can only be a list of strings.
        The total max size is up to 4,294,967,295 bytes long for all data with overhead.
        Overhead is caused by commas (,) to seperate the strings.
        :param data: *str Required
        """
        for index, str_data in enumerate(data):
            if type(str_data) is not str:
                raise TypeError(f'data[{index}] is not str, is {type(str_data)}')
        self.data = data

        self.data_size = len(','.join(self.data))
        self.size = 4+self.data_size

    @classmethod
    def decode(cls, data):
        """
        unpack a bytes object so that it's data can be stored as an list object
        The first 4 bytes are the length of the data to unpack in bytes.
        Then, bytes 5 through [size] is the actual data.
        That data must be ASCII compatible and comma (,) separated strings.
        :param data: bytes
        :return: NameList instance
        """
        size, _ = unpack('!I', data[:4])
        packed_list_data, _ = unpack(f'!{size}s', data[4:])
        unpacked_list_data = packed_list_data.decode().split(',', -1)
        return cls(*unpacked_list_data)

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        data = ','.join(self.data).encode()
        return pack(f'!I{self.data_size}s', self.data_size, data)



