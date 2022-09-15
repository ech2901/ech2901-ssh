import collections
import unittest
import SSH_Core
import random

from struct import error as StructError, pack
from string import printable

random_tests_count = 100


class Byte(unittest.TestCase):
    bad_data = (True, False, None, 'test', 100, 0.03, float('inf'), list(), dict(), object)

    @property
    def test_data(self):
        for _ in range(random_tests_count):
            yield random.randbytes(random.randint(0, 30))

    def testInstances(self):
        for data in self.test_data:
            with self.subTest(data):
                SSH_Core.Byte(data)

    def testDecode(self):
        for data in self.test_data:
            with self.subTest(f'decode: {data}'):
                try:
                    inst, _ = SSH_Core.Byte.decode(data, -1)
                    with self.subTest(f'check data integrity: {data}'):
                        self.assertEqual(inst.data, data)
                except:
                    self.fail(data)

    def testDecodeOversized(self):
        for data in self.test_data:
            size = random.randint(0, len(data))
            with self.subTest(f'decode {size} bytes of {data}'):
                inst, consumed_data = SSH_Core.Byte.decode(data, size)
                self.assertEqual(inst.data, data[:size])
                self.assertEqual(consumed_data, data[size:])

    def testEncode(self):
        for data in self.test_data:
            inst = SSH_Core.Byte(data)
            with self.subTest(f'encode from: {inst.data}'):
                self.assertEqual(data, inst.encode())

    def testDecodeEncode(self):
        for data in self.test_data:
            inst, _ = SSH_Core.Byte.decode(data, -1)
            with self.subTest(f'Test decode then encode: {data}'):
                self.assertEqual(inst.encode(), data)

    def testEncodeDecode(self):
        for data in self.test_data:
            inst1 = SSH_Core.Byte(data)
            inst2, _ = SSH_Core.Byte.decode(inst1.encode(), -1)
            with self.subTest(f'Test encode then decode: {data}'):
                self.assertEqual(inst2.data, data)

    def testInstanceFail(self):
        for data in self.bad_data:
            with self.subTest(f'Expect fail: attempt to instance {data}'):
                self.assertRaises(TypeError, SSH_Core.Byte, data)

    def testDecodeFail(self):
        for data in self.bad_data:
            with self.subTest(f'Expect fail: attempt to decode {data}'):
                self.assertRaises(TypeError, SSH_Core.Byte.decode, data, -1)

    def testEncodeFail(self):
        for data in self.bad_data:
            inst = SSH_Core.Byte(b'')
            inst.data = data
            with self.subTest(f'Expect fail: instance data set to {data}'):
                self.assertRaises(StructError, inst.encode)


