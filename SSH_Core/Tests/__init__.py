import unittest
import SSH_Core
import random

class TestDatatypes(unittest.TestSuite):
    pass


class TestByte(unittest.TestCase):



class TestBoolean(unittest.TestCase):
    def setUp(self):
        self.bool_inst = SSH_Core.Boolean(True)

    def test_data(self):
        self.assertTrue(self.bool_inst.data)
        self.assertIsNotNone(self.bool_inst.data)
        self.assertIsInstance(self.bool_inst.data, bool)

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



if __name__ == '__main__':
    datatypes = TestDatatypes()
    datatypes.addTest(TestBoolean)

    datatypes.run()