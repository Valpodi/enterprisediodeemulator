#!/bin/bash
set -eux

function cleanup()
{
  echo "cleanup! reset all file permissions to host owned"
  HOSTUID=`id -u`
  docker-compose -p emulator down
  docker run -v "$(pwd)":"$(pwd)" "centos:7" /bin/bash -c "chown -R $HOSTUID $(pwd)"
}

./scripts/buildInterfaceAndEmulator.sh

pushd test
export RESULT_FILENAME="emulator_test_results.xml"
export PYTHON_SCRIPT="/tmp/emulator_tests.py"
export IMPORT_DIODE=False
docker-compose -p emulator up --exit-code-from tester --build
docker-compose -p emulator down
popd

pushd test
export RESULT_FILENAME="import_emulator_test_results.xml"
export PYTHON_SCRIPT="/tmp/import_emulator_tests.py"
export IMPORT_DIODE=True
docker-compose -p emulator up --exit-code-from tester --build
docker-compose -p emulator down
popd

python3 -m nose --with-xunit --xunit-file=test/emulator_test_results.xml -v \
        Emulator/ \
        test/management_interface_integration_tests.py \
        test/emulator_port_span_test.py \
        test/e2e_test_interface_and_emulator.py \
        test/e2e_test_import_interface_and_emulator.py