# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import json
import subprocess
import argparse
import os


def start_emulator(port_config_path, is_import=False):
    with open(port_config_path) as file:
        port_map = json.load(file)["routingTable"]
    with open("Emulator/config/diode_type.json", "w") as diode_type_file:
        if is_import:
            diode_type_file.write(json.dumps({"f2 type": "import"}))
        else:
            diode_type_file.write(json.dumps({"f2 type": "basic"}))

    ingress_ports = [port["ingressPort"] for port in port_map]
    ports_cmd = "".join([f"-p {port}:{port}/udp " for port in ingress_ports])
    return subprocess.run(
        f'docker run --name=emulator -v {os.getcwd()}/{port_config_path}:/usr/src/app/config/portConfig.json {ports_cmd} -d emulator'.split()).returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--portConfig', help="path to portConfig file", default="Emulator/config/portConfig.json")
    parser.add_argument('-i', '--importDiode', help="launch the emulator as the import variant", action="store_true")
    port_config = parser.parse_args().portConfig
    import_flag = parser.parse_args().importDiode
    start_emulator(port_config, import_flag)
