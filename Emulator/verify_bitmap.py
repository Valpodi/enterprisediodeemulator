# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import construct


class VerifyBitmap:
    @staticmethod
    def validate(bitmap):
        try:
            VerifyBitmap._check_valid_bitmap_header(bitmap)
            return VerifyBitmap._check_bitmap_size(bitmap) and VerifyBitmap._check_compression_method(bitmap)
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
                                "BF_Size" / construct.Int32ul,
                                "Reserved_1" / construct.Const(b'\x00\x00'),
                                "Reserved_2" / construct.Const(b'\x00\x00'),
                                "Pixel_Array_Offset" / construct.Int32ul,
                                "Header_Size" / construct.Const(b'\x28\x00\x00\x00'),
                                "Bitmap_Width" / construct.Int32ul,
                                "Bitmap_Height" / construct.Int32ul,
                                "Colour_Plane_Count" / construct.Const(b'\x01\x00'),
                                "Compression_Method" / construct.Int32ul,
                                "Color_Used" / construct.Int32ul,
                                "Important_Color" / construct.Int32ul)

    @staticmethod
    def _check_bitmap_size(data):
        header_size_bytes = VerifyBitmap._get_bitmap_header_field_by_name(data, "Header_Size")
        header_size_int = int.from_bytes(header_size_bytes, byteorder='little')
        return VerifyBitmap._get_bitmap_header_field_by_name(data, "BF_Size") == len(data[header_size_int:])

    @staticmethod
    def _get_bitmap_header_field_by_name(data, field):
        return VerifyBitmap._bitmap_header_bytes().parse(data).search(field)

    @staticmethod
    def _check_compression_method(data):
        return VerifyBitmap._get_bitmap_header_field_by_name(data, "Compression_Method") <= 6


class InvalidBitmapHeaderError(Exception):
    pass
