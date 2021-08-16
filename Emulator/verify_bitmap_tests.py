# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
from verify_bitmap import VerifyBitmap


class VerifyBitmapTests(unittest.TestCase):
    def test_bitmap_contains_valid_header(self):
        bitmap_sample = b''.join([b'\x42\x4D', b'\x3A\x00\x00\x00', b'\x00\x00', b'\x00\x00',
                                  b'\x36\x00\x00\x00', b'\x28\x00\x00\x00', b'\x10\x00\x00\x00', b'\x10\x00\x00\x00'])
        self.assertTrue(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_throws_with_invalid_type_bytes(self):
        bitmap_sample = b''.join([b'\x41\x4D', b'\x3A\x00\x00\x00', b'\x00\x00', b'\x00\x00'])
        self.assertFalse(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_throws_with_invalid_reserved_1_bytes(self):
        bitmap_sample = b''.join([b'\x42\x4D', b'\x3A\x00\x00\x00', b'\x01\x00', b'\x00\x00'])

        self.assertFalse(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_throws_with_invalid_pixel_array_offset_bytes(self):
        bitmap_sample = b''.join([b'\x42\x4D', b'\x3A\x00\x00\x00', b'\x00\x00', b'\x00\x00',
                                  b'\x36\x00\x00'])
        self.assertFalse(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_throws_with_invalid_header_size(self):
        bitmap_sample = b''.join([b'\x42\x4D', b'\x3A\x00\x00\x00', b'\x00\x00', b'\x00\x00',
                                  b'\x36\x00\x00', b'\x27\x00\x00\x00'])
        self.assertFalse(VerifyBitmap.validate(bitmap_sample))


if __name__ == '__main__':
    unittest.main()
