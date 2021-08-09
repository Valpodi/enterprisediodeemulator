# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import copy
import unittest
import verify_config


class VerifyConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = {"properties": {"ingress": {"type": "object"},
                                 "egress": {"type": "object"},
                                 "routingTable": {"type": "array"}},
                  "required": ["ingress", "egress", "routingTable"]}

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
        self.assertRaises(verify_config.ConfigErrorEmptyFile,
                          verify_config.VerifyConfig({}).validate,
                          {})

    def test_config_file_longer_than_max_length_throws_error(self):
        self.assertRaises(verify_config.ConfigErrorFileSizeTooLarge,
                          verify_config.VerifyConfig({}).validate,
                          config={"ingress": {}, "egress": {}, "routingTable": []}, max_length=10)

    def test_config_file_matches_schema(self):
        verify_config.VerifyConfig(self.schema).validate(self.config)

    def test_config_file_that_does_not_match_schema_throws_error(self):
        self.assertRaises(verify_config.ConfigErrorFailedSchemaVerification,
                          verify_config.VerifyConfig(self.schema).validate,
                          {"ingress": {}})

    def test_port_span_exceeds_2048_throws_error(self):
        config_port_span_too_large = copy.deepcopy(self.config)
        config_port_span_too_large["routingTable"] = [
            {
                "ingressPort": 40000,
                "egressIpAddress": "192.168.0.20",
                "egressSrcPort": 50001,
                "egressDestPort": 50001
            },
            {
                "ingressPort": 42048,
                "egressIpAddress": "192.168.0.21",
                "egressSrcPort": 51024,
                "egressDestPort": 51024
            }
        ]
        self.assertRaisesRegex(verify_config.ConfigErrorInvalidPortSpan,
                               "Config validation failed: Ingress portSpan must be less than 2048.",
                               verify_config.VerifyConfig(self.schema).validate,
                               config_port_span_too_large)

    def test_ingress_ports_not_unique_throws_error(self):
        config_ports_not_unique = copy.deepcopy(self.config)
        config_ports_not_unique["routingTable"] = [
            {
                "ingressPort": 40000,
                "egressIpAddress": "192.168.0.20",
                "egressSrcPort": 50001,
                "egressDestPort": 50001
            },
            {
                "ingressPort": 40000,
                "egressIpAddress": "192.168.0.21",
                "egressSrcPort": 51024,
                "egressDestPort": 51024
            }
        ]
        self.assertRaisesRegex(verify_config.ConfigErrorIngressPortsNotUnique,
                               "Config validation failed: Ingress ports must be unique.",
                               verify_config.VerifyConfig(self.schema).validate,
                               config_ports_not_unique)


if __name__ == '__main__':
    unittest.main()
