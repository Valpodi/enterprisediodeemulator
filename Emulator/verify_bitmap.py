# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file


class VerifyBitmap:
    @staticmethod
    def validate(bitmap):
        return VerifyBitmap._verify_bitmap_type(bitmap)

    @staticmethod
    def _verify_bitmap_type(bitmap):
        return bitmap[:2] == b"BM"