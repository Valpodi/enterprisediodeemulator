import string
import unittest
import socket
import random
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
    @classmethod
    def setUpClass(cls):
        TestHelpers.wait_for_open_comms_ports()

    def setUp(self):
        self.test_udp_sender = TestSender()
        self.test_udp_listener = TestReceiver("0.0.0.0", 50001)
        self.test_udp_listener_2 = TestReceiver("0.0.0.0", 51024)

    def tearDown(self):
        self.test_udp_sender.close()
        self.test_udp_listener.close()
        self.test_udp_listener_2.close()

    def test_data_received(self):
        self.test_udp_sender.send(b"1234", "emulator_diode_emulator_1", 40001)
        self.assertEqual(self.test_udp_listener.recv(), b"1234")

    def test_data_received_one_destination_repeated(self):
        self.test_udp_sender.send(b"abcd", "emulator_diode_emulator_1", 40001)
        self.assertEqual(self.test_udp_listener.recv(), b"abcd")
        self.test_udp_sender.send(b"1234", "emulator_diode_emulator_1", 40001)
        self.assertEqual(self.test_udp_listener.recv(), b"1234")

    def test_data_received_two_destinations(self):
        self.test_udp_sender.send(b"abcd", "emulator_diode_emulator_1", 41024)
        self.test_udp_sender.send(b"1234", "emulator_diode_emulator_1", 40001)
        self.assertEqual(self.test_udp_listener_2.recv(), b"abcd")
        self.assertEqual(self.test_udp_listener.recv(), b"1234")

    def test_recv_9k_bytes(self):
        data = bytes(''.join(random.choice(string.ascii_letters) for i in range(9000)), 'utf-8')
        self.test_udp_sender.send(data, "emulator_diode_emulator_1", 40001)
        self.assertEqual(data, self.test_udp_listener.recv())


if __name__ == '__main__':
    unittest.main()
