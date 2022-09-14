import unittest
import SSH_Core
import random

from struct import error as StructError

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
                    self.fail()

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
                    self.fail()

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

if __name__ == '__main__':
    unittest.main()
