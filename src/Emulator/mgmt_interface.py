from flask import Response
import json


class Interface:
    @staticmethod
    def do_config_get():
        return Response(json.dumps({"config": "config file contents"}), 200)

    @staticmethod
    def do_config_update():
        return Response(json.dumps({"status": "completed"}), 200)

    @staticmethod
    def do_power_on_procedure():
        return Response(json.dumps({"status": "completed"}), 200)

    @staticmethod
    def do_power_off_procedure():
        return Response(json.dumps({"status": "completed"}), 200)
