import unittest

import propsapi.sources.housecanary as hc


class TestGetSewer(unittest.TestCase):
    def test_septic(self):
        self.assertEqual(hc.get_sewer('septic'), ('septic', None))

    def test_noseptic(self):
        self.assertNotEqual(hc.get_sewer('123 fake'), ('septic', None))

    def test_unknown(self):
        self.assertEqual(hc.get_sewer('unknown'), ('yes', None))

    def test_null(self):
        self.assertEqual(hc.get_sewer('null'), (None, None))
