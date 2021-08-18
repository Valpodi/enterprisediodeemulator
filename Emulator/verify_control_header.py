# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import construct


class VerifyControlHeader:
    @staticmethod
    def validate(bitmap):
        try:
            VerifyControlHeader._check_valid_control_header(bitmap)
        except InvalidControlHeaderError:
            return False

        return VerifyControlHeader._check_EOF(bitmap)

    @staticmethod
    def _check_valid_control_header(data):
        try:
            struct = VerifyControlHeader._control_header_bytes()
            struct.parse(data)
        except construct.core.ConstructError:
            raise InvalidControlHeaderError("Invalid bitmap header")

    @staticmethod
    def _control_header_bytes():
        return construct.Struct("Frame_Count" / construct.Int32ul,
                                "EOF" / construct.Int8ul,
                                "Padding" / construct.Array(103, construct.Const(b'\x00')))

    @staticmethod
    def _check_EOF(data):
        eof_byte = VerifyControlHeader._get_bitmap_header_field_by_name(data, "EOF")
        return eof_byte == 0 or eof_byte == 1

    @staticmethod
    def _get_bitmap_header_field_by_name(data, field):
        return VerifyControlHeader._control_header_bytes().parse(data).search(field)


class InvalidControlHeaderError(Exception):
    pass
