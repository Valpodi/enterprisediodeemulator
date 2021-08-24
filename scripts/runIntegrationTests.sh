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

python3 -m nose --with-xunit --xunit-file=test/emulator_test_results.xml -v \
        Emulator/ \
        test/
