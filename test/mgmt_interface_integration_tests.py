# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import os
import unittest
import subprocess
import requests
import json
import threading
from test_helpers import TestHelpers
import launch_emulator
from Emulator import launch_management_interface


class MgmtInterfaceIntegrationTests(unittest.TestCase):
    interface_server_thread = None
    valid_port_config = None

    @classmethod
    def setUpClass(cls):
        cls.start_interface_server()
        cls.valid_port_config = TestHelpers.save_port_config()
        try:
            TestHelpers.wait_for_open_comms_ports("172.17.0.1", 8081, "zv")
        except TimeoutError as ex:
            print(f"Exception during setUpClass: {ex}")
            cls.tearDownClass()
            raise

    @classmethod
    def start_interface_server(cls):
        cls.interface_server_thread = threading.Thread(target=launch_management_interface.start_interface, args=(8081,))
        cls.interface_server_thread.start()

    @classmethod
    def tearDownClass(cls):
        subprocess.run("docker stop management_interface", shell=True)
        cls.interface_server_thread.join()
        TestHelpers.reset_port_config_file(cls.valid_port_config)

    @classmethod
    def tearDown(cls):
        TestHelpers.reset_port_config_file(cls.valid_port_config)
        subprocess.run("docker stop emulator && docker rm emulator", shell=True)

    def test_get_config_endpoint(self):
        response = requests.get("http://172.17.0.1:8081/api/config/diode")
        with open('Emulator/config/portConfig.json', 'r') as config_file:
            expected = json.loads(config_file.read())
        self.assertEqual(expected, json.loads(response.text))

    def test_power_on_endpoint(self):
        self.assertRaises(TimeoutError, TestHelpers.wait_for_open_comms_ports, "172.17.0.1", 40001, "zvu")
        requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001, "zvu")

    def test_power_off_endpoint(self):
        launch_emulator.start_emulator("Emulator/config/portConfig.json")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001, "zvu")
        requests.post("http://172.17.0.1:8081/api/command/diode/power/off")
        self.assertRaises(TimeoutError, TestHelpers.wait_for_open_comms_ports, "172.17.0.1", 40001, "zvu")

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

        requests.put("http://172.17.0.1:8081/api/config/diode",
                     json=new_config,
                     headers={"Content-Type": "application/json"})
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40002, "zvu")

    def test_config_endpoint_schema_check_raises_error(self):
        with open('Emulator/config/portConfig.json', 'r') as config_file:
            new_config = json.loads(config_file.read())
            del new_config["routingTable"]

        requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        TestHelpers.wait_for_open_comms_ports("172.17.0.1", 40001, "zvu")

        response = requests.put("http://172.17.0.1:8081/api/config/diode",
                                json=new_config,
                                headers={"Content-Type": "application/json"})
        self.assertEqual(500, response.status_code)

    def test_missing_config_file_with_get_config_endpoint(self):
        os.remove('Emulator/config/portConfig.json')
        response = requests.get("http://172.17.0.1:8081/api/config/diode")
        self.assertEqual("Config file does not exist", json.loads(response.text)["status"])

    def test_missing_config_file_with_power_on_endpoint(self):
        os.remove('Emulator/config/portConfig.json')
        response = requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        self.assertEqual("Config file could not be found to power on diode", json.loads(response.text)["status"])


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MgmtInterfaceIntegrationTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
