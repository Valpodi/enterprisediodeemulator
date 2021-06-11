# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import yaml
import subprocess
import argparse


def start_emulator(port_config_path, is_import=False):
    with open(port_config_path) as file:
        port_map = yaml.load(file, Loader=yaml.FullLoader)["routingTable"]
    ports_cmd = ""
    ports = []
    for i in range(len(port_map)):
        port = port_map[i].split(":")[0]
        ports.append(port)
        ports_cmd += f"-p {port}:{port}/udp "
    subprocess.Popen(
        f'docker run -v $(pwd)/{port_config_path}:/usr/src/app/portConfig.yaml {ports_cmd} --env IMPORTDIODE={is_import} -d emulator',
        shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--portConfig', help="path to portConfig file", default="config/portConfig.yaml")
    parser.add_argument('-i', '--importDiode', help="lauch the emulator as the import variant", action="store_true")
    port_config = parser.parse_args().portConfig
    import_flag = parser.parse_args().importDiode
    start_emulator(port_config, import_flag)
