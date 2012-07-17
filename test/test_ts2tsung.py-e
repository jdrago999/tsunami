#!/usr/bin/env python

import os
import unittest2 as unittest
from doctest import Example
from lxml import etree
from lxml.doctestcompare import LXMLOutputChecker

class TestFullLoadTestingDSL(unittest.TestCase):
    def assertXmlFilesEqual(self, result_filename, expected_filename):
        with open(result_filename) as rf:
            got = rf.read()
        with open(expected_filename) as ef:
            want = ef.read()

        checker = LXMLOutputChecker()
        if not checker.check_output(want, got, 0):
            message = checker.output_difference(Example("", got), want, 0)
            raise AssertionError(message)

    def assertFilesEqual(self, expected_filename, result_filename):
        with open(result_filename) as rf:
            got = rf.read()
        with open(expected_filename) as ef:
            want = ef.read()
        self.assertEqual(got, want)

    def test_simple(self):
        result = os.system("python ts2tsung.py --from=test/files/simple.ts " + 
            "--to=/tmp/output.xml")
        self.assertEqual(result, 0 )
        self.assertTrue(os.path.exists("/tmp/output.xml"))
        self.assertXmlFilesEqual( "/tmp/output.xml", \
            "test/files/simple_working.xml" )
        self.assertFilesEqual("/tmp/output/_pin.csv",  
                              "test/files/simple/_pin.csv")

        os.remove("/tmp/output.xml")
        os.remove("/tmp/output/_pin.csv")
        os.rmdir("/tmp/output")
if __name__ == '__main__':
    unittest.main()
