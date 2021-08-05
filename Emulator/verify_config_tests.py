# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file
import unittest
from verify_config import VerifyConfig, ConfigErrorEmptyFile, ConfigErrorFileSizeTooLarge, \
    ConfigErrorFailedSchemaVerification


class VerifyConfigTests(unittest.TestCase):
    def test_empty_config_throws_error(self):
        verify_config = VerifyConfig({})
        self.assertRaises(ConfigErrorEmptyFile, verify_config.validate)

    def test_config_file_longer_than_max_length_throws_error(self):
        verify_config = VerifyConfig({"ingress": {}, "egress": {}, "routingTable": []}, max_length=10)
        self.assertRaises(ConfigErrorFileSizeTooLarge,
                          verify_config.validate)

    def test_config_file_matches_schema(self):
        VerifyConfig({"ingress": {}, "egress": {}, "routingTable": []}).validate()

    def test_config_file_that_does_not_match_schema_throws_error(self):
        verify_config = VerifyConfig({"ingress": {}})
        self.assertRaises(ConfigErrorFailedSchemaVerification, verify_config.validate)


if __name__ == '__main__':
    unittest.main()
