# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import os
import connexion
from flask import Response
import json
import subprocess
import launch_emulator
from verify_config import VerifyConfig


class Interface:
    config_file = None

    @classmethod
    def do_config_get(cls):
        return cls._check_file_and_action('Emulator/config/portConfig.json',
                                          cls._get_config_file,
                                          "Config file does not exist")

    @classmethod
    def _check_file_and_action(cls, file, action, error_message):
        if cls._file_exists(file):
            return Response(json.dumps(action()), 200)
        else:
            return Response(json.dumps({"status": error_message}), 200)

    @staticmethod
    def _file_exists(filepath):
        return os.path.exists(filepath)

    @classmethod
    def _get_config_file(cls):
        with open('Emulator/config/portConfig.json', 'r') as config_file:
            return json.loads(config_file.read())

    @classmethod
    def get_config_schema(cls):
        return cls._check_file_and_action('Emulator/openapi/schema.json',
                                          cls._get_schema_file,
                                          "Schema file does not exist")

    @classmethod
    def _get_schema_file(cls):
        with open('Emulator/openapi/schema.json', 'r') as schema_file:
            return json.loads(schema_file.read())

    @classmethod
    def do_config_update(cls):
        cls.config_file = connexion.request.get_json()
        cls._validate_config()
        cls._power_off_diode()
        cls._update_config()
        cls._power_on_diode()

        return Response(json.dumps({"status": "completed"}), 200)

    @classmethod
    def _validate_config(cls):
        return VerifyConfig().validate(cls.config_file)

    @classmethod
    def _update_config(cls):
        with open('Emulator/config/portConfig.json', 'w') as config_file:
            json.dump(cls.config_file, config_file)

    @classmethod
    def do_power_on_procedure(cls):
        return cls._check_file_and_action('Emulator/config/portConfig.json',
                                          cls._power_on_diode,
                                          "Config file could not be found to power on diode")

    @classmethod
    def _power_on_diode(cls):
        return {"status": {0: "completed"}.get(launch_emulator.start_emulator("Emulator/config/portConfig.json"), "failed")}

    @classmethod
    def do_power_off_procedure(cls):
        return Response(json.dumps(cls._power_off_diode()), 200)

    @classmethod
    def _power_off_diode(cls):
        return {"status": {0: "completed"}.get(
            subprocess.run("docker stop emulator && docker rm emulator", shell=True).returncode, "failed")}


