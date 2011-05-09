#!/var/local/python237/bin/python
# -*- coding: utf-8 -*-
# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Authors:
#
# Alex Ghica, Finsiel Romania
# Cornel Nitu, Finsiel Romania
#

import unittest
import MySQLConnector, SQLStatements
import time

class TestSQL(unittest.TestCase, MySQLConnector.MySQLConnector):

    def _timed_query(self, statement):
        starttime = time.time()
        res = self._query(statement)
        endtime = time.time()
        print endtime-starttime, statement.replace('\n',' ')
        print "-------------------------------------------"
        return res

    def setUp(self):
        self._open('', 'localhost','gemetread','buhbuh','gemet2008')

    def tearDown(self):
        self._close()

    def test_get_languages(self):
        """ test get languages"""
	self._timed_query(SQLStatements.sql_get_namespaces())

    def test_get_concept_languages(self):
        """ test get languages"""
	self._timed_query(SQLStatements.sql_get_concept_languages(1, 7))

    def test_get_themes(self):
        """ test get languages"""
	self._timed_query(SQLStatements.sql_get_themes(3, 'en', 'utf8_general_ci'))


if __name__ == '__main__':
    unittest.main()
