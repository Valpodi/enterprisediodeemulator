# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

class VerifyConfig:
    @staticmethod
    def validate(config):
        return VerifyConfig.verify_non_empty_config_file(config)

    @staticmethod
    def verify_non_empty_config_file(config):
        if len(config) == 0:
            raise ConfigErrorEmptyFile("Provided config file is empty")


class ConfigErrorEmptyFile(Exception):
    pass
