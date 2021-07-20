# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import json
import subprocess
import argparse


def start_emulator(port_config_path, is_import=False):
    with open(port_config_path) as file:
        port_map = json.load(file)["routingTable"]
    ingress_ports = [port["ingressPort"] for port in port_map]
    ports_cmd = "".join([f"-p {port}:{port}/udp " for port in ingress_ports])
    subprocess.Popen(
        f'docker run -v $(pwd)/{port_config_path}:/usr/src/app/portConfig.json {ports_cmd} --env IMPORTDIODE={is_import} -d emulator',
        shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--portConfig', help="path to portConfig file", default="config/portConfig.json")
    parser.add_argument('-i', '--importDiode', help="launch the emulator as the import variant", action="store_true")
    port_config = parser.parse_args().portConfig
    import_flag = parser.parse_args().importDiode
    start_emulator(port_config, import_flag)
