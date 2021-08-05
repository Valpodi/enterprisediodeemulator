# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

from jsonschema import validate as json_schema_validate
from jsonschema import ValidationError, FormatChecker
import json
from config_schema import ConfigSchema


class VerifyConfig:
    def __init__(self, config, max_length=1048576):
        self.config = config
        self.max_length = max_length

    def validate(self):
        self._verify_non_empty_config_file()
        self._verify_config_less_than_max_length()
        self._verify_config_with_schema()

    def _verify_non_empty_config_file(self):
        if len(self.config) == 0:
            raise ConfigErrorEmptyFile("Provided config file is empty")

    def _verify_config_less_than_max_length(self):
        if len(json.dumps(self.config)) > self.max_length:
            raise ConfigErrorFileSizeTooLarge("Provided config file size too large")

    def _verify_config_with_schema(self):
        try:
            json_schema_validate(self.config, schema=ConfigSchema.get_schema(), format_checker=FormatChecker())
        except ValidationError as err:
            raise ConfigErrorFailedSchemaVerification


class ConfigErrorEmptyFile(Exception):
    pass


class ConfigErrorFileSizeTooLarge(Exception):
    pass


class ConfigErrorFailedSchemaVerification(Exception):
    pass
