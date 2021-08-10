import subprocess
import unittest
from test_helpers import TestHelpers


class EmulatorSpanTooLargeTest(unittest.TestCase):

    def setUp(self):
        subprocess.run("docker stop emulator".split())
        subprocess.run("docker rm emulator".split())

    def tearDown(self):
        subprocess.run("docker stop emulator".split())
        subprocess.run("docker rm emulator".split())

    def test_start_emulator_with_port_span_too_large_throws_error(self):
        subprocess.call("python3 launch_emulator.py -p test/portSpanTooLarge.json".split())
        self.assertRaises(TimeoutError, TestHelpers.wait_for_open_comms_ports, "172.17.0.1", 40000, "zvu", attempts=3)
        logs = subprocess.check_output("docker logs emulator".split(), stderr=subprocess.STDOUT)
        self.assertTrue("Config validation failed: Ingress portSpan must be less than 2048." in logs.decode())


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(EmulatorSpanTooLargeTest)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
