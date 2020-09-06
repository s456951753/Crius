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


class Test1(TestCase):
    def test_get_table_range(self):
        self.assertEqual(dbutil.getTableRange("a", '19900101', '19950101'), ["a_1990_1994", "a_1995_1999"])
        self.assertEqual(dbutil.getTableRange("", '19900101', '19950101'), ["_1990_1994", "_1995_1999"])
        self.assertEqual(dbutil.getTableRange("", '20200101', '20200101'), ["_2020_2024"])
        self.assertEqual(dbutil.getTableRange("", '19900101', '19940101'), ["_1990_1994"])
        self.assertEqual(dbutil.getTableRange("", '19980101', '20030101'), ["_1995_1999", "_2000_2004"])
        self.assertEqual(dbutil.getTableRange("", '19980101', '19980101'), ["_1995_1999"])
        self.assertEqual(dbutil.getTableRange("", '19900228', '19900301'), ["_1990_1994"])
