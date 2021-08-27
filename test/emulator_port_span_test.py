# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import subprocess
import unittest


class EmulatorSpanTooLargeTest(unittest.TestCase):

    def setUp(self):
        subprocess.run("docker stop emulator".split())
        subprocess.run("docker rm emulator".split())

    def tearDown(self):
        subprocess.run("docker stop emulator".split())
        subprocess.run("docker rm emulator".split())

    def test_launch_emulator_with_port_span_too_large_throws_error(self):
        self.assertTrue("Config validation failed: Ingress portSpan must be less than 2048." in subprocess.run(
            "python3 Emulator/launch_emulator.py -p test/portSpanTooLarge.json".split(), stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE).stdout.decode())


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(EmulatorSpanTooLargeTest)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
