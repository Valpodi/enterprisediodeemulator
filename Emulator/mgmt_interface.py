# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file
import connexion
import requests
from flask import Response
import json
import subprocess
import launch_emulator


class Interface:
    @classmethod
    def do_config_get(cls):
        return Response(json.dumps(cls._get_config_file()), 200)

    @classmethod
    def _get_config_file(cls):
        with open('Emulator/config/portConfig.json', 'r') as config_file:
            return json.loads(config_file.read())

    @classmethod
    def do_config_update(cls):
        cls._power_off_diode()
        cls._update_config()
        cls._power_on_diode()

        return Response(json.dumps({"status": "completed"}), 200)

    @classmethod
    def _update_config(cls):
        with open('Emulator/config/portConfig.json', 'w') as config_file:
            json.dump(connexion.request.get_json(), config_file)

    @classmethod
    def do_power_on_procedure(cls):
        return Response(json.dumps(cls._power_on_diode()), 200)

    @classmethod
    def _power_on_diode(cls):
        return {"status": {0: "completed"}.get(launch_emulator.start_emulator("Emulator/config/portConfig.json"), "failed")}

    @classmethod
    def do_power_off_procedure(cls):
        return Response(json.dumps(cls._power_off_diode()), 200)

    @classmethod
    def _power_off_diode(cls):
        return {"status": {0: "completed"}.get(subprocess.run("docker stop emulator && docker rm emulator", shell=True).returncode, "failed")}
