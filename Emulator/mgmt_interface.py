# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import subprocess
from flask import Response
import json


class Interface:
    @classmethod
    def do_config_get(cls):
        return Response(json.dumps(cls._get_config_file()), 200)

    @classmethod
    def _get_config_file(cls):
        with open('config/portConfig.json', 'r') as config_file:
            return json.loads(config_file.read())

    @classmethod
    def do_config_update(cls):
        return Response(json.dumps({"status": "completed"}), 200)

    @classmethod
    def do_power_on_procedure(cls):
        cls._power_on_diode()
        return Response(json.dumps({"status": "completed"}), 200)

    @classmethod
    def do_power_off_procedure(cls):
        return Response(json.dumps({"status": "completed"}), 200)

    @classmethod
    def _power_on_diode(cls):
        return {0: "completed"}.get(subprocess.check_output("python3 launchEmulatory.py", shell=True).returncode, default="failed")
