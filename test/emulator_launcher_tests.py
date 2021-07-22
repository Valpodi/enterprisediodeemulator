import unittest
import subprocess


class EmulatorTests(unittest.TestCase):

    def test_portspan_over_1024_fails_to_launch(self):
        self.assertRaises(subprocess.CalledProcessError, subprocess.check_call,
                          "python3 launchEmulator.py".split(), cwd="Emulator")


if __name__ == '__main__':
    unittest.main()