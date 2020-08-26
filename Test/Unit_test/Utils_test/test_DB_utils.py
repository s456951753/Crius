import datetime
from unittest import TestCase
import Utils.DB_utils as dbutil


class Test(TestCase):
    def test_get_table_name(self):
        a = "ada"
        self.assertEqual(dbutil.getTableName(100, a), "ada_9995_10000")
        self.assertEqual(dbutil.getTableName(1991, a), "ada_1990_1994")
        self.assertEqual(dbutil.getTableName(1994, a), "ada_1990_1994")
        self.assertEqual(dbutil.getTableName(1995, a), "ada_1995_1999")
        self.assertEqual(dbutil.getTableName(1990, a), "ada_1990_1994")
        self.assertEqual(dbutil.getTableName(2001, a), "ada_2000_2004")
        self.assertEqual(dbutil.getTableName(datetime.date.today().year, a), "ada_2020_2024")
