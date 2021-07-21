# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import subprocess


def start_emulator_with_interface():
    subprocess.Popen(
        f'docker run -v /var/run/docker.sock:/var/run/docker.sock '
        f'           -p 8081:8081 '
        f'           -d emulatorinterface',
        shell=True)


if __name__ == "__main__":
    start_emulator_with_interface()
