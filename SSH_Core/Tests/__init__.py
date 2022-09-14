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
                    inst = SSH_Core.Byte.decode(data)
                    with self.subTest(f'check data integrity: {data}'):
                        self.assertEqual(inst.data, data)
                except:
                    self.fail(data)

    def testEncode(self):
        for data in self.test_data:
            inst = SSH_Core.Byte(data)
            with self.subTest(f'encode from: {inst.data}'):
                self.assertEqual(data, inst.encode())

    def testDecodeEncode(self):
        for data in self.test_data:
            inst = SSH_Core.Byte.decode(data)
            with self.subTest(f'Test decode then encode: {data}'):
                self.assertEqual(inst.encode(), data)

    def testEncodeDecode(self):
        for data in self.test_data:
            inst1 = SSH_Core.Byte(data)
            inst2 = SSH_Core.Byte.decode(inst1.encode())
            with self.subTest(f'Test encode then decode: {data}'):
                self.assertEqual(inst2.data, data)

    def testInstanceFail(self):
        for data in self.bad_data:
            with self.subTest(f'Expect fail: attempt to instance {data}'):
                self.assertRaises(TypeError, SSH_Core.Byte, data)

    def testDecodeFail(self):
        for data in self.bad_data:
            with self.subTest(f'Expect fail: attempt to decode {data}'):
                self.assertRaises(TypeError, SSH_Core.Byte.decode, data)

    def testEncodeFail(self):
        for data in self.bad_data:
            inst = SSH_Core.Byte(b'')
            inst.data = data
            with self.subTest(f'Expect fail: instance data set to {data}'):
                self.assertRaises(StructError, inst.encode)


class Boolean(unittest.TestCase):
    bad_data = (None, 1, 0, -1, 0.5, 'test', b'test2', list, dict())
    test_data = [val.to_bytes(1, 'big') for val in range(256)]

    def testInstances(self):
        for data in (True, False):
            with self.subTest(data):
                SSH_Core.Boolean(data)

    def testDecode(self):
        for data in self.test_data:
            with self.subTest(f'Test decode: {data}'):
                try:
                    inst = SSH_Core.Boolean.decode(data)
                    with self.subTest(f'Test truth: {data}'):
                        if data == b'\x00':
                            self.assertFalse(inst.data)
                        else:
                            self.assertTrue(inst.data)
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
            inst = SSH_Core.Boolean.decode(data)
            with self.subTest(f'Decoding then encoding: {data}'):
                if data == b'\x00':
                    self.assertEqual(inst.encode(), b'\x00')
                else:
                    self.assertEqual(inst.encode(), b'\x01')

    def testEncodeDecode(self):
        for data in (True, False):
            inst1 = SSH_Core.Boolean(data)
            inst2 = SSH_Core.Boolean.decode(inst1.encode())
            with self.subTest(f'Encoding then decoding: {data}'):
                self.assertEqual(inst2.data, data)

    def testInstanceFail(self):
        for data in self.bad_data:
            with self.subTest(f'Fail instance with: {data}'):
                self.assertRaises(TypeError, SSH_Core.Boolean, data)

    def testDecodeFail(self):
        for data in (b'', b'\x01\x00', b'test', *self.bad_data):
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
    bad_data = (1<<33, -1, 0.5, True, False, None, object, list(), dict(), b'', b'1', 'test')

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
                inst = SSH_Core.UInt32.decode(data)
                with self.subTest(f'Decode: {data}'):
                    self.assertEqual(inst.data, test_val)
            except:
                self.fail(data)

    def testEncode(self):
        for test_val, data in self.test_data:
            inst = SSH_Core.UInt32(data)
            with self.subTest(f'Encode: {data}'):
                self.assertEqual(inst.encode(), test_val)

    def testDecodeEncode(self):
        for data, _ in self.test_data:
            inst = SSH_Core.UInt32.decode(data)
            with self.subTest(f'Decoding than encoding: {data}'):
                self.assertEqual(inst.encode(), data)

    def testEncodeDecode(self):
        for _, data in self.test_data:
            inst1 = SSH_Core.UInt32(data)
            inst2 = SSH_Core.UInt32.decode(inst1.encode())
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
        for data in (b'', b'asd', b'asdfg', *self.bad_data):
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
    bad_data = (1<<65, -1, 0.5, True, False, None, object, list(), dict(), b'', b'1', 'test')

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
                inst = SSH_Core.UInt64.decode(data)
                with self.subTest(f'Decode: {data}'):
                    self.assertEqual(inst.data, test_val)
            except:
                self.fail(data)

    def testEncode(self):
        for test_val, data in self.test_data:
            inst = SSH_Core.UInt64(data)
            with self.subTest(f'Encode: {data}'):
                self.assertEqual(inst.encode(), test_val)

    def testDecodeEncode(self):
        for data, _ in self.test_data:
            inst = SSH_Core.UInt64.decode(data)
            with self.subTest(f'Decoding than encoding: {data}'):
                self.assertEqual(inst.encode(), data)

    def testEncodeDecode(self):
        for _, data in self.test_data:
            inst1 = SSH_Core.UInt64(data)
            inst2 = SSH_Core.UInt64.decode(inst1.encode())
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
        for data in (b'', b'asd', b'asdffauyg', *self.bad_data):
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
                inst = SSH_Core.String.decode(data)
                self.assertEqual(inst.data, test_val)

    def testEncode(self):
        for test_val, data, in self.test_data:
            with self.subTest(f'Encoding: {data}'):
                inst = SSH_Core.String(data)
                self.assertEqual(inst.encode(), test_val)

    def testDecodeEncode(self):
        pass

    def testEncodeDecode(self):
        pass

    def testInstanceFail(self):
        pass

    def testDecodeFail(self):
        pass

    def testEncodeFail(self):
        pass


if __name__ == '__main__':
    unittest.main()
