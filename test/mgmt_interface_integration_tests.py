# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
import subprocess
import requests
import json
import time
import threading
from test_helpers import TestHelpers
import launch_emulator
from Emulator import launch_emulator_interface


class MgmtInterfaceIntegrationTests(unittest.TestCase):
    interface_server_thread = None
    valid_port_config = None

    @classmethod
    def setUpClass(cls):
        cls.start_interface_server()
        cls.save_port_config()
        try:
            TestHelpers.wait_for_open_comms_ports("172.17.0.1", 8081, "zv")
        except TimeoutError as ex:
            print(f"Exception during setUpClass: {ex}")
            cls.clean_up_class()
            raise

    @classmethod
    def save_port_config(cls):
        with open('Emulator/config/portConfig.json', 'r') as config_file:
            cls.valid_port_config = json.loads(config_file.read())

    @classmethod
    def start_interface_server(cls):
        cls.interface_server_thread = threading.Thread(target=launch_emulator_interface.start_interface, args=(8081,))
        cls.interface_server_thread.start()

    @classmethod
    def clean_up_class(cls):
        subprocess.run("docker stop interface", shell=True)
        cls.interface_server_thread.join()
        cls.reset_port_config_file()

    @classmethod
    def reset_port_config_file(cls):
        with open('Emulator/config/portConfig.json', 'w') as config_file:
            json.dump(cls.valid_port_config, config_file, indent=4)

    @classmethod
    def tearDownClass(cls):
        cls.clean_up_class()

    @classmethod
    def tearDown(cls):
        subprocess.run("docker stop emulator && docker rm emulator", shell=True)

    def test_get_config_endpoint(self):
        response = requests.get("http://172.17.0.1:8081/api/config/diode")

        with open('Emulator/config/portConfig.json', 'r') as config_file:
            expected = json.loads(config_file.read())

        self.assertEqual(expected, json.loads(response.text))
        self.assertEqual(200, response.status_code)

    def test_power_on_endpoint(self):
        self.assertRaises(TimeoutError, TestHelpers.wait_for_open_comms_ports, "172.17.0.1", 40001, "zvu")

        response = requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001, "zvu")

        self.assertEqual("completed", json.loads(response.text)['status'])
        self.assertEqual(200, response.status_code)

    def test_power_off_endpoint(self):
        launch_emulator.start_emulator("Emulator/config/portConfig.json")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001, "zvu")

        response = requests.post("http://172.17.0.1:8081/api/command/diode/power/off")
        self.assertRaises(TimeoutError, TestHelpers.wait_for_open_comms_ports, "172.17.0.1", 40001, "zvu")

        self.assertEqual("completed", json.loads(response.text)['status'])
        self.assertEqual(200, response.status_code)

    def test_power_off_removes_emulator_container(self):
        requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001, "zvu")
        requests.post("http://172.17.0.1:8081/api/command/diode/power/off")
        self.assertRaises(TimeoutError, TestHelpers.wait_for_open_comms_ports, "172.17.0.1", 40001, "zvu")
        requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001, "zvu")

    def test_update_config_endpoint(self):
        with open('Emulator/config/portConfig.json', 'r') as config_file:
            new_config = json.loads(config_file.read())

        new_config["routingTable"][0]["ingressPort"] = 40002

        requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001, "zvu")

        response = requests.put("http://172.17.0.1:8081/api/config/diode",
                                json=new_config,
                                headers={"Content-Type": "application/json"})
        self.assertEqual("completed", json.loads(response.text)['status'])

        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40002, "zvu")


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MgmtInterfaceIntegrationTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
