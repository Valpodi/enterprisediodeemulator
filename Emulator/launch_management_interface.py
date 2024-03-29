# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import signal
import subprocess
import argparse


def shutdown_handler(signum, frame):
    print("\nINFO: Shutting down interface server...")
    subprocess.run("docker stop emulator".split())
    subprocess.run("docker rm emulator".split())
    raise Exception("shutdown")


def start_interface(port, is_import_diode):
    subprocess.run(
        f'docker run -v /var/run/docker.sock:/var/run/docker.sock '
        f'           -v "$(pwd)":"$(pwd)"'
        f'           -p {port}:8081 '
        f'           --name=management_interface '
        f'           --rm '
        f'           --env IMPORTDIODE={is_import_diode} '
        f'           emulatorinterface /bin/bash -c "pushd $(pwd) && python3 /usr/src/app/http_server.py"',
        shell=True)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_handler)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--interfacePort', help="port to run interface server", default="8081")
    parser.add_argument('-i', '--importDiode', help="launch emulator as the import variant", action="store_true")
    interface_port = parser.parse_args().interfacePort
    import_diode = parser.parse_args().importDiode
    start_interface(interface_port, import_diode)
