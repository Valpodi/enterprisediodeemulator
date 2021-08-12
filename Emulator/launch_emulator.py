# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import json
import subprocess
import argparse
import os


def start_emulator(port_config_path):
    with open(port_config_path) as config_file:
        port_map = json.load(config_file)["routingTable"]
    ingress_ports = [port["ingressPort"] for port in port_map]
    ports_cmd = "".join([f"-p {port}:{port}/udp " for port in ingress_ports])
    return subprocess.run(
        f'docker run --name=emulator -v {os.getcwd()}/{port_config_path}:/usr/src/app/config/port_config.json {ports_cmd} -d emulator'.split()).returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--portConfig', help="path to portConfig file", default="Emulator/config/port_config.json")
    port_config = parser.parse_args().portConfig
    start_emulator(port_config)
