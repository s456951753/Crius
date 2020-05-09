import unittest
import Utils.configuration_file_service as config_service


class MyTestCase(unittest.TestCase):
    def test_getProperty(self):
        self.assertEqual(
            config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                       property_name=config_service.TS_TOKEN_NAME),
            "0123456789abcdeFG"
        )


if __name__ == '__main__':
    unittest.main()
