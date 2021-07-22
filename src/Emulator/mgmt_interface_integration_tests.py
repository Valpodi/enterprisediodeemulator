import unittest
import subprocess
import requests
import json
import time


class MgmtInterfaceIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.start_server()

    @classmethod
    def start_server(cls):
        subprocess.run("docker build -f MgmtInterfaceDockerfile -t emulatorinterface .", shell=True)
        subprocess.Popen("python3 launch_emulator_with_interface.py", shell=True)
        cls.wait_for_port(8081)

    @classmethod
    def wait_for_port(cls, port_to_check):
        cls.wait_for_action(lambda: (subprocess.call(
            f"nc -zv localhost {port_to_check} -w 1".split())), 0, f"port {port_to_check} should be open", delay=3)

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

    def test_get_config_endpoint(self):
        response = requests.get("http://localhost:8081/api/config/diode")

        self.assertEqual(200, response.status_code)
        self.assertEqual("config file contents", json.loads(response.text)["config"])


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MgmtInterfaceIntegrationTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
