import unittest
import SSH_Core
import random

from struct import error

random_tests_count = 100


class TestByte(unittest.TestCase):
    def __init__(self, methodName: str):
        super().__init__(methodName)

        self.test_data = list()
        for i in range(random_tests_count):
            self.test_data.append(random.randbytes(i))

    def init_instances(self):
        self.test_instances = list()
        for index, data in enumerate(self.test_data):
            with self.subTest(f'{index}: {data}'):
                self.test_instances.append(SSH_Core.Byte(data))

    def test_instance_all_fail(self):
        test_types = [
            int,
            bool,
            str,
            bytearray,
            list,
            tuple,
            dict
        ]

        for test_type in test_types:
            with self.subTest(test_type.__name__):
                self.assertRaises(ValueError, SSH_Core.Byte, test_type())

    def test_data_integrity(self):
        self.init_instances()
        for index, data in enumerate(self.test_data):
            with self.subTest(f'{index}: {data}'):
                self.assertEqual(self.test_instances[index].data, data)

    def test_decode(self):
        self.init_instances()
        for index, data in enumerate(self.test_data):
            with self.subTest(f'{index}: {data}'):
                self.assertEqual(
                    self.test_instances[index].data,
                    SSH_Core.Byte.decode(data).data
                )

    def test_encode(self):
        self.init_instances()
        for index, data in enumerate(self.test_data):
            with self.subTest(f'{index}: {data}'):
                self.assertEqual(self.test_instances[index].encode(), data)

    def test_equivalence_encodeing(self):
        self.init_instances()
        for index, inst in enumerate(self.test_instances):
            with self.subTest(f'{index}: {inst.data}'):
                test_inst = SSH_Core.Byte.decode(inst.encode())
                self.assertEqual(test_inst.data, inst.data)

    def test_equivalence_decoding(self):
        for index, data in enumerate(self.test_data):
            with self.subTest(f'{index}: {data}'):
                test_inst = SSH_Core.Byte.decode(data)
                self.assertEqual(test_inst.encode(), data)


class TestBoolean(unittest.TestCase):

    def test_instances_all_fail(self):
        test_types = [
            int,
            str,
            bytes,
            bytearray,
            list,
            tuple,
            dict
        ]

        for test_type in test_types:
            with self.subTest(test_type.__name__):
                self.assertRaises(ValueError, SSH_Core.Boolean, test_type())

    def test_data(self):
        bool_inst = SSH_Core.Boolean(True)
        self.assertTrue(bool_inst.data)
        self.assertIsNotNone(bool_inst.data)
        self.assertIsInstance(bool_inst.data, bool)

    def test_decode(self):
        test_data = [
            (b'\x00', False),
            (b'\x01', True),
            (b't', True),
            (b' ', True)
        ]

        for testcase, passcase in test_data:
            with self.subTest(testcase):
                test_bool = SSH_Core.Boolean.decode(testcase)
                self.assertEqual(test_bool.data, passcase, test_bool.data)

    def test_encode(self):
        test_data = [
            (True, b'\01'),
            (False, b'\00')
        ]

        for testcase, passcase in test_data:
            with self.subTest(testcase):
                test_bool = SSH_Core.Boolean(testcase)
                self.assertEqual(test_bool.encode(), passcase)

    def test_equivalence_encoding(self):
        test_data = [True, False]
        for testcase in test_data:
            with self.subTest(testcase):
                bool_inst1 = SSH_Core.Boolean(testcase)
                bool_inst2 = SSH_Core.Boolean.decode(bool_inst1.encode())
                self.assertEqual(bool_inst2.data, bool_inst1.data)

    def test_equivalence_decoding(self):
        test_data = [
            b'\x00',
            b'\x01',
            b't',
            b' '
        ]

        for testcase in test_data:
            with self.subTest(testcase):
                bool_inst1 = SSH_Core.Boolean.decode(testcase)
                bool_inst2 = SSH_Core.Boolean.decode(bool_inst1.encode())
                self.assertEqual(bool_inst2.data, bool_inst1.data)


class TestUInt32(unittest.TestCase):
    int_max = (1 << 32)-1

    def test_instance_all_pass(self):
        """Test creating valid instances that we expect"""
        for _ in range(random_tests_count):
            test_val = random.randint(0, self.int_max)
            with self.subTest(test_val):
                SSH_Core.UInt32(test_val)

    def test_instances_all_fail1(self):
        """Test creating invallid instances with bad data types"""
        test_types = [
            bool,
            str,
            bytes,
            bytearray,
            list,
            tuple,
            dict
        ]

        for test_type in test_types:
            with self.subTest(test_type.__name__):
                self.assertRaises(ValueError, SSH_Core.UInt32, test_type())

    def test_instance_all_fail2(self):
        """Test creating invalid instances with bad data"""
        for _ in range(random_tests_count):
            test_val_pos = random.randint(0, self.int_max)+self.int_max
            test_val_neg = -random.randint(1, self.int_max)

            with self.subTest(test_val_pos):
                self.assertRaises(ValueError, SSH_Core.UInt32, test_val_pos)
            with self.subTest(test_val_neg):
                self.assertRaises(ValueError, SSH_Core.UInt32, test_val_neg)

    def test_decode_all_pass(self):
        """Test if decoding data returns expected values"""
        for _ in range(random_tests_count):
            test_int = random.randint(0, self.int_max)
            test_data = test_int.to_bytes(4, 'big')
            with self.subTest(f'{test_int}: {test_data}'):
                test_inst = SSH_Core.UInt32.decode(test_data)
                self.assertEqual(test_inst.data, test_int)

    def test_decode_all_fail(self):
        """Test if decoding invalid data raises an error"""
        for _ in range(random_tests_count):
            test_int1 = random.randint(0, self.int_max)
            test_data1 = test_int1.to_bytes(4+random.randint(1, 8), 'big')

            with self.subTest(f'{test_int1}: {test_data1}'):
                self.assertRaises(error, SSH_Core.UInt32.decode, test_data1)

    def test_enocode_all_pass(self):
        """Test if encoding data returns expected value"""
        for _ in range(random_tests_count):
            test_data = random.randint(0, self.int_max)
            test_inst = SSH_Core.UInt32(test_data)
            with self.subTest(f'{test_data}'):
                test_bytes = test_inst.encode()
                self.assertEqual(int.from_bytes(test_bytes, 'big'), test_data)

    def test_encode_all_fail(self):
        """Test if trying to encode invalid data raises an error"""
        for _ in range(random_tests_count):
            test_data = random.randint(0, self.int_max)
            test_inst = SSH_Core.UInt32(test_data)
            test_inst.data = test_data + self.int_max
            with self.subTest(f'{test_inst.data}'):
                self.assertRaises(error, test_inst.encode)

    def test_equivalence_encoding(self):
        """Test if decoding data from another instances encode function """\
            """doesn't malform the data"""
        for _ in range(random_tests_count):
            test_data = random.randint(0, self.int_max)
            test_inst = SSH_Core.UInt32.decode(SSH_Core.UInt32(test_data).encode())
            with self.subTest(test_data):
                self.assertEqual(test_inst.data, test_data)

    def test_equivalence_decoding(self):
        """Test if encoding data from another instances decode function """\
            """doesn't malform the data"""
        for _ in range(random_tests_count):
            test_data = random.randbytes(4)
            test_inst = SSH_Core.UInt32.decode(test_data).encode()
            with self.subTest(test_data):
                self.assertEqual(test_data, test_inst)



if __name__ == '__main__':
    unittest.main()
