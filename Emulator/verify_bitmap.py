# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import construct
import struct


class VerifyBitmap:
    @staticmethod
    def validate(bitmap):
        try:
            VerifyBitmap._check_valid_bitmap_header(bitmap)
            return VerifyBitmap._check_bitmap_size(bitmap)
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
        return construct.Struct("Type" / construct.Const(b'\x4D\x42'),
                                "BF_Size" / construct.Int32ub,
                                "Reserved_1" / construct.Const(b'\x00\x00'),
                                "Reserved_2" / construct.Const(b'\x00\x00'),
                                "Pixel_Array_Offset" / construct.Int32ub,
                                "Header_Size" / construct.Const(b'\x00\x00\x00\x28'),
                                "Bitmap_Width" / construct.Int32ub,
                                "Bitmap_Height" / construct.Int32ub,
                                "Colour_Plane_Count" / construct.Const(b'\x00\x01'),
                                "Compression_Method" / construct.Int32ub,
                                "Color_Used" / construct.Int32ub,
                                "Important_Color" / construct.Int32ub)

    @staticmethod
    def _check_bitmap_size(data):
        header_size_bytes = VerifyBitmap._get_bitmap_header_field_by_name(data, "Header_Size")
        header_size_int = int(header_size_bytes.hex(), base=16)
        return VerifyBitmap._get_bitmap_header_field_by_name(data, "BF_Size") == len(data[header_size_int:])

    @staticmethod
    def _get_bitmap_header_field_by_name(data, field):
        return VerifyBitmap._bitmap_header_bytes().parse(data).search(field)


class InvalidBitmapHeaderError(Exception):
    pass
