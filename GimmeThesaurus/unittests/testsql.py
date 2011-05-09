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
import DatabaseManager, SQLStatements

class DBConnection:
    def __init__(self, db_host, db_user, db_password, db_name, db_port='3306'):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = int(db_port)

class TestSQL(unittest.TestCase, DatabaseManager.DatabaseManager):

    def setUp(self):
        conn = DBConnection('localhost','gemetread','buhbuh','gemet2008')
        self.openConnection(conn)

    def tearDown(self):
        self.closeConnection()

    def testConnection(self):
        """ Overrides the one in DatabaseManager, so it is not run as a unittest
        """

    def test_get_namespaces(self):
        """ test get namespaces - This will change over time :-("""
	err, res, msg  = self.query(SQLStatements.sql_get_namespaces())
        correct = (
          {'namespace_version': 'GEMET - Concepts, version 2.3, 2009-07-13', 'namespace_id': 1L, 'namespace_uri': 'http://www.eionet.europa.eu/gemet/concept/', 'namespace_type': 'http://www.w3.org/2004/02/skos/core#Concept', 'namespace_name': 'Concepts'},
          {'namespace_version': 'GEMET - Super groups, version 2.3, 2009-07-13', 'namespace_id': 2L, 'namespace_uri': 'http://www.eionet.europa.eu/gemet/supergroup/', 'namespace_type': 'http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#SuperGroup', 'namespace_name': ''},
          {'namespace_version': 'GEMET - Groups, version 2.3, 2009-07-13', 'namespace_id': 3L, 'namespace_uri': 'http://www.eionet.europa.eu/gemet/group/', 'namespace_type': 'http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#Group', 'namespace_name': 'Groups'},
          {'namespace_version': 'GEMET - Themes, version 2.3, 2009-07-13', 'namespace_id': 4L, 'namespace_uri': 'http://www.eionet.europa.eu/gemet/theme/', 'namespace_type': 'http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#Theme', 'namespace_name': 'Themes'},
          {'namespace_version': 'GEMET - INSPIRE themes, version 1.0, 2008-06-01', 'namespace_id': 5L, 'namespace_uri': 'http://inspire.jrc.it/theme/', 'namespace_type': '', 'namespace_name': 'Inspire Themes'},
          {'namespace_version': 'Version 0.1', 'namespace_id': 6L, 'namespace_uri': 'http://en.wikipedia.org/wiki/Names_of_European_cities_in_different_languages#', 'namespace_type': '', 'namespace_name': 'European Cities'}
        )
        self.assertEquals(res, correct)

    def test_get_concept_languages(self):
        """ test get languages for concept 7 in namespace 1"""
	err, res, msg  = self.query(SQLStatements.sql_get_concept_languages(1, 7))
        correct = (
          {'langcode': 'ar'}, {'langcode': 'bg'}, {'langcode': 'cs'}, {'langcode': 'da'},
          {'langcode': 'de'}, {'langcode': 'el'}, {'langcode': 'en'}, {'langcode': 'en-US'},
          {'langcode': 'es'}, {'langcode': 'et'}, {'langcode': 'eu'}, {'langcode': 'fi'},
          {'langcode': 'fr'}, {'langcode': 'ga'}, {'langcode': 'hu'}, {'langcode': 'it'},
          {'langcode': 'lt'}, {'langcode': 'lv'}, {'langcode': 'mt'}, {'langcode': 'nl'},
          {'langcode': 'no'}, {'langcode': 'pl'}, {'langcode': 'pt'}, {'langcode': 'ro'},
          {'langcode': 'ru'}, {'langcode': 'sk'}, {'langcode': 'sl'}, {'langcode': 'sv'}
        )
        self.assertEquals(res, correct)

    def test_get_themes(self):
        """ get themes"""
	err, res, msg  = self.query(SQLStatements.sql_get_themes(3, 'en', 'utf8_general_ci'))
        correct = [96L, 234L, 1062L, 618L, 893L, 1349L, 2504L, 10114L, 2711L, 10111L, 13109L, 14980L, 10117L, 3875L, 4125L, 4281L, 1922L, 4630L, 4750L, 4856L, 6237L, 10112L, 7007L, 7136L, 10118L, 7243L, 7779L, 7956L, 14979L, 8575L, 8603L, 9117L]
        list_of_themeids = [ x['theme_id'] for x in res]
        self.assertEquals(list_of_themeids, correct)

