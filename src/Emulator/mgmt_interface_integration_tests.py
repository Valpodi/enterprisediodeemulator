import unittest
import subprocess
import requests
import json
import os
import time
import mgmt_interface


class MgmtInterfaceIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.start_server()

    @classmethod
    def start_server(cls):
        subprocess.run("docker build -f MgmtInterfaceDockerfile -t emulatorinterface .", shell=True)
        subprocess.Popen("python3 launch_emulator_with_interface.py", shell=True)
        cls.wait_for_server()

    @classmethod
    def wait_for_server(cls):
        loop_counter = 10
        api_active = False
        while not api_active:
            time.sleep(2)
            loop_counter -= 1
            if requests.get("http://localhost:8081/api/config/diode").status_code == 200:
                api_active = True
            if loop_counter == 0:
                raise Exception("FailedToStartServer")
        print(f"Management interface started")

    def test_get_config_endpoint(self):
        response = requests.get("http://localhost:8081/api/config/diode")

        self.assertEqual(200, response.status_code)
        self.assertEqual("config file contents", json.loads(response.text)["config"])


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MgmtInterfaceIntegrationTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
