# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
import copy
from verify_bitmap import VerifyBitmap


class VerifyBitmapTests(unittest.TestCase):
    bitmap_header_as_dict = dict(Type=b'\x42\x4D',
                                 BF_Size=b'\x00\x00\x00\x00',
                                 Reserved_1=b'\x00\x00',
                                 Reserved_2=b'\x00\x00',
                                 Pixel_Array_Offset=b'\x00\x00\x00\x00',
                                 Header_Size=b'\x28\x00\x00\x00',
                                 Bitmap_Width=b'\x10\x00\x00\x00',
                                 Bitmap_Height=b'\x10\x00\x00\x00',
                                 Colour_Plane_Count=b'\x01\x00',
                                 Compression_Method=b'\x00\x00\x00\x00',
                                 Color_Used=b'\x00\x00\x00\x00',
                                 Important_Color=b'\x00\x00\x00\x00'
                                 )

    def test_bitmap_contains_valid_header(self):
        bitmap_sample = b"".join(self.bitmap_header_as_dict.values())
        self.assertTrue(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_returns_false_with_invalid_type_bytes(self):
        invalid_type_header = copy.deepcopy(self.bitmap_header_as_dict)
        invalid_type_header["Type"] = b'\x41\x4D'
        bitmap_sample = b"".join(invalid_type_header.values())
        self.assertFalse(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_returns_false_with_invalid_reserved_1_bytes(self):
        invalid_reserved_1_header = copy.deepcopy(self.bitmap_header_as_dict)
        invalid_reserved_1_header["Reserved_1"] = b'\x3A\x00'
        bitmap_sample = b"".join(invalid_reserved_1_header.values())
        self.assertFalse(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_returns_false_with_invalid_pixel_array_offset_bytes(self):
        invalid_pixel_array_offset_bytes_header = copy.deepcopy(self.bitmap_header_as_dict)
        invalid_pixel_array_offset_bytes_header["Pixel_Array_Offset"] = b'\x36\x00'
        bitmap_sample = b"".join(invalid_pixel_array_offset_bytes_header.values())
        self.assertFalse(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_returns_false_with_invalid_header_size(self):
        invalid_header_size_header = copy.deepcopy(self.bitmap_header_as_dict)
        invalid_header_size_header["Header_Size"] = b'\x18\x00\x00\x00'
        bitmap_sample = b"".join(invalid_header_size_header.values())
        self.assertFalse(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_returns_false_with_invalid_colour_plane_count(self):
        invalid_colour_plane_count_header = copy.deepcopy(self.bitmap_header_as_dict)
        invalid_colour_plane_count_header["Colour_Plane_Count"] = b'\x00\x00'
        bitmap_sample = b"".join(invalid_colour_plane_count_header.values())
        self.assertFalse(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_returns_false_with_header_file_size_not_equal_to_data_length(self):
        bitmap_sample = b"".join(self.bitmap_header_as_dict.values()) + b'hello'
        self.assertFalse(VerifyBitmap.validate(bitmap_sample))

    def test_bitmap_validate_returns_true_with_non_empty_bitmap_data(self):
        header = copy.deepcopy(self.bitmap_header_as_dict)
        header["BF_Size"] = b'\x05\x00\x00\x00'
        bitmap_sample = b"".join(header.values()) + b'hello'
        self.assertTrue(VerifyBitmap.validate(bitmap_sample))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(VerifyBitmapTests)
    unittest.TextTestRunner(verbosity=100).run(SUITE)