################
# Disabled because Mysql doesn't return the data in UTF-8
    def test_get_properties_as_rdf(self):
        """ get rdf for concept 250"""
        err, res, msg  = self.query(SQLStatements.sql_get_properties_as_rdf(1, 250))
        correct = (
          {'langcode': '', 'is_resource': 1L, 'uri': 'http://www.w3.org/2004/02/skos/core#broader', 'value': 'http://www.eionet.europa.eu/gemet/concept/6817'},
          {'langcode': '', 'is_resource': 1L, 'uri': 'http://www.w3.org/2004/02/skos/core#broader', 'value': 'http://www.eionet.europa.eu/gemet/group/8575'},
          {'langcode': '', 'is_resource': 1L, 'uri': 'http://www.w3.org/2004/02/skos/core#broader', 'value': 'http://www.eionet.europa.eu/gemet/theme/7'},
          {'langcode': '', 'is_resource': 1L, 'uri': 'http://www.w3.org/2004/02/skos/core#broader', 'value': 'http://www.eionet.europa.eu/gemet/theme/33'},
          {'langcode': 'bg', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#definition', 'value': '\xd0\xa1\xd0\xb8\xd1\x81\xd1\x82\xd0\xb5\xd0\xbc\xd0\xb0 \xd0\xb8\xd0\xbb\xd0\xb8 \xd0\xbf\xd1\x80\xd0\xbe\xd1\x86\xd0\xb5\xd1\x81 \xd0\xb7\xd0\xb0 \xd0\xba\xd0\xbe\xd0\xbd\xd1\x82\xd1\x80\xd0\xbe\xd0\xbb\xd0\xb8\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb5 \xd0\xbd\xd0\xb0 \xd1\x82\xd0\xb5\xd0\xbc\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd1\x83\xd1\x80\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xb8 \xd0\xbf\xd0\xbe\xd0\xbd\xd1\x8f\xd0\xba\xd0\xbe\xd0\xb3\xd0\xb0 \xd0\xbd\xd0\xb0 \xd0\xb2\xd0\xbb\xd0\xb0\xd0\xb6\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x82\xd0\xb0 \xd0\xb8 \xd1\x87\xd0\xb8\xd1\x81\xd1\x82\xd0\xbe\xd1\x82\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbd\xd0\xb0 \xd0\xb2\xd1\x8a\xd0\xb7\xd0\xb4\xd1\x83\xd1\x85\xd0\xb0 \xd0\xb2 \xd0\xba\xd1\x8a\xd1\x89\xd0\xb0 \xd0\xb8 \xd1\x82.\xd0\xbd.'},
          {'langcode': 'en', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#definition', 'value': 'A system or process for controlling the temperature and sometimes the humidity and purity of the air in a house, etc.\r\n(Source: CED)'},
          {'langcode': 'pl', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#definition', 'value': 'system kontrolowania temperatury, czasem wilgotno\xc5\x9bci i czysto\xc5\x9bci powietrza w pomieszczeniach'},
          {'langcode': 'ru', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#definition', 'value': '\xd0\xa1\xd0\xb8\xd1\x81\xd1\x82\xd0\xb5\xd0\xbc\xd0\xb0 \xd0\xb8\xd0\xbb\xd0\xb8 \xd0\xbf\xd1\x80\xd0\xbe\xd1\x86\xd0\xb5\xd1\x81\xd1\x81 \xd0\xba\xd0\xbe\xd0\xbd\xd1\x82\xd1\x80\xd0\xbe\xd0\xbb\xd1\x8f \xd0\xb7\xd0\xb0 \xd1\x82\xd0\xb5\xd0\xbc\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd1\x83\xd1\x80\xd0\xbe\xd0\xb9 \xd0\xb8 \xd0\xb8\xd0\xbd\xd0\xbe\xd0\xb3\xd0\xb4\xd0\xb0 \xd0\xb7\xd0\xb0 \xd0\xb2\xd0\xbb\xd0\xb0\xd0\xb6\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c\xd1\x8e \xd0\xb8 \xd1\x87\xd0\xb8\xd1\x81\xd1\x82\xd0\xbe\xd1\x82\xd0\xbe\xd0\xb9 \xd0\xb2\xd0\xbe\xd0\xb7\xd0\xb4\xd1\x83\xd1\x85\xd0\xb0 \xd0\xb2 \xd0\xb4\xd0\xbe\xd0\xbc\xd0\xb5 \xd0\xb8 \xd0\xbf\xd1\x80.'},
          {'langcode': 'sl', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#definition', 'value': 'Sistem ali proces uravnavanja temperature in v\xc4\x8dasih tudi vlage in \xc4\x8distosti zraka v hi\xc5\xa1i, itd.\n(Vir: CED)'},
          {'langcode': 'ar', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': '\xd8\xaa\xd9\x83\xd9\x8a\xd9\x8a\xd9\x81 \xd8\xa7\xd9\x84\xd9\x87\xd9\x88\xd8\xa7\xd8\xa1'},
          {'langcode': 'bg', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': '\xd0\x9a\xd0\xbb\xd0\xb8\xd0\xbc\xd0\xb0\xd1\x82\xd0\xb8\xd0\xb7\xd0\xb8\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb5 (\xd0\xba\xd0\xbe\xd0\xbd\xd0\xb4\xd0\xb8\xd1\x86\xd0\xb8\xd0\xbe\xd0\xbd\xd0\xb8\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb5) \xd0\xbd\xd0\xb0 \xd0\xb2\xd1\x8a\xd0\xb7\xd0\xb4\xd1\x83\xd1\x85\xd0\xb0'},
          {'langcode': 'cs', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'klimatizace'},
          {'langcode': 'da', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'luftkonditionering'},
          {'langcode': 'de', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'Klimatisierung'},
          {'langcode': 'el', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': '\xce\xba\xce\xbb\xce\xb9\xce\xbc\xce\xb1\xcf\x84\xce\xb9\xcf\x83\xce\xbc\xcf\x8c\xcf\x82'},
          {'langcode': 'en', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'air conditioning'},
          {'langcode': 'en-US', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'air conditioning'},
          {'langcode': 'es', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'acondicionamiento del aire'},
          {'langcode': 'et', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': '\xc3\xb5hu konditsioneerimine'},
          {'langcode': 'eu', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'aire-girotze'},
          {'langcode': 'fi', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'ilmastointi'},
          {'langcode': 'fr', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'climatisation'},
          {'langcode': 'ga', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'aerch\xc3\xb3iri\xc3\xba'},
          {'langcode': 'hu', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'l\xc3\xa9gkondicion\xc3\xa1l\xc3\xa1s'},
          {'langcode': 'it', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': "condizionamento dell'aria"},
          {'langcode': 'lt', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'oro kondicionavimas'},
          {'langcode': 'lv', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'gaisa kondicion\xc4\x93\xc5\xa1ana'},
          {'langcode': 'mt', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'kondizzjonament tal-arja'},
          {'langcode': 'nl', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'luchtverversing'},
          {'langcode': 'no', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'luftkondisjonering'},
          {'langcode': 'pl', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'klimatyzacja'},
          {'langcode': 'pt', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'ar condicionado'},
          {'langcode': 'ro', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'aer condi\xc5\xa3ionat'},
          {'langcode': 'ru', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': '\xd0\xba\xd0\xbe\xd0\xbd\xd0\xb4\xd0\xb8\xd1\x86\xd0\xb8\xd0\xbe\xd0\xbd\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb2\xd0\xbe\xd0\xb7\xd0\xb4\xd1\x83\xd1\x85\xd0\xb0'},
          {'langcode': 'sk', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'klimatiz\xc3\xa1cia'},
          {'langcode': 'sl', 'is_resource': 0L, 'uri': 'http://www.w3.org/2004/02/skos/core#prefLabel', 'value': 'klimatizacija'}
        )
        self.assertEquals(res, correct)



if __name__ == '__main__':
    unittest.main()
