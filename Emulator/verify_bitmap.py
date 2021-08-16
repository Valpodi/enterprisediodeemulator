# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file
import construct


class VerifyBitmap:
    def validate(self, bitmap):
        return self._check_valid_bitmap_header(bitmap)

    def _check_valid_bitmap_header(self, data):
        return self._check_type(data)

    @staticmethod
    def _check_type(data):
        if data[:2] == b'BM':
            return True
        return False
