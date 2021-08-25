# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
import json
from management_interface import ManagementInterface, DiodePowerCycleError


class MgmtInterfaceTests(unittest.TestCase):
    def test_do_config_get_returns_config_file(self):
        ManagementInterface._file_exists = lambda filepath: True
        ManagementInterface._get_file_content = lambda filepath: {
            "ingress": {},
            "egress": {},
            "routingTable": []
        }
        response = ManagementInterface().get_config_information()

        self.assertEqual({"ingress": {}, "egress": {}, "routingTable": []}, json.loads(response.get_data()))
        self.assertEqual(200, response.status_code)

    def test_diode_power_on_returns_status_completed(self):
        ManagementInterface._file_exists = lambda filepath: True
        ManagementInterface._power_on_diode = lambda: {"Status": "Diode powered on"}
        ManagementInterface._remove_container = lambda: True
        response = ManagementInterface.do_power_on()

        self.assertEqual("Diode powered on", json.loads(response.get_data())["Status"])
        self.assertEqual(200, response.status_code)

    def test_diode_power_on_raises_error_when_emulator_cannot_be_powercyled(self):
        ManagementInterface._remove_container = lambda: False
        self.assertRaises(DiodePowerCycleError, ManagementInterface.do_power_on)

    def test_diode_power_off_returns_status_completed(self):
        ManagementInterface._power_off_diode = lambda: {"Status": "completed"}
        response = ManagementInterface.do_power_off()

        self.assertEqual(b"", response.get_data())
        self.assertEqual(200, response.status_code)

    def test_diode_get_schema_returns_config_schema(self):
        ManagementInterface._file_exists = lambda filepath: True
        schema = {"properties": {"ingress": {"type": "object"},
                                 "egress": {"type": "object"},
                                 "routingTable": {"type": "array"}},
                  "required": ["ingress", "egress", "routingTable"]}
        ManagementInterface._get_file_content = lambda filepath: schema
        response = ManagementInterface.get_config_schema()

        self.assertEqual(schema, json.loads(response.get_data()))
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MgmtInterfaceTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
