__author__ = 'aardr'

import SQLDiff


def test_region_extract():
    sql_diff = getSQLDiff()
    print [dict(name=i["name"], region=i["region"]) for i in sql_diff.regions]


def test_set_search():
    sql_diff = getSQLDiff()
    sql_diff.set_search("ICPC")
    print sql_diff.search_pattern


def test_set_from_region():
    sql_diff = getSQLDiff()
    sql_diff.set_search("ICPC")
    sql_diff.set_from("DEV")
    print sql_diff.fromObject


def test_set_to_region():
    sql_diff = getSQLDiff()
    sql_diff.set_search("ICPC")
    sql_diff.set_to("TEST")
    print sql_diff.toObject


def tests():
    test_region_extract()
    test_set_search()
    test_set_from_region()
    test_set_to_region()

tests()