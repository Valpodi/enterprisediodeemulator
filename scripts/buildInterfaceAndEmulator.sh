#!/bin/bash
set -eux

function cleanup()
{
echo "cleanup! reset all file permissions to host owned"
HOSTUID=`id -u`
docker-compose -p emulator down
docker run -v "$(pwd)":"$(pwd)" "centos:7" /bin/bash -c "chown -R $HOSTUID $(pwd)"
}

pushd Emulator
docker build --no-cache -t emulator -f Dockerfile .
popd

docker build -f Emulator/MgmtInterfaceDockerfile -t emulatorinterface .