# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import copy
import unittest
import subprocess
import threading
import requests
import socket
import json
from test_helpers import TestHelpers, TestSender, TestReceiver


class EndToEndEmulatorTests(unittest.TestCase):
    interface_server_thread = None
    valid_port_config = None
    config_filepath = 'Emulator/config/port_config.json'

    @classmethod
    def setUpClass(cls):
        cls.start_interface_server_in_thread()
        cls.valid_port_config = TestHelpers.read_port_config()
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
        subprocess.Popen('python3 Emulator/launch_management_interface.py --interfacePort 8081'.split())

    @classmethod
    def update_port_config(cls):
        new_port_config = copy.deepcopy(cls.valid_port_config)
        new_port_config["routingTable"][0]["egressIpAddress"] = "172.17.0.1"
        new_port_config["routingTable"][1]["egressIpAddress"] = "172.17.0.1"
        with open(cls.config_filepath, 'w') as config_file:
            json.dump(new_port_config, config_file, indent=4)

    def setUp(self):
        self.test_udp_sender = TestSender()
        self.test_udp_listener = TestReceiver("0.0.0.0", 50001)
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 50001, "zvu")

    def tearDown(self):
        self.test_udp_sender.close()
        self.test_udp_listener.close()
        subprocess.run("docker stop emulator".split())
        subprocess.run("docker rm emulator".split())

    @classmethod
    def tearDownClass(cls):
        TestHelpers.reset_port_config_file(cls.valid_port_config)
        subprocess.run("docker stop management_interface".split())
        cls.interface_server_thread.join()

    def test_non_sisl_data_received_matches_data_sent(self):
        requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001, "zvu")
        self.assertRaises(socket.timeout, TestHelpers.wait_for_action, lambda: (self.test_udp_listener.recv() != b"\x00", 0), "Non-empty packets received exceeded maximum")
        self.test_udp_sender.send(b"1234", "172.17.0.1", 40001)

        self.assertEqual(self.test_udp_listener.recv(), b"1234")
        requests.post("http://172.17.0.1:8081/api/command/diode/power/off")
        TestHelpers.wait_for_closed_comms_ports("172.17.0.1", 40001, "zvu")


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(EndToEndEmulatorTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
