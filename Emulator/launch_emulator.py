# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import json
import subprocess
import argparse
import os

from verify_config import VerifyConfig


def start_emulator(port_config_path, is_import_diode=False):
    with open("Emulator/openapi/schema.json") as schema_file:
        schema = json.load(schema_file)

    with open(port_config_path) as config_file:
        config = json.load(config_file)

    VerifyConfig(schema).validate(config)
    port_map = config["routingTable"]
    ingress_ports = [port["ingressPort"] for port in port_map]
    ports_cmd = "".join([f"-p {port}:{port}/udp " for port in ingress_ports])
    return subprocess.run(
        f'docker run --name=emulator '
        f'           -v {os.getcwd()}/{port_config_path}:/usr/src/app/config/port_config.json '
        f'           {ports_cmd} '
        f'           --env IMPORTDIODE={is_import_diode} '
        f'           -d emulator '
        f''.split()).returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--portConfig', help="path to portConfig file", default="Emulator/config/port_config.json")
    parser.add_argument('-i', '--importDiode', help="launch emulator as the import variant", action="store_true")
    port_config = parser.parse_args().portConfig
    import_diode = parser.parse_args().importDiode
    start_emulator(port_config, import_diode)
