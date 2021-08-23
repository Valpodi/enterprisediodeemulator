# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import construct


class VerifyControlHeader:
    @staticmethod
    def validate(frame):
        return VerifyControlHeader._check_valid_control_header(frame) and \
            VerifyControlHeader._check_EOF(frame) and \
            VerifyControlHeader._check_frame_count(frame)

    @staticmethod
    def _check_valid_control_header(data):
        try:
            VerifyControlHeader._control_header_bytes().parse(data)
            return True
        except construct.core.ConstructError:
            return False

    @staticmethod
    def _control_header_bytes():
        return construct.Struct("Session_Id" / construct.Int32ul,
                                "Frame_Count" / construct.Int32ul,
                                "EOF" / construct.Int8ul,
                                "Padding" / construct.Array(103, construct.Const(b'\x00')))

    @staticmethod
    def _check_EOF(data):
        return VerifyControlHeader._get_bitmap_header_field_by_name(data, "EOF") in [0, 1]

    @staticmethod
    def _check_frame_count(data):
        return VerifyControlHeader._get_bitmap_header_field_by_name(data, "Frame_Count") > 0

    @staticmethod
    def _get_bitmap_header_field_by_name(data, field):
        return VerifyControlHeader._control_header_bytes().parse(data).search(field)
