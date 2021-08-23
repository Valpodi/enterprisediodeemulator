# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
import copy
from verify_bitmap import VerifyBitmap


class VerifyBitmapTests(unittest.TestCase):
    bitmap_header_as_dict = dict(Type=b'\x42\x4D',
                                 BF_Size=b'\x36\x00\x00\x00',
                                 Reserved_1=b'\x00\x00',
                                 Reserved_2=b'\x00\x00',
                                 Pixel_Array_Offset=b'\x36\x00\x00\x00',

                                 Header_Size=b'\x28\x00\x00\x00',
                                 Bitmap_Width=b'\x00\x00\x00\x00',
                                 Bitmap_Height=b'\x00\x00\x00\x00',
                                 Colour_Plane_Count=b'\x01\x00',
                                 Bits_Per_Pixel=b'\x20\x00',
                                 Compression_Method=b'\x00\x00\x00\x00',
                                 Bitmap_Size_In_Bytes=b'\x00\x00\x00\x00',
                                 Horizontal_Resolution_In_Pixels_Per_Meter=b'\x00\x00\x00\x00',
                                 Vertical_Resolution_In_Pixels_Per_Meter=b'\x00\x00\x00\x00',
                                 Color_Used=b'\x00\x00\x00\x00',
                                 Important_Color=b'\x00\x00\x00\x00',
                                 )

    def test_bitmap_contains_valid_header(self):
        bitmap_sample = b"".join(self.bitmap_header_as_dict.values())
        self.assertTrue(VerifyBitmap().validate(bitmap_sample))

    def test_bitmap_validate_returns_false_with_header_file_size_not_equal_to_data_length(self):
        bitmap_sample = b"".join(self.bitmap_header_as_dict.values()) + b'jive'
        self.assertFalse(VerifyBitmap().validate(bitmap_sample))

    def test_bitmap_validate_returns_true_with_header_file_size_equal_to_data_length(self):
        header = copy.deepcopy(self.bitmap_header_as_dict)
        header["Bitmap_Width"] = b'\x01\x00\x00\x00'
        header["Bitmap_Height"] = b'\x01\x00\x00\x00'
        header["BF_Size"] = b'\x3A\x00\x00\x00'
        bitmap_sample = b"".join(header.values()) + b'jive'
        self.assertTrue(VerifyBitmap().validate(bitmap_sample))

    def test_bitmap_validate_returns_false_with_invalid_bits_per_pixel(self):
        header = copy.deepcopy(self.bitmap_header_as_dict)
        header["Bits_Per_Pixel"] = b'\x19\x00'
        bitmap_sample = b"".join(header.values())
        self.assertFalse(VerifyBitmap().validate(bitmap_sample))

    def test_bitmap_validate_returns_false_with_invalid_bitmap_dimensions(self):
        header = copy.deepcopy(self.bitmap_header_as_dict)
        header["BF_Size"] = b'\x3A\x00\x00\x00'
        header["Bitmap_Width"] = b'\x02\x00\x00\x00'
        header["Bitmap_Height"] = b'\x01\x00\x00\x00'

        bitmap_sample = b"".join(header.values()) + b'jive'
        self.assertFalse(VerifyBitmap().validate(bitmap_sample))

    def test_bitmap_validate_returns_true_with_valid_bitmap_dimensions(self):
        header = copy.deepcopy(self.bitmap_header_as_dict)
        header["Bitmap_Width"] = b'\x01\x00\x00\x00'
        header["Bitmap_Height"] = b'\x01\x00\x00\x00'
        header["BF_Size"] = b'\x3A\x00\x00\x00'

        bitmap_sample = b"".join(header.values()) + b'jive'
        self.assertTrue(VerifyBitmap().validate(bitmap_sample))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(VerifyBitmapTests)
    unittest.TextTestRunner(verbosity=100).run(SUITE)
