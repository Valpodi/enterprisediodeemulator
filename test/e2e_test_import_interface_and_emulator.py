# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import copy
import unittest
import subprocess
import threading
import pysisl
import requests
import socket
import json

from test_helpers import TestHelpers, TestSender, TestReceiver


class EndToEndEmulatorTests(unittest.TestCase):
    interface_server_thread = None
    valid_port_config = None
    config_filepath = 'Emulator/config/port_config.json'
    test_udp_sender = None
    test_udp_listener = None

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
        cls.test_udp_sender = TestSender()
        cls.test_udp_listener = TestReceiver("0.0.0.0", 50001)
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 50001)
        requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001)

    @classmethod
    def start_interface_server_in_thread(cls):
        cls.interface_server_thread = threading.Thread(target=cls.start_interface_server, daemon=True)
        cls.interface_server_thread.start()

    @classmethod
    def start_interface_server(cls):
        subprocess.Popen('python3 Emulator/launch_management_interface.py --interfacePort 8081 --importDiode'.split())

    @classmethod
    def update_port_config(cls):
        new_port_config = copy.deepcopy(cls.valid_port_config)
        new_port_config["routingTable"][0]["egressIpAddress"] = "172.17.0.1"
        new_port_config["routingTable"][1]["egressIpAddress"] = "172.17.0.1"
        with open(cls.config_filepath, 'w') as config_file:
            json.dump(new_port_config, config_file, indent=4)

    def setUp(self):
        self.clear_netcat_buffer()

    def clear_netcat_buffer(self):
        self.assertRaises(socket.timeout, TestHelpers.wait_for_action,
                          lambda: (self.test_udp_listener.recv() != b"\x00", 0),
                          "Non-empty packets received exceeded maximum")

    @classmethod
    def tearDownClass(cls):
        cls.test_udp_sender.close()
        cls.test_udp_listener.close()
        requests.post("http://172.17.0.1:8081/api/command/diode/power/off")
        TestHelpers.wait_for_closed_comms_ports("172.17.0.1", 40001)
        TestHelpers.reset_port_config_file(cls.valid_port_config)
        subprocess.run("docker stop management_interface".split())
        cls.interface_server_thread.join()

    def test_sisl_data_received_matches_data_sent(self):
        data = TestHelpers.get_valid_control_header() + b'{name: !str "helpful_name", flag: !bool "false", count: !int "3"}'
        self.test_udp_sender.send(data, "172.17.0.1", 40001)
        self.assertEqual(self.test_udp_listener.recv(), data)

    def test_not_sisl_data_is_wrapped(self):
        data = TestHelpers.get_valid_control_header() + b'not_sisl'
        self.test_udp_sender.send(data, "172.17.0.1", 40001)
        received = self.test_udp_listener.recv()
        self.assertNotEqual(received, data)

        sent_control_header_length = 64
        received_unwrapped = pysisl.unwraps(received[sent_control_header_length:])
        control_header_length = 112
        self.assertEqual(received_unwrapped, data[control_header_length:])


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(EndToEndEmulatorTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
