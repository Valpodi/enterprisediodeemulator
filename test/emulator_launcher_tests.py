# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
import subprocess


class EmulatorTests(unittest.TestCase):

    def test_portspan_over_2048_fails_to_launch(self):
        self.assertRaises(subprocess.CalledProcessError, subprocess.check_call,
                          "python3 launch_emulator.py".split(), cwd="Emulator")


if __name__ == '__main__':
    unittest.main()
