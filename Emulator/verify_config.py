# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import json
from jsonschema import ValidationError, FormatChecker
from jsonschema import validate as json_schema_validate


class VerifyConfig:
    def __init__(self, schema=None, max_config_bytes=1048576):
        self.schema_filepath = '/usr/src/app/openapi/schema.json'
        self.schema = self._get_schema() if schema is None else schema
        self.max_config_bytes = max_config_bytes

    def validate(self, config):
        VerifyConfig._verify_non_empty_config_file(config)
        self._verify_config_less_than_max_length(config)
        self._verify_config_with_schema(config)
        VerifyConfig._verify_port_span(config)
        VerifyConfig._verify_unique_ports(config)

    @staticmethod
    def _verify_non_empty_config_file(config):
        if len(config) == 0:
            raise ConfigErrorEmptyFile("Provided config file is empty")

    def _verify_config_less_than_max_length(self, config):
        if len(json.dumps(config)) > self.max_config_bytes:
            raise ConfigErrorFileSizeTooLarge("Provided config file size too large")

    def _verify_config_with_schema(self, config):
        try:
            json_schema_validate(config, schema=self.schema, format_checker=FormatChecker())
        except ValidationError as err:
            raise ConfigErrorFailedSchemaVerification(err.message)

    def _get_schema(self):
        with open(self.schema_filepath, 'r') as schema:
            return json.loads(schema.read())

    @staticmethod
    def _verify_port_span(config):
        route_table = config["routingTable"]
        ingress_ports = [route["ingressPort"] for route in route_table]

        if (max(ingress_ports) - min(ingress_ports) + 1) > 2048:
            raise ConfigErrorInvalidPortSpan("Config validation failed: Ingress portSpan must be less than 2048.")

    @staticmethod
    def _verify_unique_ports(config):
        route_table = config["routingTable"]
        ingress_ports = [route["ingressPort"] for route in route_table]

        if len(set(ingress_ports)) < len(ingress_ports):
            raise ConfigErrorIngressPortsNotUnique("Config validation failed: Ingress ports must be unique.")


class ConfigErrorEmptyFile(Exception):
    pass


class ConfigErrorFileSizeTooLarge(Exception):
    pass


class ConfigErrorFailedSchemaVerification(Exception):
    pass


class ConfigErrorInvalidPortSpan(Exception):
    pass


class ConfigErrorIngressPortsNotUnique(Exception):
    pass
