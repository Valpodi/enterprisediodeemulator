# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import yaml
import subprocess
import argparse


def start_emulator():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--portConfig', help="path to portConfig file")
    port_config_path = parser.parse_args().portConfig or "config/portConfig.yaml"
    with open(port_config_path) as file:
        port_map = yaml.load(file, Loader=yaml.FullLoader)["streamToPortMap"]
    ports = ""
    for i in range(len(port_map)):
        ports += f"-p {port_map[i]['srcPort']}:{port_map[i]['srcPort']}/udp "
    subprocess.Popen(f'docker run -v $(pwd)/config/portConfig.yaml:/portConfig.yaml {ports} -d emulator', shell=True)


if __name__ == "__main__":
    start_emulator()
