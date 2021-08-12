# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import unittest
from verify_bitmap import VerifyBitmap


class VerifyBitmapTests(unittest.TestCase):
    def test_verify_bitmap(self):
        self.assertTrue(VerifyBitmap.validate())


if __name__ == '__main__':
    unittest.main()
