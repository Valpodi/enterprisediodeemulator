#!/bin/bash
set -eux

function cleanup()
{
  echo "cleanup! reset all file permissions to host owned"
  HOSTUID=`id -u`
  pushd src || true
  docker-compose -p emulator down
  docker run -v "$(pwd)":"$(pwd)" "centos:7" /bin/bash -c "chown -R $HOSTUID $(pwd)"
}

pushd test
export IMPORT_DIODE=False
export RESULT_FILENAME="emulator_test_results.xml"
export PYTHON_SCRIPT="/tmp/emulatorTests.py"
docker-compose -p emulator up --exit-code-from tester --build

export IMPORT_DIODE=True
export RESULT_FILENAME="import_emulator_test_results.xml"
export PYTHON_SCRIPT="/tmp/importEmulatorTests.py"
docker-compose -p emulator up --exit-code-from tester --build
popd

pushd Emulator
docker build --no-cache -t emulator -f Dockerfile .
CONTAINER_ID=$(python3 ../launchEmulator.py -p ../test/portSpanTooLarge.json)
sleep 1
EXPECTED='            "ExitCode": 1,'
OUTPUT=$(docker inspect "${CONTAINER_ID}" | grep ExitCode)
if [[ "$OUTPUT" != "$EXPECTED" ]]; then
  exit 1
fi
popd

./scripts/runInterfaceIntegrationTests.sh