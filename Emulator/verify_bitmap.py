# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file
import math

import construct


class VerifyBitmap:
    accepted_bits_per_pixel = [16, 24, 32]
    file_and_dib_header_size_in_bytes = 54

    def validate(self, bitmap):
        return self._check_valid_bitmap_header(bitmap) and \
               self._check_bitmap_size(bitmap) and \
               self._check_bits_per_pixel() and \
               self._check_bitmap_dimensions()

    def _check_valid_bitmap_header(self, data):
        try:
            self.header = self._bitmap_header_bytes().parse(data)
            return True
        except construct.core.ConstructError:
            return False

    @staticmethod
    def _bitmap_header_bytes():
        return construct.Struct("Type" / construct.Const(b'\x42\x4D'),
                                "BF_Size" / construct.Int32ul,  # File Header (14) + DIB Header (40) + Pixel Array
                                "Reserved_1" / construct.Const(b'\x00\x00'),
                                "Reserved_2" / construct.Const(b'\x00\x00'),
                                "Pixel_Array_Offset" / construct.Const(b'\x36\x00\x00\x00'),

                                "Header_Size" / construct.Const(b'\x28\x00\x00\x00'),
                                "Bitmap_Width" / construct.Int32ul,
                                "Bitmap_Height" / construct.Int32ul,
                                "Colour_Plane_Count" / construct.Const(b'\x01\x00'),
                                "Bits_Per_Pixel" / construct.Int16ul,
                                "Compression_Method" / construct.Const(b'\x00\x00\x00\x00'),
                                "Bitmap_Size_In_Bytes" / construct.Int32ul,
                                "Horizontal_Resolution_In_Pixels_Per_Meter" / construct.Int32ul,
                                "Vertical_Resolution_In_Pixels_Per_Meter" / construct.Int32ul,
                                "Color_Used" / construct.Const(b'\x00\x00\x00\x00'),
                                "Important_Color" / construct.Const(b'\x00\x00\x00\x00'))

    def _check_bitmap_size(self, data):
        return self._get_bitmap_header_field_by_name("BF_Size") == len(data)

    def _get_bitmap_header_field_by_name(self, field):
        return self.header.search(field)

    def _check_bits_per_pixel(self):
        return self._get_bitmap_header_field_by_name("Bits_Per_Pixel") in self.accepted_bits_per_pixel

    def _check_bitmap_dimensions(self):
        width_pixels = self._get_bitmap_header_field_by_name("Bitmap_Width")
        height_pixels = self._get_bitmap_header_field_by_name("Bitmap_Height")
        bytes_per_pixel = self._get_bitmap_header_field_by_name("Bits_Per_Pixel") / 8
        header_and_pixel_array_size_bytes = self._get_bitmap_header_field_by_name("BF_Size")

        array_dimensions_bytes = width_pixels * height_pixels * bytes_per_pixel
        return header_and_pixel_array_size_bytes == (array_dimensions_bytes + self.file_and_dib_header_size_in_bytes)
