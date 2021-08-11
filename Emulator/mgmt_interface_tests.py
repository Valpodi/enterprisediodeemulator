# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
import json
from mgmt_interface import Interface


class MgmtInterfaceTests(unittest.TestCase):
    def test_do_config_get_returns_config_file(self):
        Interface._file_exists = lambda filepath: True
        Interface._get_file_content = lambda filepath: {
            "ingress": {},
            "egress": {},
            "routingTable": []
        }
        response = Interface().do_config_get()

        self.assertEqual({"ingress": {}, "egress": {}, "routingTable": []}, json.loads(response.get_data()))
        self.assertEqual(200, response.status_code)

    def test_diode_power_on_returns_status_completed(self):
        Interface._file_exists = lambda filepath: True
        Interface._power_on_diode = lambda: {"status": "Diode powered on"}
        Interface._remove_container = lambda: True
        response = Interface.do_power_on_procedure()

        self.assertEqual("Diode powered on", json.loads(response.get_data())["status"])
        self.assertEqual(200, response.status_code)

    def test_diode_power_on_returns_500_when_emulator_cannot_be_powercyled(self):
        Interface._remove_container = lambda: False
        response = Interface.do_power_on_procedure()

        self.assertEqual(b"Server Error", response.get_data())
        self.assertEqual(500, response.status_code)

    def test_diode_power_off_returns_status_completed(self):
        Interface._power_off_diode = lambda: {"status": "completed"}
        response = Interface.do_power_off_procedure()

        self.assertEqual("completed", json.loads(response.get_data())["status"])
        self.assertEqual(200, response.status_code)

    def test_diode_get_schema_returns_config_schema(self):
        Interface._file_exists = lambda filepath: True
        schema = {"properties": {"ingress": {"type": "object"},
                                 "egress": {"type": "object"},
                                 "routingTable": {"type": "array"}},
                  "required": ["ingress", "egress", "routingTable"]}
        Interface._get_file_content = lambda filepath: schema
        response = Interface.get_config_schema()

        self.assertEqual(schema, json.loads(response.get_data()))
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MgmtInterfaceTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
