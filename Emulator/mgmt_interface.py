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
    config_filepath = 'Emulator/config/portConfig.json'
    schema_filepath = 'Emulator/openapi/schema.json'

    @classmethod
    def do_config_get(cls):
        if cls._file_exists(cls.config_filepath):
            return Response(json.dumps(cls._get_file_content(cls.config_filepath)), 200)
        else:
            return Response(json.dumps({"status": "Config file does not exist"}), 200)

    @staticmethod
    def _get_file_content(filepath):
        with open(filepath, 'r') as file:
            return json.loads(file.read())

    @staticmethod
    def _file_exists(filepath):
        return os.path.exists(filepath)

    @classmethod
    def get_config_schema(cls):
        if cls._file_exists(cls.schema_filepath):
            return Response(json.dumps(cls._get_file_content(cls.schema_filepath)), 200)
        else:
            return Response(json.dumps({"status": "Schema file does not exist"}), 200)

    @classmethod
    def _get_schema_file(cls):
        with open(cls.schema_filepath, 'r') as schema_file:
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
        if cls._file_exists(cls.config_filepath):
            return Response(json.dumps(cls._power_on_diode()), 200)
        else:
            return Response(json.dumps({"status": "Config file could not be found to power on diode"}), 200)

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


