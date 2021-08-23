# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
import copy
from verify_control_header import VerifyControlHeader


class VerifyControlHeaderTests(unittest.TestCase):
    control_header_as_dict = dict(Session_Id=b'\x01\x00\x00\x00',
                                  Frame_Count=b'\x01\x00\x00\x00',
                                  EOF=b'\x00',
                                  Padding=103*b'\x00'
                                  )

    def test_data_contains_valid_header(self):
        data_sample = b"".join(self.control_header_as_dict.values()) + b"\x00"
        self.assertTrue(VerifyControlHeader().validate(data_sample))

    def test_control_header_returns_false_with_invalid_frame_count(self):
        invalid_frame_count_header = copy.deepcopy(self.control_header_as_dict)
        invalid_frame_count_header["Frame_Count"] = b'\x00\x00\x00\x00'
        data_sample = b"".join(invalid_frame_count_header.values())
        self.assertFalse(VerifyControlHeader().validate(data_sample))

    def test_control_header_returns_false_with_invalid_EOF(self):
        invalid_eof_header = copy.deepcopy(self.control_header_as_dict)
        invalid_eof_header["EOF"] = b'\x02'
        data_sample = b"".join(invalid_eof_header.values())
        self.assertFalse(VerifyControlHeader().validate(data_sample))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(VerifyControlHeaderTests)
    unittest.TextTestRunner(verbosity=100).run(SUITE)
