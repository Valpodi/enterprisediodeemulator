# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import os
import connexion
from flask import Response
import json
import subprocess
import launch_emulator
from verify_config import VerifyConfig, ConfigError


class ManagementInterface:
    config_file = None
    config_filepath = 'Emulator/config/port_config.json'
    schema_filepath = '/usr/src/app/openapi/schema.json'

    @classmethod
    def get_config_information(cls):
        if cls._file_exists(cls.config_filepath):
            data = cls._get_file_content(cls.config_filepath)
        else:
            data = {"Status": "Config file does not exist"}
        return Response(json.dumps(data), 200)

    @staticmethod
    def _file_exists(filepath):
        return os.path.exists(filepath)

    @staticmethod
    def _get_file_content(filepath):
        with open(filepath, 'r') as file:
            return json.loads(file.read())

    @classmethod
    def get_config_schema(cls):
        if cls._file_exists(cls.schema_filepath):
            data = cls._get_file_content(cls.schema_filepath)
        else:
            data = {"Status": "Schema file does not exist"}
        return Response(json.dumps(data), 200)

    @classmethod
    def do_config_update(cls):
        cls.config_file = connexion.request.get_json()
        try:
            cls._validate_config()
        except ConfigError as exc:
            return Response(f"{exc}", 400)
        cls._power_off_diode()
        cls._update_config()
        cls._power_on_diode()

        return Response("", 200)

    @classmethod
    def _validate_config(cls):
        return VerifyConfig().validate(cls.config_file)

    @classmethod
    def _update_config(cls):
        with open(cls.config_filepath, 'w') as config_file:
            json.dump(cls.config_file, config_file)

    @classmethod
    def do_power_on(cls):
        if not cls._remove_container():
            raise DiodePowerCycleError("ERROR: unable to power on the diode.")

        if cls._file_exists(cls.config_filepath):
            data = cls._power_on_diode()
        else:
            data = {"Status": "Config file could not be found to power on diode"}
        return Response(json.dumps(data), 200)

    @classmethod
    def _power_on_diode(cls):
        is_import_diode = os.environ.get("IMPORTDIODE")
        return {"Status": {0: "Diode powered on"}.get(launch_emulator.start_emulator(cls.config_filepath, is_import_diode))}

    @classmethod
    def do_power_off(cls):
        cls._power_off_diode()
        return Response("", 200)

    @classmethod
    def _power_off_diode(cls):
        cls._remove_container()

    @classmethod
    def _remove_container(cls):
        stop_process = subprocess.run("docker stop emulator".split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        stop_process_success = (b"No such container: emulator" in stop_process.stdout) or (stop_process.returncode == 0)
        remove_process = subprocess.run("docker rm emulator".split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        remove_process_success = (b"No such container: emulator" in stop_process.stdout) or (remove_process.returncode == 0)
        return stop_process_success & remove_process_success

    @classmethod
    def get_versioning_information(cls):
        return Response("Not implemented", 200)

    @classmethod
    def get_status_information(cls):
        return Response("Not implemented", 200)

    @classmethod
    def get_ip_settings(cls):
        return Response("Not implemented", 200)

    @classmethod
    def update_ip_settings(cls):
        return Response("Not implemented", 200)

    @classmethod
    def get_syslog_address(cls):
        return Response("Not implemented", 200)

    @classmethod
    def update_syslog_address(cls):
        return Response("Not implemented", 200)

    @classmethod
    def get_ssh_settings(cls):
        return Response("Not implemented", 200)

    @classmethod
    def update_ssh_settings(cls):
        return Response("Not implemented", 200)

    @classmethod
    def update_ssl_certificates(cls):
        return Response("Not implemented", 200)


class DiodePowerCycleError(Exception):
    pass
