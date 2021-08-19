# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import construct


class VerifyBitmap:
    @staticmethod
    def validate(bitmap):
        try:
            VerifyBitmap._check_valid_bitmap_header(bitmap)
            return VerifyBitmap._check_bitmap_size(bitmap) and VerifyBitmap._check_bits_per_pixel(bitmap) and VerifyBitmap._check_bitmap_dimensions(bitmap)
        except InvalidBitmapHeaderError:
            return False

    @staticmethod
    def _check_valid_bitmap_header(data):
        try:
            VerifyBitmap._bitmap_header_bytes().parse(data)
        except construct.core.ConstructError:
            raise InvalidBitmapHeaderError("Invalid bitmap header")

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

    @staticmethod
    def _check_bitmap_size(data):
        return VerifyBitmap._get_bitmap_header_field_by_name(data, "BF_Size") == len(data)

    @staticmethod
    def _get_bitmap_header_field_by_name(data, field):
        return VerifyBitmap._bitmap_header_bytes().parse(data).search(field)

    @staticmethod
    def _check_bits_per_pixel(data):
        return VerifyBitmap._get_bitmap_header_field_by_name(data, "Bits_Per_Pixel") in [16, 24, 32]

    @staticmethod
    def _check_bitmap_dimensions(data):
        width_pixels = VerifyBitmap._get_bitmap_header_field_by_name(data, "Bitmap_Width")
        height_pixels = VerifyBitmap._get_bitmap_header_field_by_name(data, "Bitmap_Height")
        bits_per_pixel = VerifyBitmap._get_bitmap_header_field_by_name(data, "Bits_Per_Pixel")
        header_and_pixel_array_size_bytes = VerifyBitmap._get_bitmap_header_field_by_name(data, "BF_Size")

        array_dimensions_bytes = (width_pixels * height_pixels * bits_per_pixel) / 8
        header_size_bytes = 54
        return header_and_pixel_array_size_bytes == (array_dimensions_bytes + header_size_bytes)



class InvalidBitmapHeaderError(Exception):
    pass
