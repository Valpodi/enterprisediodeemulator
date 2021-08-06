# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import copy
import unittest
import subprocess
import threading
import requests
import socket
import json
from test_helpers import TestHelpers


class TestSender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data, ip, port):
        self.sock.sendto(data, (ip, port))

    def close(self):
        self.sock.close()


class TestReceiver:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.sock.settimeout(1)

    def recv(self):
        data, addr = self.sock.recvfrom(9000)
        return data

    def close(self):
        self.sock.close()


class EndToEndEmulatorTests(unittest.TestCase):
    interface_server_thread = None
    valid_port_config = None

    @classmethod
    def setUpClass(cls):
        cls.start_interface_server_in_thread()
        cls.valid_port_config = TestHelpers.save_port_config()
        cls.update_port_config()
        try:
            TestHelpers.wait_for_open_comms_ports("172.17.0.1", 8081, "zv")
        except TimeoutError as ex:
            print(f"Exception during setUpClass: {ex}")
            cls.tearDownClass()
            raise

    @classmethod
    def start_interface_server_in_thread(cls):
        cls.interface_server_thread = threading.Thread(target=cls.start_interface_server, daemon=True)
        cls.interface_server_thread.start()

    @classmethod
    def start_interface_server(cls):
        subprocess.Popen('python3 Emulator/launch_management_interface.py --interfacePort 8081', shell=True)

    @classmethod
    def update_port_config(cls):
        new_port_config = copy.deepcopy(cls.valid_port_config)
        new_port_config["routingTable"][0]["egressIpAddress"] = "172.17.0.1"
        new_port_config["routingTable"][1]["egressIpAddress"] = "172.17.0.1"
        with open('Emulator/config/portConfig.json', 'w') as config_file:
            json.dump(new_port_config, config_file, indent=4)

    def tearDown(self):
        self.test_udp_sender.close()
        self.test_udp_listener.close()
        subprocess.run("docker stop emulator && docker rm emulator", shell=True)

    @classmethod
    def tearDownClass(cls):
        TestHelpers.reset_port_config_file(cls.valid_port_config)
        subprocess.run("docker stop management_interface", shell=True)
        cls.interface_server_thread.join()

    def setUp(self):
        self.test_udp_sender = TestSender()
        self.test_udp_listener = TestReceiver("0.0.0.0", 50001)
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 50001, "zvu")

    def test_data_received_matches_data_sent(self):
        requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001, "zvu")
        self.assertRaises(socket.timeout, TestHelpers.wait_for_action, lambda: (self.test_udp_listener.recv() != b"\x00", 0), "Non-empty packets received exceeded maximum")
        self.test_udp_sender.send(b"1234", "172.17.0.1", 40001)

        self.assertEqual(self.test_udp_listener.recv(), b"1234")
        requests.post("http://172.17.0.1:8081/api/command/diode/power/off")
        self.assertRaises(TimeoutError, TestHelpers.wait_for_open_comms_ports, "172.17.0.1", 40001, "zvu")


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(EndToEndEmulatorTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
