#!/bin/bash
set -eux

python3 -m nose --with-xunit --xunit-file=test/interface_integration_test_results.xml  test/mgmt_interface_integration_tests.py

