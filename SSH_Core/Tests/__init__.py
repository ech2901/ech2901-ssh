import unittest
import SSH_Core
import random

from struct import error as StructError

random_tests_count = 100


class Byte(unittest.TestCase):
    bad_data = (True, False, None, 'test', 100, 0.03, float('inf'), list(), dict(), object)

    def generate_test_data(self):
        self.test_data = list()
        for _ in range(random_tests_count):
            self.test_data.append(random.randbytes(random.randint(0, 30)))

    def testInstances(self):
        self.generate_test_data()
        for data in self.test_data:
            with self.subTest(data):
                SSH_Core.Byte(data)

    def testDecode(self):
        self.generate_test_data()
        for data in self.test_data:
            with self.subTest(f'decode: {data}'):
                inst = SSH_Core.Byte.decode(data)
                with self.subTest(f'check data integrity: {data}'):
                    self.assertEqual(inst.data, data)

    def testEncode(self):
        self.generate_test_data()
        for data in self.test_data:
            inst = SSH_Core.Byte(data)
            with self.subTest(f'encode from: {inst.data}'):
                self.assertEqual(data, inst.encode())

    def testDecodeEncode(self):
        self.generate_test_data()
        for data in self.test_data:
            inst = SSH_Core.Byte.decode(data)
            with self.subTest(f'Test decode then encode: {data}'):
                self.assertEqual(inst.encode(), data)

    def testEncodeDecode(self):
        self.generate_test_data()
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
        self.generate_test_data()
        for data in self.bad_data:
            inst = SSH_Core.Byte(b'')
            inst.data = data
            with self.subTest(f'Expect fail: instance data set to {data}'):
                self.assertRaises(StructError, inst.encode)



if __name__ == '__main__':
    unittest.main()
