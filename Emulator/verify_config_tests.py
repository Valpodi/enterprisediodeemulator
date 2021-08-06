# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import copy
import unittest
from verify_config import VerifyConfig, ConfigErrorEmptyFile, ConfigErrorFileSizeTooLarge, \
    ConfigErrorFailedSchemaVerification, ConfigErrorInvalidPortSpan


class VerifyConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        interface = {
            "useDHCP": False,
            "ping": True,
            "mtu": 9000
        }

        cls.config = {"ingress": interface,
                      "egress": interface,
                      "routingTable": [
                          {
                              "ingressPort": 50000,
                              "egressIpAddress": "192.168.0.20",
                              "egressSrcPort": 60000,
                              "egressDestPort": 60600
                          },
                          {
                              "ingressPort": 50500,
                              "egressIpAddress": "192.168.0.21",
                              "egressSrcPort": 60004,
                              "egressDestPort": 61004
                          }
                      ]
                      }

    def test_empty_config_throws_error(self):
        verify_config = VerifyConfig({})
        self.assertRaises(ConfigErrorEmptyFile, verify_config.validate)

    def test_config_file_longer_than_max_length_throws_error(self):
        verify_config = VerifyConfig({"ingress": {}, "egress": {}, "routingTable": []}, max_length=10)
        self.assertRaises(ConfigErrorFileSizeTooLarge,
                          verify_config.validate)

    def test_config_file_matches_schema(self):
        VerifyConfig(self.config).validate()

    def test_config_file_that_does_not_match_schema_throws_error(self):
        verify_config = VerifyConfig({"ingress": {}})
        self.assertRaises(ConfigErrorFailedSchemaVerification, verify_config.validate)

    def test_ethernet_ports_is_provided_when_use_dhcp_is_true(self):
        config_with_dhcp_true = copy.deepcopy(self.config)
        config_with_dhcp_true["ingress"]["useDHCP"] = True
        self.assertRaisesRegex(ConfigErrorFailedSchemaVerification,
                               "'ethernetPorts' is a required property",
                               VerifyConfig(config_with_dhcp_true).validate)

    def test_port_span_exceeds_1024_throws_error(self):
        config_port_span_too_large = copy.deepcopy(self.config)
        config_port_span_too_large["routingTable"] = [
            {
                "ingressPort": 40000,
                "egressIpAddress": "192.168.0.20",
                "egressSrcPort": 50001,
                "egressDestPort": 50001
            },
            {
                "ingressPort": 41024,
                "egressIpAddress": "192.168.0.21",
                "egressSrcPort": 51024,
                "egressDestPort": 51024
            }
        ]
        self.assertRaisesRegex(ConfigErrorInvalidPortSpan,
                               "Config validation failed: Ingress portSpan must be less than 1024.",
                               VerifyConfig(config_port_span_too_large).validate)


if __name__ == '__main__':
    unittest.main()
