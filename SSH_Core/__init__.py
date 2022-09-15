from struct import pack, unpack, error
from typing import Any

# TODO: add unit tests for math operations


class Datatype(object):
    """
    Base class representation of a datatype used by ssh protocol
    """

    data: Any

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
        data = self.encode()
        return f'0x{int.from_bytes(data, "big"):0{len(data)}X}'

    def __repr__(self) -> str:
        """
        Return a string representation of the data
        :return: "Dataclass(data=self.data, len=self.size)"
        """
        out = f'{self.__class__.__name__}(data={self.data})'
        return out

    def __int__(self):
        return int.from_bytes(self.encode(), 'big')

    def __sub__(self, other):
        return int(self)-int(other)

    def __add__(self, other):
        return int(self)+int(other)

    def __eq__(self, other):
        return int(self) == int(other)

    def __hash__(self):
        return int(self)


class Byte(Datatype):
    def __init__(self, data: bytes):
        """
        Create a Byte representation for ssh protocol.
        Does not have to be ASCII formatted.
        :param data: bytes Required
        """
        if type(data) is bytes:
            self.data = data
        else:
            raise TypeError(f'data is not bytes, is {type(data)}')

    @classmethod
    def decode(cls, data: bytes, size: int = 1):
        """
        unpack a bytes object so that it's data can be stored as a bytes object
        optional size int to describe how many byes should be consumed
        :param data: bytes
        :param size: int
        :return: Byte instance
        """
        if type(data) is bytes:
            if size == -1:
                byte_data = unpack(f'!{len(data)}s', data)
                return cls(*byte_data), b''
            byte_data = unpack(f'!{size}s', data[0:size])
            return cls(*byte_data), data[size:]
        else:
            raise TypeError(f'type of data is not bytes, is {type(data)}')

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        if type(self.data) is bytes:
            return pack(f'!{len(self.data)}s', self.data)
        raise error(f'data is not bytes, is {type(self.data)}')

    @classmethod
    def __class_getitem__(cls, size):
        class SizedByte(cls):
            @classmethod
            def decode(sub_cls, data: bytes):
                return cls.decode(data, size)

        return SizedByte

class Boolean(Datatype):
    def __init__(self, data: bool):
        """
        Create a Boolean representation for ssh protocol.
        This can only ever be True or False
        :param data: bool Required
        """
        if type(data) is bool:
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
        bool_data = unpack('!?', data[0:1])
        return cls(*bool_data), data[1:]

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        Booleans can only ever be encoded as b'\x00' or b'\x01' for False an True respectively.
        :return: bytes
        """
        if type(self.data) is bool:
            return b'\x01' if self.data else b'\x00'
        raise error(f'data is not bool, is {type(self.data)}')


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
        uint_data = unpack('!I', data[:4])
        return cls(*uint_data), data[4:]

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        if type(self.data) is int:
            return pack('!I', self.data)
        else:
            raise error(f'data is not int, is {type(self.data)}')

    def __int__(self):
        return self.data


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
        uint_data = unpack('!Q', data[:8])
        return cls(*uint_data), data[8:]

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        if type(self.data) is int:
            return pack('!Q', self.data)
        else:
            raise error(f'data is not int, is {type(self.data)}')

    def __int__(self):
        return self.data


class String(Datatype):
    def __init__(self, data: str):
        """
        Create a String representation for ssh protocol.
        data cant only be a str object
        :param data: str Required
        """
        if type(data) is str:
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
        string_data = unpack(f'!{size[0]}s', data[4:4+size[0]])
        return cls(string_data[0].decode()), data[4+size[0]:]

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        if type(self.data) is str:
            data_size = len(self.data)
            return pack(f'!I{data_size}s', data_size, self.data.encode())
        raise error(f'data is not str, is {type(self.data)}')


class MPInt(Datatype):
    def __init__(self, data: int):
        """
        Create a MPInt representation for ssh protocol.
        data can only be an int, signed or unsigned.
        The max size is up to 4,294,967,295 bytes long
        :param data: str Required
        """
        if type(data) is int:
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
        size = unpack('!I', data[:4])
        str_data = unpack(f'!{size[0]}s', data[4:4+size[0]])
        mpint_data = int.from_bytes(str_data[0], 'big', signed=True)
        return cls(mpint_data), data[4+size[0]:]

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """

        if type(self.data) is int:

            data_size = (self.data.bit_length()+7)//8
            if self.data.bit_length() % 8 == 0:
                data_size = data_size+1

            return pack(
                f'!I{data_size}s',
                data_size,
                self.data.to_bytes(data_size, 'big', signed=True)
            )
        else:
            raise error(f'data is not int, is {type(self.data)}')

    def __int__(self):
        return self.data


class NameList(Datatype):
    def __init__(self, *data):
        """
        Create a NameList representation for ssh protocol.
        data can only be a list of strings.
        The total max size is up to 4,294,967,295 bytes long for all data with overhead.
        Overhead is caused by commas (,) to separate the strings.
        :param data: *str Required
        """
        for index, str_data in enumerate(data):
            if type(str_data) is not str:
                raise TypeError(f'data[{index}] is not str, is {type(str_data)}')
        self.data = data

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
        size = unpack('!I', data[:4])
        if size[0]:
            packed_list_data = unpack(f'!{size[0]}s', data[4:4+size[0]])
            unpacked_list_data = packed_list_data[0].decode().split(',', -1)
            return cls(*unpacked_list_data), data[4+size[0]:]
        return cls(), data[4:]

    def encode(self) -> bytes:
        """
        Encode the data into a bytes object for transmission
        :return: bytes
        """
        try:
            data = ','.join(self.data).encode()
            data_size = len(data)
            return pack(f'!I{data_size}s', data_size, data)
        except:
            raise error