class Boolean(unittest.TestCase):
    bad_data = (None, 1, 0, -1, 0.5, 'test', b'', list, dict())
    test_data = [val.to_bytes(1, 'big') for val in range(256)]

    def testInstances(self):
        for data in (True, False):
            with self.subTest(data):
                SSH_Core.Boolean(data)

    def testDecode(self):
        for data in self.test_data:
            with self.subTest(f'Test decode: {data}'):
                try:
                    inst, _ = SSH_Core.Boolean.decode(data)
                    with self.subTest(f'Test truth: {data}'):
                        if data == b'\x00':
                            self.assertFalse(inst.data)
                        else:
                            self.assertTrue(inst.data)
                except:
                    self.fail(data)

    def testDecodeOversized(self):
        for data in self.test_data:
            data = data+random.randbytes(4)
            with self.subTest(f'Test decode: {data}'):
                try:
                    inst, consumed_data = SSH_Core.Boolean.decode(data)
                    with self.subTest(f'Test truth: {data}'):
                        if data[0:1] == b'\x00':
                            self.assertFalse(inst.data)
                            self.assertEqual(consumed_data, data[1:])
                        else:
                            self.assertTrue(inst.data)
                            self.assertEqual(consumed_data, data[1:])
                except:
                    self.fail(data)



    def testEncode(self):
        for data in (True, False):
            inst = SSH_Core.Boolean(data)
            with self.subTest(f'Encoding: {data}'):
                if data:
                    self.assertEqual(inst.encode(), b'\x01')
                else:
                    self.assertEqual(inst.encode(), b'\x00')

    def testDecodeEncode(self):
        for data in self.test_data:
            inst, _ = SSH_Core.Boolean.decode(data)
            with self.subTest(f'Decoding then encoding: {data}'):
                if data == b'\x00':
                    self.assertEqual(inst.encode(), b'\x00')
                else:
                    self.assertEqual(inst.encode(), b'\x01')

    def testEncodeDecode(self):
        for data in (True, False):
            inst1 = SSH_Core.Boolean(data)
            inst2, _ = SSH_Core.Boolean.decode(inst1.encode())
            with self.subTest(f'Encoding then decoding: {data}'):
                self.assertEqual(inst2.data, data)

    def testInstanceFail(self):
        for data in self.bad_data:
            with self.subTest(f'Fail instance with: {data}'):
                self.assertRaises(TypeError, SSH_Core.Boolean, data)

    def testDecodeFail(self):
        for data in self.bad_data:
            with self.subTest(f'Fail decode with: {data}'):
                if type(data) is bytes:
                    self.assertRaises(StructError, SSH_Core.Boolean.decode, data)
                else:
                    self.assertRaises(TypeError, SSH_Core.Boolean.decode, data)

    def testEncodeFail(self):
        for data in (b'', b'\x01\x00', b'test', *self.bad_data):
            inst = SSH_Core.Boolean(True)
            inst.data = data
            with self.subTest(f'Fail encode with: {data}'):
                self.assertRaises(StructError, inst.encode)


class UInt32(unittest.TestCase):
    bad_data = (1 << 33, -1, 0.5, True, False, None, object, list(), dict(), b'', b'1', 'test')

    @property
    def test_data(self):
        for _ in range(random_tests_count):
            data = random.randbytes(4)
            yield data, int.from_bytes(data, 'big')

    def testInstances(self):
        for _, data in self.test_data:
            with self.subTest(data):
                SSH_Core.UInt32(data)

    def testDecode(self):
        for data, test_val in self.test_data:
            try:
                inst, _ = SSH_Core.UInt32.decode(data)
                with self.subTest(f'Decode: {data}'):
                    self.assertEqual(inst.data, test_val)
            except:
                self.fail(data)

    def testDecodeOversized(self):
        for data, test_val in self.test_data:
            data = data+random.randbytes(4)
            try:
                inst, consumed_data = SSH_Core.UInt32.decode(data)
                with self.subTest(f'Decode: {data}'):
                    self.assertEqual(inst.data, test_val)
                    self.assertEqual(consumed_data, data[4:])
            except:
                self.fail(data)

    def testEncode(self):
        for test_val, data in self.test_data:
            inst = SSH_Core.UInt32(data)
            with self.subTest(f'Encode: {data}'):
                self.assertEqual(inst.encode(), test_val)

    def testDecodeEncode(self):
        for data, _ in self.test_data:
            inst, _ = SSH_Core.UInt32.decode(data)
            with self.subTest(f'Decoding than encoding: {data}'):
                self.assertEqual(inst.encode(), data)

    def testEncodeDecode(self):
        for _, data in self.test_data:
            inst1 = SSH_Core.UInt32(data)
            inst2, _ = SSH_Core.UInt32.decode(inst1.encode())
            with self.subTest(f'Encoding than decoding: {data}'):
                self.assertEqual(inst2.data, data)

    def testInstanceFail(self):
        for data in self.bad_data:
            with self.subTest(f'Fail instance with: {data}'):
                if type(data) is int and (data < 0 or data.bit_length() > 32):
                    self.assertRaises(ValueError, SSH_Core.UInt32, data)
                else:
                    self.assertRaises(TypeError, SSH_Core.UInt32, data)

    def testDecodeFail(self):
        for data in (b'', b'asd', *self.bad_data):
            with self.subTest(f'Fail decode with: {data}'):
                if type(data) is bytes:
                    self.assertRaises(StructError, SSH_Core.UInt32.decode, data)
                else:
                    self.assertRaises(TypeError, SSH_Core.UInt32.decode, data)

    def testEncodeFail(self):
        for data in self.bad_data:
            inst = SSH_Core.UInt32(0)
            inst.data = data
            with self.subTest(f'Fail encode with: {data}'):
                self.assertRaises(StructError, inst.encode)


