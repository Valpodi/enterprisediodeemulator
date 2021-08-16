# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file
import construct

#
# class VerifyBitmap:
#     def validate(self, bitmap):
#         return self._check_valid_bitmap_header(bitmap)
#
#     def _check_valid_bitmap_header(self, data):
#         return self._check_type(data)
#
#     @staticmethod
#     def _check_type(data):
#         if data[:2] == b'BM':
#             return True
#         return False


class VerifyBitmap:
    @staticmethod
    def validate(bitmap):
        return VerifyBitmap._check_valid_bitmap_header(bitmap)

    @staticmethod
    def _check_valid_bitmap_header(data):
        try:
            VerifyBitmap._bitmap_header_bytes().parse(data)
            return True
        except construct.core.ConstructError as e:
            return False

    @staticmethod
    def _bitmap_header_bytes():
        return construct.Struct("Type" / construct.Const(b'BM'),
                                "BF Size" / construct.Int32ub)