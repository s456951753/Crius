import unittest
import Utils.numeric_utils as nu


class MyTestCase(unittest.TestCase):
    def test_convert_successful(self):
        self.assertEqual(nu.get_converted_stock_code('000690.SZ'), '000690.XSHE')
        self.assertEqual(nu.get_converted_stock_code('603328.SH'), '603328.XSHG')
        self.assertEqual(nu.get_converted_stock_code('000690.XSHE'), '000690.SZ')
        self.assertEqual(nu.get_converted_stock_code('603328.XSHG'), '603328.SH')

    def test_validation_failed(self):
        with self.assertRaises(nu.NameInvalidException):
            nu.get_converted_stock_code("asd9zCv&*()ds/.")


if __name__ == '__main__':
    unittest.main()