class UInt64(unittest.TestCase):
    bad_data = (1 << 65, -1, 0.5, True, False, None, object, list(), dict(), b'', b'1', 'test')

    @property
    def test_data(self):
        for _ in range(random_tests_count):
            data = random.randbytes(8)
            yield data, int.from_bytes(data, 'big')

    def testInstances(self):
        for _, data in self.test_data:
            with self.subTest(data):
                SSH_Core.UInt64(data)

    def testDecode(self):
        for data, test_val in self.test_data:
            try:
                inst, _ = SSH_Core.UInt64.decode(data)
                with self.subTest(f'Decode: {data}'):
                    self.assertEqual(inst.data, test_val)
            except:
                self.fail(data)

    def testDecodeOversized(self):
        for data, test_val in self.test_data:
            data = data+random.randbytes(4)
            try:
                inst, consumed_data = SSH_Core.UInt64.decode(data)
                with self.subTest(f'Decode: {data}'):
                    self.assertEqual(inst.data, test_val)
                    self.assertEqual(consumed_data, data[8:])
            except:
                self.fail(data)

    def testEncode(self):
        for test_val, data in self.test_data:
            inst = SSH_Core.UInt64(data)
            with self.subTest(f'Encode: {data}'):
                self.assertEqual(inst.encode(), test_val)

    def testDecodeEncode(self):
        for data, _ in self.test_data:
            inst, _ = SSH_Core.UInt64.decode(data)
            with self.subTest(f'Decoding than encoding: {data}'):
                self.assertEqual(inst.encode(), data)

    def testEncodeDecode(self):
        for _, data in self.test_data:
            inst1 = SSH_Core.UInt64(data)
            inst2, _ = SSH_Core.UInt64.decode(inst1.encode())
            with self.subTest(f'Encoding than decoding: {data}'):
                self.assertEqual(inst2.data, data)

    def testInstanceFail(self):
        for data in self.bad_data:
            with self.subTest(f'Fail instance with: {data}'):
                if type(data) is int and (data < 0 or data.bit_length() > 32):
                    self.assertRaises(ValueError, SSH_Core.UInt64, data)
                else:
                    self.assertRaises(TypeError, SSH_Core.UInt64, data)

    def testDecodeFail(self):
        for data in (b'', b'asd', *self.bad_data):
            with self.subTest(f'Fail decode with: {data}'):
                if type(data) is bytes:
                    self.assertRaises(StructError, SSH_Core.UInt64.decode, data)
                else:
                    self.assertRaises(TypeError, SSH_Core.UInt64.decode, data)

    def testEncodeFail(self):
        for data in self.bad_data:
            inst = SSH_Core.UInt64(0)
            inst.data = data
            with self.subTest(f'Fail encode with: {data}'):
                self.assertRaises(StructError, inst.encode)


