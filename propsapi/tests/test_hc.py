"""
Test suite for the (mocked) HouseCanary API interface.
"""
import unittest
import propsapi.sources.hcapi as hc


class TestGetSewer(unittest.TestCase):
    def test_septic(self):
        response, error = hc.get_sewer('septic')
        self.assertEqual(response, 'septic')
        self.assertIsNone(error)

    def test_noseptic(self):
        response, error = hc.get_sewer('123 fake')
        self.assertNotEqual(response, 'septic')
        self.assertIsNone(error)

    def test_unknown(self):
        response, error = hc.get_sewer('unknown')
        self.assertEqual(response, 'yes')
        self.assertIsNone(error)

    def test_null(self):
        response, error = hc.get_sewer('null')
        self.assertIsNone(response)
        self.assertIsNone(error)

    def test_noinfo(self):
        response, error = hc.get_sewer('noinfo')
        self.assertIsNone(response)
        self.assertEqual(error, 'no content')

    def test_error(self):
        response, error = hc.get_sewer('error')
        self.assertIsNone(response)
        self.assertEqual(error, 'error in source')
