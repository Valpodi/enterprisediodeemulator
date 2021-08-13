# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
from verify_bitmap import VerifyBitmap


class VerifyBitmapTests(unittest.TestCase):
    def test_bitmap_contains_valid_header(self):
        bitmap_sample = b'BM6\x03\x00\x00\x00\x00\x00\x00\x00\x00\x10\x12\x00\x00\xa0\x0f\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x00\x03\x00\x00'
        self.assertTrue(VerifyBitmap.validate(bitmap_sample))


if __name__ == '__main__':
    unittest.main()