class String(unittest.TestCase):
    bad_data = (-1, 0, 1, b'test', True, False, None, list(), dict(), object)

    @property
    def corrupt_data(self):
        for _ in range(random_tests_count):
            size = random.randint(1, 256)
            data = ''.join(random.sample(3*printable, size))
            yield pack(f'!I{size}s', size+1, data.encode())

    @property
    def test_data(self):
        for _ in range(random_tests_count):
            size = random.randint(0, 256)
            data = ''.join(random.sample(3*printable, size))
            byte_data = pack(f'!I{size}s', size, data.encode())
            yield byte_data, data

    def testInstances(self):
        for _, data in self.test_data:
            with self.subTest(data):
                SSH_Core.String(data)

    def testDecode(self):
        for data, test_val in self.test_data:
            with self.subTest(f'Decoding: {data}'):
                inst, _ = SSH_Core.String.decode(data)
                self.assertEqual(inst.data, test_val)

    def testDecodeOversized(self):
        for data, test_val in self.test_data:
            data = data+random.randbytes(4)
            size = int.from_bytes(data[0:4], 'big')

            with self.subTest(f'Decoding: {data}'):
                inst, consumed_data = SSH_Core.String.decode(data)
                self.assertEqual(inst.data, test_val)
                self.assertEqual(consumed_data, data[4+size:])

    def testEncode(self):
        for test_val, data, in self.test_data:
            with self.subTest(f'Encoding: {data}'):
                inst = SSH_Core.String(data)
                self.assertEqual(inst.encode(), test_val)

    def testDecodeEncode(self):
        for data, _ in self.test_data:
            inst, _ = SSH_Core.String.decode(data)
            with self.subTest(f'Decoding then encoding: {data}'):
                self.assertEqual(inst.encode(), data)

    def testEncodeDecode(self):
        for _, data in self.test_data:
            inst1 = SSH_Core.String(data)
            inst2, _ = SSH_Core.String.decode(inst1.encode())
            with self.subTest(f'Encoding then decoding: {data}'):
                self.assertEqual(inst2.data, data)

    def testInstanceFail(self):
        for data in self.bad_data:
            with self.subTest(f'Fail instance with: {data}'):
                self.assertRaises(TypeError, SSH_Core.String, data)

    def testDecodeFail(self):
        for data in self.corrupt_data:
            with self.subTest(f'Fail decode with: {data}'):
                self.assertRaises(StructError, SSH_Core.String.decode, data)

    def testEncodeFail(self):
        for data in self.bad_data:
            inst = SSH_Core.String('')
            inst.data = data
            with self.subTest(f'Fail encode with: {data}'):
                self.assertRaises(StructError, inst.encode)


class MPInt(unittest.TestCase):
    bad_data = (True, False, None, 0.5, 'test', b'test2', b'', b'3', tuple(), object)

    @property
    def pos_test_data(self):
        for _ in range(random_tests_count):
            data = random.randint(0, 10_000)

            if data >= 0 and data.bit_length() % 8 == 0:
                size = 1+(data.bit_length()+7)//8
            else:
                size = (data.bit_length()+7)//8

            byte_data = data.to_bytes(size, 'big', signed=True)

            yield pack(f'!I{size}s', size, byte_data), data

    @property
    def neg_test_data(self):
        for _ in range(random_tests_count):
            data = -random.randint(1, 10_000)

            if data.bit_length() % 8 == 0:
                size = 1+(data.bit_length()+7)//8
            else:
                size = (data.bit_length()+7)//8

            byte_data = data.to_bytes(size, 'big', signed=True)

            yield pack(f'!I{size}s', size, byte_data), data

    @property
    def test_data(self):
        for byte_data, data in self.pos_test_data:
            yield byte_data, data
        for byte_data, data in self.neg_test_data:
            yield byte_data, data

    @property
    def corrupt_data(self):
        for byte_data, _ in self.test_data:
            size = int.from_bytes(byte_data[:4], 'big')
            yield (size+1).to_bytes(4, 'big') + byte_data[4:]


    def testInstances(self):
        for _, data in self.test_data:
            with self.subTest(data):
                SSH_Core.MPInt(data)

    def testDecode(self):
        for data, test_val in self.test_data:
            with self.subTest(f'Decoding: {data}'):
                inst, _ = SSH_Core.MPInt.decode(data)
                self.assertEqual(inst.data, test_val)

    def testDecodeOversized(self):
        for data, test_val in self.test_data:
            data = data+random.randbytes(4)
            size = int.from_bytes(data[0:4], 'big')
            with self.subTest(f'Decoding: {data}'):
                inst, consumed_data = SSH_Core.MPInt.decode(data)
                self.assertEqual(inst.data, test_val)
                self.assertEqual(consumed_data, data[4+size:])

    def testEncode(self):
        for test_val, data, in self.test_data:
            with self.subTest(f'Encoding: {data}'):
                inst = SSH_Core.MPInt(data)
                self.assertEqual(inst.encode(), test_val)

    def testDecodeEncode(self):
        for data, _ in self.test_data:
            inst, _ = SSH_Core.MPInt.decode(data)
            with self.subTest(f'Decoding then encoding: {data}'):
                self.assertEqual(inst.encode(), data)

    def testEncodeDecode(self):
        for _, data in self.test_data:
            inst1 = SSH_Core.MPInt(data)
            inst2, _ = SSH_Core.MPInt.decode(inst1.encode())
            with self.subTest(f'Encoding then decoding: {data}'):
                self.assertEqual(inst2.data, data)

    def testInstanceFail(self):
        for data in self.bad_data:
            with self.subTest(f'Fail instance with: {data}'):
                self.assertRaises(TypeError, SSH_Core.MPInt, data)

    def testDecodeFail(self):
        for data in self.corrupt_data:
            with self.subTest(f'Fail decode with: {data}'):
                self.assertRaises(StructError, SSH_Core.MPInt.decode, data)

    def testEncodeFail(self):
        for data in self.bad_data:
            inst = SSH_Core.MPInt(0)
            inst.data = data
            with self.subTest(f'Fail encode with: {data}'):
                self.assertRaises(StructError, inst.encode)


