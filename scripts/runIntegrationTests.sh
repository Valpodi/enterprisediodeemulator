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

./scripts/buildInterfaceAndEmulator.sh

pushd test
export IMPORT_DIODE=False
export RESULT_FILENAME="emulator_test_results.xml"
export PYTHON_SCRIPT="/tmp/emulator_tests.py"
docker-compose -p emulator up --exit-code-from tester --build
docker-compose -p emulator down

python3 -m nose --with-xunit --xunit-file=test/verify_config_unit_test_results.xml Emulator/verify_config_tests.py
python3 -m nose --with-xunit --xunit-file=test/interface_unit_test_results.xml Emulator/mgmt_interface_tests.py
python3 -m nose --with-xunit --xunit-file=test/interface_integration_test_results.xml test/mgmt_interface_integration_tests.py

pushd Emulator
docker build --no-cache -t emulator -f Dockerfile .
CONTAINER_ID=$(python3 ../launch_emulator.py -p ../test/portSpanTooLarge.json)
sleep 1
EXPECTED='            "ExitCode": 1,'
OUTPUT=$(docker inspect "${CONTAINER_ID}" | grep ExitCode)
if [[ "$OUTPUT" != "$EXPECTED" ]]; then
  exit 1
fi
docker stop emulator
docker rm emulator
popd

python3 -m nose --with-xunit --xunit-file=test/e2e_test_results.xml test/e2e_test_interface_and_emulator.py
