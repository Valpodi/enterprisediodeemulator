# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import construct


class VerifyControlHeader:
    @staticmethod
    def validate(bitmap):
        try:
            VerifyControlHeader._check_valid_control_header(bitmap)
            return True
        except InvalidControlHeaderError:
            return False

    @staticmethod
    def _check_valid_control_header(data):
        try:
            VerifyControlHeader._control_header_bytes().parse(data)
        except construct.core.ConstructError:
            raise InvalidControlHeaderError("Invalid bitmap header")

    @staticmethod
    def _control_header_bytes():
        return construct.Struct("Frame_Count" / construct.Int32ul,
                                "EOF" / construct.Const(b'\x01'),
                                "Padding" / construct.Const(103*b'\x00'))

    @staticmethod
    def _get_bitmap_header_field_by_name(data, field):
        return VerifyControlHeader._control_header_bytes().parse(data).search(field)


class InvalidControlHeaderError(Exception):
    pass
