import unittest
import socket
from test_helpers import TestHelpers
import time


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
    def setUp(self):
        self.test_udp_sender = TestSender()
        self.test_udp_listener = TestReceiver("0.0.0.0", 50001)
        self.test_udp_listener_2 = TestReceiver("0.0.0.0", 51024)

    def tearDown(self):
        self.test_udp_sender.close()
        self.test_udp_listener.close()
        self.test_udp_listener_2.close()

    def test_sisl_received_not_wrapped(self):
        input = TestHelpers.get_example_control_header() + b'{name: !str "helpful_name", flag: !bool "false", count: !int "3"}'
        self.test_udp_sender.send(input, "emulator_diode_emulator_1", 40001)
        response = TestHelpers.wait_for_action(lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=input), "receive udp")
        self.assertTrue(response, input)

    def test_non_sisl_is_wrapped(self):
        input = TestHelpers.get_example_control_header() + b'hello'
        self.test_udp_sender.send(input, "emulator_diode_emulator_1", 40001)
        response = TestHelpers.wait_for_action(lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=b"\xd1\xdf\x5f\xff"), "receive udp")
        self.assertEqual(response[64:68], b"\xd1\xdf\x5f\xff")

    def test_bitmap_not_wrapped(self):
        bitmap_sample = b'BM6\x03\x00\x00\x00\x00\x00\x00\x00\x00\x10\x12\x00\x00\xa0\x0f\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x00\x03\x00\x00'
        input = TestHelpers.get_example_control_header() + bitmap_sample
        self.test_udp_sender.send(input, "emulator_diode_emulator_1", 40001)
        response = TestHelpers.wait_for_action(lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=input), "receive udp")
        self.assertEqual(response, input)

    def test_send_with_valid_control_header_is_received(self):
        input = TestHelpers.get_example_control_header() + b"{}"
        self.test_udp_sender.send(input, "emulator_diode_emulator_1", 40001)
        response = TestHelpers.wait_for_action(lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=input), "receive udp")
        self.assertEqual(len(response), 114)

    def test_frame_dropped_if_invalid_header(self):
        input = TestHelpers.get_bad_example_control_header() + b'hello'
        self.assertRaises(socket.timeout,
                          TestHelpers.wait_for_action,
                          lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=input),
                          "receive udp")

    def test_frame_dropped_if_no_header(self):
        input = b'hello'
        self.assertRaises(socket.timeout,
                          TestHelpers.wait_for_action,
                          lambda: TestHelpers.read_udp_msg(self.test_udp_listener.sock, expected_output=input),
                          "receive udp")


if __name__ == '__main__':
    unittest.main()