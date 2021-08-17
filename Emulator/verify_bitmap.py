# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import construct


class VerifyBitmap:
    @staticmethod
    def validate(bitmap):
        try:
            VerifyBitmap._check_valid_bitmap_header(bitmap)
            return True
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
                                "BF Size" / construct.Int32ub,
                                "Reserved 1" / construct.Const(b'\x00\x00'),
                                "Reserved 2" / construct.Const(b'\x00\x00'),
                                "Pixel Array Offset" / construct.Int32ub,
                                "Header Size" / construct.Const(b'\x28\x00\x00\x00'),
                                "Bitmap Width" / construct.Int32ub,
                                "Bitmap Height" / construct.Int32ub,
                                "Colour Plane Count" / construct.Const(b'\x01\x00'),
                                "Compression Method" / construct.Int32ub,
                                "Color Used" / construct.Int32ub,
                                "Important Color" / construct.Int32ub)


class InvalidBitmapHeaderError(Exception):
    pass
