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

python3 test/write_diode_type.py -t basic
pushd test
export RESULT_FILENAME="emulator_test_results.xml"
export PYTHON_SCRIPT="/tmp/emulator_tests.py"
docker-compose -p emulator up --exit-code-from tester --build
docker-compose -p emulator down
popd

python3 test/write_diode_type.py -t import
pushd test
export RESULT_FILENAME="import_emulator_test_results.xml"
export PYTHON_SCRIPT="/tmp/import_emulator_tests.py"
docker-compose -p emulator up --exit-code-from tester --build
docker-compose -p emulator down
popd

python3 test/write_diode_type.py -t basic
./scripts/buildInterfaceAndEmulator.sh
python3 -m nose --with-xunit --xunit-file=test/verify_config_unit_test_results.xml Emulator/verify_config_tests.py
python3 -m nose --with-xunit --xunit-file=test/verify_bitmap_unit_test_results.xml Emulator/verify_bitmap_tests.py
python3 -m nose --with-xunit --xunit-file=test/verify_control_header_unit_test_results.xml Emulator/verify_control_header_tests.py
python3 -m nose --with-xunit --xunit-file=test/interface_unit_test_results.xml Emulator/management_interface_tests.py
python3 -m nose --with-xunit --xunit-file=test/interface_integration_test_results.xml test/management_interface_integration_tests.py

#python3 -m nose --with-xunit --xunit-file=test/emulator_port_span_test_results.xml test/emulator_port_span_test.py
python3 test/write_diode_type.py -t basic
python3 -m nose --with-xunit --xunit-file=test/e2e_test_results.xml test/e2e_test_interface_and_emulator.py

python3 test/write_diode_type.py -t import
./scripts/buildInterfaceAndEmulator.sh
python3 -m nose --with-xunit --xunit-file=test/e2e_test_import_results.xml test/e2e_test_import_interface_and_emulator.py
python3 test/write_diode_type.py -t basic