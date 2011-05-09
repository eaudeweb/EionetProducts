# encoding: utf-8
#
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
# Agency (EEA).  Portions created by Eau de Web are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Authors:
#
# Alex Morega, Eau de Web

import unittest
from urllib2 import urlopen
import re

base_url = 'http://localhost:8080/gemet'
#base_url = 'http://gemet.eaudeweb.ro/gemet'

class TestPages(unittest.TestCase):
    def do_page_tests(self, requests, must_have=[], must_not_have=[]):
        for request in requests:
            page = urlopen(base_url + request)
            self.failUnless('utf-8' in page.info()['content-type'].lower(), 'page encoding is not UTF-8')
            data = page.read().decode('utf-8')
            page.close()
            for substring in must_have:
                assert substring in data, 'string "%s" not found in page "%s"!' % (substring.encode('utf-8'), request)
            for substring in must_not_have:
                assert substring not in data, u'string "%s" should not be in page "%s"!' % (substring.encode('utf-8'), request)

    def test_homepage(self):
        # lang: en
        self.do_page_tests(['', '/', '/index_html', '/?langcode=en'],
            must_have=['Themes list', 'building', 'industry', 'Select language:', 'en', 'ru'])
        # lang: ru
        self.do_page_tests(['?langcode=ru', '/?langcode=ru', '/index_html?langcode=ru'],
            must_have=['Themes list', u'строительство', u'промышленность', 'Select language:', 'en', 'ru'])

    def test_theme_page(self):
        # lang: en
        self.do_page_tests(['/theme_concepts?th=24&langcode=en', '/theme_concepts?th=24'],
            must_have=['Concepts list for', 'noise, vibrations', 'air traffic', 'airborne noise'])
        # lang: ru
        self.do_page_tests(['/theme_concepts?th=24&langcode=ru'],
            must_have=['Concepts list for', u'шум, вибрация', u'автомобильная шина', u'акустическое свойство'])
        # pagination
        self.do_page_tests(['/theme_concepts?letter=19&th=24&ns=4'],
            must_have=['Concepts list for', 'noise, vibrations', 'sonic boom', 'sound transmission'])
        self.do_page_tests(['/theme_concepts?letter=0&start=60&th=24'],
            must_have=['noise effect', 'silencer'],
            must_not_have=['four stroke engine', 'two-stroke engine'])

    def test_concept_page(self):
        # lang: en
        self.do_page_tests(['/concept?cp=617&langcode=en', '/concept?cp=617'],
            must_have=['atmosphere', 'surrounding the Earth', 'narrower terms', 'atmospheric structure',
            u'atmosfär', 'ATMOSPHERE (air, climate)'])
        # lang: ru
        self.do_page_tests(['/concept?cp=617&langcode=ru'],
            must_have=[u'атмосфера', u'поверхность Земли', 'narrower terms', u'структура атмосферы',
                       u'atmosfär', u'АТМОСФЕРА (воздух, климат)', u'воздух'])

        # other namespaces
        self.do_page_tests(['/concept?cp=11&langcode=en&ns=5'],
            must_have=['Land cover'],
            must_not_have=['abiotic factor'])

    def test_alphabetic(self):
        # lang: en
        self.do_page_tests(['/alphabetic', '/alphabetic?langcode=en'],
            must_have=['acid deposition', 'abandoned vehicle'],
            must_not_have=['alkane'])
        # lang: ru
        self.do_page_tests(['/alphabetic?langcode=ru'],
            must_have=[u'автомобиль, направляемый на переплавку'])
        self.do_page_tests(['/alphabetic?letter=14&langcode=ru'],
            must_have=[u'массовый отдых'],
            must_not_have=[u'многоквартирный жилой дом'])
        self.do_page_tests(['/alphabetic?letter=14&start=180&langcode=ru'],
            must_have=[u'многоквартирный жилой дом'])

    def test_groups(self):
        # language: en
        self.do_page_tests(['/groups', '/groups?langcode=en'],
            must_have=['NATURAL ENVIRONMENT, ANTHROPIC ENVIRONMENT', 'ACCESSORY LISTS',
            'BIOSPHERE (organisms, ecosystems)', 'INDUSTRY, CRAFTS; TECHNOLOGY; EQUIPMENTS'])
        # language: ru
        self.do_page_tests(['/groups?langcode=ru'],
            must_have=[u'ВСПОМОГАТЕЛЬНЫЕ ТЕРМИНЫ', u'СОЦИАЛЬНЫЕ АСПЕКТЫ, МЕРЫ ЭКОЛОГИЧЕСКОЙ ПОЛИТИКИ',
            u'ЗЕМЛЯ (ландшафт, география)', u'ЗАКОНОДАТЕЛЬСТВО, НОРМЫ, КОНВЕНЦИИ'])

    def test_relations(self):
        # language: en
        self.do_page_tests(['/relations?tree=eJwzsTA1AwACHADY', '/relations?tree=eJwzsTA1AwACHADY&langcode=en'],
            must_have=['LITHOSPHERE (soil, geological processes)', 'pedosphere'],
            must_not_have=['seismic activity'])
        self.do_page_tests(['/relations?tree=eJwzsTA10zE2M7EAAAk-Adk_', '/relations?tree=eJwzsTA10zE2M7EAAAk-Adk_&langcode=en'],
            must_have=['LITHOSPHERE (soil, geological processes)', 'pedosphere', 'seismic activity'])
        # language: ru
        self.do_page_tests(['/relations?tree=eJwzsTA1AwACHADY&langcode=ru'],
            must_have=[u'ЛИТОСФЕРА (почва, геологические процессы)', u'геологический процесс'],
            must_not_have=[u'седиментация (геол.)'])
        self.do_page_tests(['/relations?tree=eJwzsTA10zE2M7EAAAk-Adk_&langcode=ru'],
            must_have=[u'ЛИТОСФЕРА (почва, геологические процессы)', u'геологический процесс', u'седиментация (геол.)'])

    def test_search(self):
        self.do_page_tests(['/search?query=air&langcode=en', '/search?query=air'],
            must_have=['air temperature', 'air quality management', 'environmental management'])
        self.do_page_tests(['/search?langcode=ru&query=%D0%B2%D0%BE%D0%B7%D0%B4%D1%83%D1%85'],
            must_have=[u'атмосфера'])

    def test_link_to_rdf(self):
        def get(url):
            page = urlopen(base_url + url)
            data = page.read().decode('utf-8')
            page.close()
            return data

        data = get('/concept?ns=1&cp=6817')
        pattern = (r'\<link\s*rel="alternate"\s*type="application/rdf\+xml"\s*'
                   r'title="RDF"\s*href="http\://www\.eionet\.europa\.eu'
                   r'/gemet/concept/6817"\s*/\>')
        self.assertTrue(re.search(pattern, data, re.DOTALL))

        data = get('/concept?ns=4&cp=13')
        pattern = (r'\<link\s*rel="alternate"\s*type="application/rdf\+xml"\s*'
                   r'title="RDF"\s*href="http\://www\.eionet\.europa\.eu'
                   r'/gemet/theme/13"\s*/\>')
        self.assertTrue(re.search(pattern, data, re.DOTALL))

if __name__ == '__main__':
    unittest.main()
