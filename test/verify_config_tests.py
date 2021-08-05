# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file
import unittest
from Emulator.verify_config import VerifyConfig, ConfigErrorEmptyFile


class VerifyConfigTests(unittest.TestCase):
    def test_empty_config(self):
        config = ""
        self.assertRaises(ConfigErrorEmptyFile, VerifyConfig.validate, config)


if __name__ == '__main__':
    unittest.main()
