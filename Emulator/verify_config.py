# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

from jsonschema import validate as json_schema_validate
from jsonschema import ValidationError, FormatChecker
import json
from config_schema import ConfigSchema


class VerifyConfig:

    @staticmethod
    def validate(config, max_length=1048576):
        VerifyConfig._verify_non_empty_config_file(config)
        VerifyConfig._verify_config_less_than_max_length(config, max_length)
        VerifyConfig._verify_config_with_schema(config)
        VerifyConfig._verify_port_span(config)
        VerifyConfig._verify_unique_ports(config)

    @staticmethod
    def _verify_non_empty_config_file(config):
        if len(config) == 0:
            raise ConfigErrorEmptyFile("Provided config file is empty")

    @staticmethod
    def _verify_config_less_than_max_length(config, max_length):
        if len(json.dumps(config)) > max_length:
            raise ConfigErrorFileSizeTooLarge("Provided config file size too large")

    @staticmethod
    def _verify_config_with_schema(config):
        try:
            json_schema_validate(config, schema=ConfigSchema.get_schema(), format_checker=FormatChecker())
        except ValidationError as err:
            raise ConfigErrorFailedSchemaVerification(err.message)

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
