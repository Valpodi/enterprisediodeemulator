# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
import json
from Emulator.mgmt_interface import Interface


class MgmtInterfaceTests(unittest.TestCase):
    def test_do_config_get_returns_config_file(self):
        Interface._get_config_file = lambda: {
            "ingress": {},
            "egress": {},
            "routingTable": []
        }
        response = Interface.do_config_get()

        self.assertEqual({"ingress": {}, "egress": {}, "routingTable": []}, json.loads(response.get_data()))
        self.assertEqual(200, response.status_code)

    def test_do_config_update_returns_status_completed(self):
        Interface._power_off_diode = lambda: {"status": "completed"}
        Interface._update_config = lambda config: None
        Interface._power_on_diode = lambda: {"status": "completed"}

        response = Interface.do_config_update("ignore")

        self.assertEqual("completed", json.loads(response.get_data())["status"])
        self.assertEqual(200, response.status_code)

    def test_diode_power_on_returns_status_completed(self):
        Interface._power_on_diode = lambda: {"status": "completed"}
        response = Interface.do_power_on_procedure()

        self.assertEqual("completed", json.loads(response.get_data())["status"])
        self.assertEqual(200, response.status_code)

    def test_diode_power_off_returns_status_completed(self):
        Interface._power_off_diode = lambda: {"status": "completed"}
        response = Interface.do_power_off_procedure()

        self.assertEqual("completed", json.loads(response.get_data())["status"])
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MgmtInterfaceTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