class NameList(unittest.TestCase):
    bad_data = (None, 0, 1, -1, True, False, object, tuple(), list(), dict())

    @property
    def test_data(self):
        for _ in range(random_tests_count):
            count = random.randint(0, 10)
            data = list()
            for item in range(count):
                data.append(''.join(random.sample(3*printable.replace(',', '', -1), random.randint(0, 100))))
            size = len(','.join(data))
            if size:
                yield pack(f'!I{size}s', size, ','.join(data).encode()), tuple(data)
            else:
                yield pack(f'!I{size}s', size, ','.join(data).encode()), tuple()

    @property
    def corrupt_data(self):
        for byte_data, _ in self.test_data:
            size = int.from_bytes(byte_data[:4], 'big')
            yield (size+1).to_bytes(4, 'big') + byte_data[4:]

    def testInstances(self):
        for _, data in self.test_data:
            with self.subTest(data):
                SSH_Core.NameList(*data)

    def testDecode(self):
        for data, test_val in self.test_data:
            with self.subTest(f'Decoding: {data}'):
                inst, _ = SSH_Core.NameList.decode(data)
                self.assertEqual(inst.data, test_val)

    def testDecodeOversized(self):
        for data, test_val in self.test_data:
            data = data+random.randbytes(4)
            size = int.from_bytes(data[0:4], 'big')
            with self.subTest(f'Decoding: {data}'):
                inst, consumed_data = SSH_Core.NameList.decode(data)
                self.assertEqual(inst.data, test_val, test_val)
                self.assertEqual(consumed_data, data[4+size:])

    def testEncode(self):
        for test_val, data, in self.test_data:
            with self.subTest(f'Encoding: {data}'):
                inst = SSH_Core.NameList(*data)
                self.assertEqual(inst.encode(), test_val)

    def testDecodeEncode(self):
        for data, _ in self.test_data:
            inst, _ = SSH_Core.NameList.decode(data)
            with self.subTest(f'Decoding then encoding: {data}'):
                self.assertEqual(inst.encode(), data)

    def testEncodeDecode(self):
        for _, data in self.test_data:
            inst1 = SSH_Core.NameList(*data)
            inst2, _ = SSH_Core.NameList.decode(inst1.encode())
            with self.subTest(f'Encoding then decoding: {data}'):
                self.assertEqual(inst2.data, data)

    def testInstanceFail(self):
        for data in self.bad_data:
            with self.subTest(f'Fail instance with: {data}'):
                self.assertRaises(TypeError, SSH_Core.NameList, data)

    def testDecodeFail(self):
        for data in self.corrupt_data:
            with self.subTest(f'Fail decode with: {data}'):
                self.assertRaises(StructError, SSH_Core.NameList.decode, data)

    def testEncodeFail(self):
        for data in self.bad_data:
            inst = SSH_Core.NameList()
            inst.data = data
            with self.subTest(f'Fail encode with: {data}'):
                if type(data) in (list, tuple, set, dict):
                    self.skipTest(f'bad_data is a collection')
                self.assertRaises(StructError, inst.encode)

if __name__ == '__main__':
    unittest.main()
