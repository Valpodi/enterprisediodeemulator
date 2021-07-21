import unittest
import json
from mgmt_interface import Interface


class MgmtInterfaceTests(unittest.TestCase):
    def test_do_config_get_returns_config_file(self):
        response = Interface.do_config_get()

        self.assertEqual("config file contents", json.loads(response.get_data())["config"])
        self.assertEqual(200, response.status_code)

    def test_do_config_update_returns_status_completed(self):
        response = Interface.do_config_update()

        self.assertEqual("completed", json.loads(response.get_data())["status"])
        self.assertEqual(200, response.status_code)

    def test_diode_power_on_returns_status_completed(self):
        response = Interface.do_power_on_procedure()

        self.assertEqual("completed", json.loads(response.get_data())["status"])
        self.assertEqual(200, response.status_code)

    def test_diode_power_off_returns_status_completed(self):
        response = Interface.do_power_off_procedure()

        self.assertEqual("completed", json.loads(response.get_data())["status"])
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(MgmtInterfaceTests)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
