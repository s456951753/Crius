import unittest
import Utils.numeric_utils as nu
import datetime


class MyTestCase(unittest.TestCase):
    def test_convert_stock_symbol_successful(self):
        self.assertEqual(nu.get_converted_stock_code('000690.SZ'), '000690.XSHE')
        self.assertEqual(nu.get_converted_stock_code('603328.SH'), '603328.XSHG')
        self.assertEqual(nu.get_converted_stock_code('000690.XSHE'), '000690.SZ')
        self.assertEqual(nu.get_converted_stock_code('603328.XSHG'), '603328.SH')

    def test_stock_symbol_validation_failed(self):
        with self.assertRaises(nu.SymbolInvalidException):
            nu.get_converted_stock_code("asd9zCv&*()ds/.")

    def test_get_closest_half_year_successful(self):
        self.assertEqual(nu.get_closest_half_year(), "20191231")
        self.assertEqual(nu.get_closest_half_year("20000630"), "20000630")
        self.assertEqual(nu.get_closest_half_year("19751231"), "19751231")
        self.assertEqual(nu.get_closest_half_year("20200101"), "20191231")
        self.assertEqual(nu.get_closest_half_year("30220709"), "30220630")

    def test_get_list_of_converted_stock_code(self):
        self.assertEqual(nu.get_list_of_converted_stock_code(['000690.SZ', '603328.SH', '000690.XSHE', '603328.XSHG']),
                         ['000690.XSHE', '603328.XSHG', '000690.SZ', '603328.SH'])


if __name__ == '__main__':
    unittest.main()
