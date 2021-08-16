# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
from verify_bitmap import VerifyBitmap


class VerifyBitmapTests(unittest.TestCase):
    def test_bitmap_contains_valid_header(self):
        bitmap_sample = b'BM\x3A\x00\x00\x00'
        self.assertTrue(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_throws_with_invalid_header(self):
        bitmap_sample = b'BC\x3A\x00\x00\x00'
        self.assertFalse(VerifyBitmap.validate(bitmap_sample))

    def test_valid_file_size_uses_correct_bytes_in_header(self):
        bitmap_sample = b'BM\x3A\x00\x00\x00'
        self.assertTrue(VerifyBitmap.validate(bitmap_sample))


if __name__ == '__main__':
    unittest.main()
