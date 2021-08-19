# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
import socket
import copy
from test_helpers import TestHelpers


class TestSender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.data = b""

    def send(self, data, ip, port):
        self.sock.sendto(data, (ip, port))

    def close(self):
        self.sock.close()


class TestReceiver:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.sock.settimeout(5)
        self.data = b""

    def recv(self):
        data, addr = self.sock.recvfrom(9000)
        return data

    def close(self):
        self.sock.close()


class EmulatorTests(unittest.TestCase):
    bitmap_header_as_dict = dict(
        # File header
        Type=b'\x42\x4D',
        BF_Size=b'\x36\x00\x00\x00',
        Reserved_1=b'\x00\x00',
        Reserved_2=b'\x00\x00',
        Pixel_Array_Offset=b'\x36\x00\x00\x00',
        # DIB Header
        Header_Size=b'\x28\x00\x00\x00',
        Bitmap_Width=b'\x00\x00\x00\x00',
        Bitmap_Height=b'\x00\x00\x00\x00',
        Colour_Plane_Count=b'\x01\x00',
        Bits_Per_Pixel=b'\x20\x00',
        Compression_Method=b'\x00\x00\x00\x00',
        Bitmap_Size_In_Bytes=b'\x00\x00\x00\x00',  # not checked
        Horizontal_Resolution_In_Pixels_Per_Meter=b'\x00\x00\x00\x00',  # not checked
        Vertical_Resolution_In_Pixels_Per_Meter=b'\x00\x00\x00\x00',  # not checked
        Color_Used=b'\x00\x00\x00\x00',
        Important_Color=b'\x00\x00\x00\x00',
    )

    def setUp(self):
        self.test_udp_sender = TestSender()
        self.test_udp_listener = TestReceiver("0.0.0.0", 50001)
        self.test_udp_listener_2 = TestReceiver("0.0.0.0", 51024)

    def tearDown(self):
        self.test_udp_sender.close()
        self.test_udp_listener.close()
        self.test_udp_listener_2.close()

    def test_sisl_received_not_wrapped(self):
        input_data = TestHelpers.get_valid_control_header() + b'{name: !str "helpful_name", flag: !bool "false", count: !int "3"}'
        self.test_udp_sender.send(input_data, "emulator_diode_emulator_1", 40001)
        response = TestHelpers.wait_for_action(
            lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=input_data), "receive udp")
        self.assertTrue(response, input_data)

    def test_non_sisl_is_wrapped(self):
        input_data = TestHelpers.get_valid_control_header() + b'hello'
        self.test_udp_sender.send(input_data, "emulator_diode_emulator_1", 40001)
        response = TestHelpers.wait_for_action(
            lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=b"\xd1\xdf\x5f\xff"),
            "receive udp")
        self.assertEqual(response[64:68], b"\xd1\xdf\x5f\xff")

    def test_bitmap_not_wrapped(self):
        bitmap_header = copy.deepcopy(self.bitmap_header_as_dict)
        bitmap_header["Bitmap_Width"] = b'\x01\x00\x00\x00'
        bitmap_header["Bitmap_Height"] = b'\x01\x00\x00\x00'
        bitmap_header["BF_Size"] = b'\x3A\x00\x00\x00'

        bitmap_sample = b"".join(bitmap_header.values()) + b'jive'
        input_data = TestHelpers.get_valid_control_header() + bitmap_sample
        self.test_udp_sender.send(input_data, "emulator_diode_emulator_1", 40001)
        response = TestHelpers.wait_for_action(
            lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=input_data), "receive udp")
        self.assertEqual(response, input_data)

    def test_send_valid_sisl_with_valid_control_header_is_received(self):
        input_data = TestHelpers.get_valid_control_header() + b"{}"
        self.test_udp_sender.send(input_data, "emulator_diode_emulator_1", 40001)
        response = TestHelpers.wait_for_action(
            lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=input_data), "receive udp")
        self.assertEqual(len(response), 114)

    def test_frame_dropped_if_invalid_header(self):
        input_data = TestHelpers.get_invalid_control_header() + b"{}"
        self.test_udp_sender.send(input_data, "emulator_diode_emulator_1", 40001)
        self.assertRaises(socket.timeout,
                          TestHelpers.wait_for_action,
                          lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=input_data),
                          "receive udp")

    def test_frame_dropped_if_no_header(self):
        input_data = b'hello'
        self.test_udp_sender.send(input_data, "emulator_diode_emulator_1", 40001)
        self.assertRaises(socket.timeout,
                          TestHelpers.wait_for_action,
                          lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=input_data),
                          "receive udp")


if __name__ == '__main__':
    unittest.main()
