# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file
import signal
import subprocess


def shutdown_handler(signum, frame):
    subprocess.run("docker stop emulator".split())
    raise Exception("shutdown")


def start_interface():
    subprocess.run(
        f'docker run -v /var/run/docker.sock:/var/run/docker.sock '
        f'           -v "$(pwd)":"$(pwd)"'
        f'           -p 8081:8081 '
        f'           --name=interface '
        f'           --rm '
        f'           emulatorinterface /bin/bash -c "pushd $(pwd) && python3 /usr/src/app/http_server.py"',
        shell=True)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_handler)
    start_interface()
