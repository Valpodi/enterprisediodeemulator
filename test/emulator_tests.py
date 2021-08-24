# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import string
import subprocess
import unittest
import random

from test_helpers import TestHelpers, TestSender, TestReceiver


class EmulatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run("python3 Emulator/launch_emulator.py".split())
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 41024, "zvu")

    def setUp(self):
        self.test_udp_sender = TestSender()
        self.test_udp_listener = TestReceiver("0.0.0.0", 50001)
        self.test_udp_listener_2 = TestReceiver("0.0.0.0", 51024)

    def tearDown(self):
        self.test_udp_sender.close()
        self.test_udp_listener.close()
        self.test_udp_listener_2.close()

    @classmethod
    def tearDownClass(cls):
        subprocess.run("docker stop emulator".split())
        subprocess.run("docker rm emulator".split())

    def test_data_received(self):
        self.test_udp_sender.send(b"1234", "172.17.0.1", 40001)
        self.assertEqual(self.test_udp_listener.recv(), b"1234")

    def test_data_received_one_destination_repeated(self):
        self.test_udp_sender.send(b"abcd", "172.17.0.1", 40001)
        self.assertEqual(self.test_udp_listener.recv(), b"abcd")
        self.test_udp_sender.send(b"1234", "172.17.0.1", 40001)
        self.assertEqual(self.test_udp_listener.recv(), b"1234")

    def test_data_received_two_destinations(self):
        self.test_udp_sender.send(b"abcd", "172.17.0.1", 41024)
        self.test_udp_sender.send(b"1234", "172.17.0.1", 40001)
        self.assertEqual(self.test_udp_listener_2.recv(), b"abcd")
        self.assertEqual(self.test_udp_listener.recv(), b"1234")

    def test_recv_9k_bytes(self):
        data = bytes(''.join(random.choice(string.ascii_letters) for i in range(9000)), 'utf-8')
        self.test_udp_sender.send(data, "172.17.0.1", 40001)
        self.assertEqual(data, self.test_udp_listener.recv())


if __name__ == '__main__':
    unittest.main()
