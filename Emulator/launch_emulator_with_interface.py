# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import subprocess


def start_emulator_with_interface():
    subprocess.Popen(
        f'docker run -v /var/run/docker.sock:/var/run/docker.sock '
        f'           -v "$(pwd)":"$(pwd)"'
        f'           -p 172.17.0.1:8081:8081 '
        f'           -d emulatorinterface',
        shell=True)


if __name__ == "__main__":
    start_emulator_with_interface()