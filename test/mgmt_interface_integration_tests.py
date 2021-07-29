# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
import subprocess
import requests
import json
import time
import threading

import launch_emulator
from Emulator import launch_emulator_interface


class MgmtInterfaceIntegrationTests(unittest.TestCase):
    interface_server_thread = None

    @classmethod
    def setUpClass(cls):
        cls.start_interface_server()
        cls.wait_for_port(8081)
        cls.build_emulator()

    @classmethod
    def start_interface_server(cls):
        subprocess.run("docker build -f Emulator/MgmtInterfaceDockerfile -t emulatorinterface .", shell=True)
        cls.interface_server_thread = threading.Thread(target=launch_emulator_interface.start_interface)
        cls.interface_server_thread.start()

    @classmethod
    def wait_for_port(cls, port_to_check, options="zv"):
        cls.wait_for_action(lambda: (subprocess.call(
            f"nc -{options} 172.17.0.1 {port_to_check} -w 1".split())), 0, f"port {port_to_check} should be open", delay=3)

    @classmethod
    def wait_for_action(cls, action, expected_result, message, delay=0, attempts=5):
        condition_met = False
        while not condition_met:
            action_output = action()
            condition_met = (action_output == expected_result)
            attempts = attempts - 1
            if attempts == 0:
                raise TimeoutError("Failed waiting for: " + message)
            time.sleep(delay)
        if condition_met:
            return action_output

    @classmethod
    def build_emulator(cls):
        subprocess.run("cd Emulator && docker build --no-cache -t emulator -f Dockerfile . && cd ..", shell=True)

    @classmethod
    def tearDownClass(cls):
        subprocess.run("docker stop interface", shell=True)
        cls.interface_server_thread.join()

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
        response = requests.post("http://172.17.0.1:8081/api/command/diode/power/on")
        self.assertEqual("completed", json.loads(response.text)['status'])
        self.assertEqual(200, response.status_code)

    def test_power_off_endpoint(self):
        launch_emulator.start_emulator("Emulator/config/portConfig.json")
        self.wait_for_port(40001, "zvu")

        response = requests.post("http://172.17.0.1:8081/api/command/diode/power/off")
        self.assertRaises(TimeoutError, self.wait_for_port, 40001, "zvu")

        self.assertEqual("completed", json.loads(response.text)['status'])
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MgmtInterfaceIntegrationTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
