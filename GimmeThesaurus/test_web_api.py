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
import xmlrpclib

xmlrpc_url = 'http://localhost:8080/gemet'
#xmlrpc_url = 'http://gemet.eaudeweb.ro/gemet'

class TestXmlRpcApi(unittest.TestCase):
    def doXmlRpc(self, method, *args):
        server = xmlrpclib.ServerProxy(xmlrpc_url, allow_none=True)
        return getattr(server, method)(*args)
    
    def assertLanguageString(self, obj, language, string, startswith=False):
        """
        Verify the integrity of a LanguageString object.
        
        Specify startswith=True if you only want to check the beginning of the string.
        """
        
        self.failUnless(isinstance(obj, dict))
        self.failUnless('language' in obj.keys())
        self.failUnless('string' in obj.keys())
        self.failUnlessEqual(obj['language'], language)
        
        if startswith:
            self.failUnless(obj['string'].startswith(string))
        else:
            self.failUnlessEqual(obj['string'], string)
    
    def test_getConcept(self):
        """
        test the getConcept XML-RPC method
        """
        
        # fetch a few concepts, making sure we receive all the correct data
        
        reference_concepts = [
            {
                'uri': 'http://www.eionet.europa.eu/gemet/concept/7970',
                'thesaurus': 'http://www.eionet.europa.eu/gemet/concept/',
                'preferredLabel': {
                    'en': "space travel",
                    'pl': u"podróż kosmiczna",
                    'ru': u"космический полет",
                },
                'definition': {
                    'en': "Travel in the space beyond the earth's atmosphere",
                    'pl': u"podróż w przestrzeni poza atmosferą",
                    'ru': u"Путешествие в космосе за пределами земной атмосферы",
                }
            },
            {
                'uri': 'http://www.eionet.europa.eu/gemet/group/893',
                'thesaurus': 'http://www.eionet.europa.eu/gemet/group/',
                'preferredLabel': {
                    'en': "BIOSPHERE (organisms, ecosystems)",
                    'hu': u"BIOSZFÉRA (szervezetek, ökoszisztémák)",
                    'bg': u"биосфера (организми, екосистеми)",
                },
            },
            {
                'uri': 'http://www.eionet.europa.eu/gemet/theme/33',
                'thesaurus': 'http://www.eionet.europa.eu/gemet/theme/',
                'preferredLabel': {
                    'en': "trade, services",
                    'de': "Handel, Dienstleistungen",
                    'ru': u"торговля, услуги",
                },
            },
        ]
        
        for concept_ref in reference_concepts:
            for lang in concept_ref['preferredLabel'].keys():
                # get the concept
                concept = self.doXmlRpc('getConcept', concept_ref['uri'], lang)
                
                # see if it has the right structure
                self.failUnless(isinstance(concept, dict))
                self.failUnlessEqual(concept['uri'], concept_ref['uri'])
                self.failUnlessEqual(concept['thesaurus'], concept_ref['thesaurus'])
                
                # see if the label and definitions match
                self.assertLanguageString(concept['preferredLabel'], lang, concept_ref['preferredLabel'][lang])
                if 'definition' in concept_ref:
                    self.assertLanguageString(concept['definition'], lang, concept_ref['definition'][lang], startswith=True)
        
        # fetch a couple of non-existent concepts, to check the error messages
        bad_uris = ['http://www.eionet.europa.eu/gemet/concept/99999999', 'asdf']
        for bad_uri in bad_uris:
            try:
                self.doXmlRpc('getConcept', bad_uri)
                self.fail('No fault was received')
            except xmlrpclib.Fault, f:
                self.failUnless('Concept not found' in f.faultString)
                self.failUnless(bad_uri in f.faultString)
    
    def test_hasConcept(self):
        """
        test the hasConcept XML-RPC method
        """
        good_uris = ['http://www.eionet.europa.eu/gemet/concept/7970',
                     'http://www.eionet.europa.eu/gemet/theme/33']
        bad_uris = ['http://www.eionet.europa.eu/gemet/concept/99999999',
                    'asdf']
        
        for uri in good_uris:
            self.assertTrue(self.doXmlRpc('hasConcept', uri),
                             "hasConcept should return True: %r" % uri)
        
        for uri in bad_uris:
            self.assertFalse(self.doXmlRpc('hasConcept', uri),
                             "hasConcept should return False: %r" % uri)
    
    def test_hasRelation(self):
        """
        test the hasRelation XML-RPC method
        """
        good_relations = [
            ('http://www.eionet.europa.eu/gemet/concept/100',
             'http://www.w3.org/2004/02/skos/core#broader',
             'http://www.eionet.europa.eu/gemet/concept/13292'),

            ('http://www.eionet.europa.eu/gemet/concept/100',
             'http://www.w3.org/2004/02/skos/core#narrower',
             'http://www.eionet.europa.eu/gemet/concept/661'),

            ('http://www.eionet.europa.eu/gemet/concept/42',
             'http://www.w3.org/2004/02/skos/core#related',
             'http://www.eionet.europa.eu/gemet/concept/51'),

            ('http://www.eionet.europa.eu/gemet/concept/100',
             'http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#group',
             'http://www.eionet.europa.eu/gemet/group/96'),

            ('http://www.eionet.europa.eu/gemet/concept/100',
             'http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#theme',
             'http://www.eionet.europa.eu/gemet/theme/1'),

            ('http://www.eionet.europa.eu/gemet/group/96',
             'http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#groupMember',
             'http://www.eionet.europa.eu/gemet/concept/21'),

            ('http://www.eionet.europa.eu/gemet/theme/1',
             'http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#themeMember',
             'http://www.eionet.europa.eu/gemet/concept/13293'),
        ]
        bad_relations = [
            ('http://www.eionet.europa.eu/gemet/concept/999999999999',
             'http://www.w3.org/2004/02/skos/core#broader',
             'http://www.eionet.europa.eu/gemet/concept/13292'),

            ('http://www.eionet.europa.eu/gemet/concept/100',
             'badrelation',
             'http://www.eionet.europa.eu/gemet/concept/13292'),

            ('http://www.eionet.europa.eu/gemet/concept/100',
             'http://www.w3.org/2004/02/skos/core#broader',
             'badtarget'),

            ('badsource',
             'http://www.w3.org/2004/02/skos/core#broader',
             'http://www.eionet.europa.eu/gemet/concept/13292'),
        ]
        for relation in good_relations:
            self.assertTrue(self.doXmlRpc('hasRelation', *relation),
                            "hasRelation should return True: %r" % (relation,))
        
        for relation in bad_relations:
            self.assertFalse(self.doXmlRpc('hasRelation', *relation),
                            "hasRelation should return False: %r" % (relation,))
    
    def test_getAllConceptRelatives(self):
        """
        test the getAllConceptRelatives XML-RPC method
        """
        gemet_uri = 'http://www.eionet.europa.eu/gemet/'
        skos_uri = 'http://www.w3.org/2004/02/skos/core#'
        gemet_schema_uri = 'http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#'
        relations = {
            'narrower': skos_uri + 'narrower',
            'broader': skos_uri + 'broader',
            'related': skos_uri + 'related',
            'groupMember': gemet_schema_uri + 'groupMember',
            'group': gemet_schema_uri + 'group',
            'theme': gemet_schema_uri + 'theme',
            'themeMember': gemet_schema_uri + 'themeMember',
        }
        some_relatives = {
            'http://www.eionet.europa.eu/gemet/group/96': [
                    (relations['groupMember'], gemet_uri + 'concept/21'),
                    (relations['groupMember'], gemet_uri + 'concept/24'),
                    (relations['groupMember'], gemet_uri + 'concept/95'),
                    (relations['groupMember'], gemet_uri + 'concept/100'),
                    (relations['groupMember'], gemet_uri + 'concept/103'),
                    (relations['groupMember'], gemet_uri + 'concept/105'),
                    (relations['groupMember'], gemet_uri + 'concept/107'),
            ],
            
            'http://www.eionet.europa.eu/gemet/theme/1': [
                    (relations['themeMember'], gemet_uri + 'concept/13293'),
                    (relations['themeMember'], gemet_uri + 'concept/13294'),
                    (relations['themeMember'], gemet_uri + 'concept/13295'),
                    (relations['themeMember'], gemet_uri + 'concept/13296'),
                    (relations['themeMember'], gemet_uri + 'concept/13297'),
                    (relations['themeMember'], gemet_uri + 'concept/13298'),
                    (relations['themeMember'], gemet_uri + 'concept/13300'),
                    (relations['themeMember'], gemet_uri + 'concept/13301'),
            ],
            
            'http://www.eionet.europa.eu/gemet/concept/100': [
                    (relations['narrower'], gemet_uri + 'concept/661'),
                    (relations['broader'], gemet_uri + 'concept/13292'),
                    (relations['group'], gemet_uri + 'group/96'),
                    (relations['theme'], gemet_uri + 'theme/1'),
            ],
            
            'http://www.eionet.europa.eu/gemet/concept/42': [
                    (relations['related'], gemet_uri + 'concept/51'),
                    (relations['broader'], gemet_uri + 'concept/2084'),
                    (relations['related'], gemet_uri + 'concept/7844'),
            ],
            'http://www.eionet.europa.eu/gemet/group/8603': [
                    (relations['broader'], gemet_uri + 'supergroup/4044'),
            ],
            'http://www.eionet.europa.eu/gemet/supergroup/4044': [
                    (relations['narrower'], gemet_uri + 'group/234'),
                    (relations['narrower'], gemet_uri + 'group/7007'),
                    (relations['narrower'], gemet_uri + 'group/8603'),
                    (relations['narrower'], gemet_uri + 'group/10112'),
                    (relations['narrower'], gemet_uri + 'group/10114'),
            ],
        }
        
        for concept_uri in some_relatives.keys():
            relatives = self.doXmlRpc('getAllConceptRelatives', concept_uri)
            received_relations = []
            for relative in relatives:
                self.failUnless(isinstance(relative, dict))
                self.failUnless(relative['source'] == concept_uri)
                received_relations.append('%s %s' % (relative['relation'], relative['target']))
            
            for expected in some_relatives[concept_uri]:
                expected_str = '%s %s' % (expected[0], expected[1])
                self.failUnless(expected_str in received_relations,
                    "relations for %s: missing %s" % (
                    repr(concept_uri), repr(expected_str)))
        
        # test the "thesaurus" parameter
        relatives = self.doXmlRpc('getAllConceptRelatives',
                        'http://www.eionet.europa.eu/gemet/concept/100',
                        'http://www.eionet.europa.eu/gemet/concept/')
        self.failUnless(len(relatives) > 0)
        for relative in relatives:
            self.failUnless(relative['target'].startswith('http://www.eionet.europa.eu/gemet/concept/'))
        
        relatives = self.doXmlRpc('getAllConceptRelatives',
                        'http://www.eionet.europa.eu/gemet/concept/100',
                        'http://www.eionet.europa.eu/gemet/group/')
        self.failUnless(len(relatives) > 0)
        for relative in relatives:
            self.failUnless(relative['target'].startswith('http://www.eionet.europa.eu/gemet/group/'))
        
        # also test the "relation" parameter
        relatives = self.doXmlRpc('getAllConceptRelatives',
                        'http://www.eionet.europa.eu/gemet/concept/100',
                        'http://www.eionet.europa.eu/gemet/concept/',
                        'http://www.w3.org/2004/02/skos/core#broader')
        self.failUnlessEqual(len(relatives), 1)
        self.failUnlessEqual(relatives[0]['target'], 'http://www.eionet.europa.eu/gemet/concept/13292')
        self.failUnlessEqual(relatives[0]['relation'], 'http://www.w3.org/2004/02/skos/core#broader')
        
        # test only the "relation" parameter
        relatives = self.doXmlRpc('getAllConceptRelatives',
                        'http://www.eionet.europa.eu/gemet/concept/100',
                        None,
                        'http://www.w3.org/2004/02/skos/core#broader')
        received_targets = []
        for relative in relatives:
            received_targets.append(relative['target'])
        self.failUnless('http://www.eionet.europa.eu/gemet/concept/13292' in received_targets)
    
    def test_getRelatedConcepts(self):
        relatives = self.doXmlRpc('getRelatedConcepts',
                        'http://www.eionet.europa.eu/gemet/concept/42',
                        'http://www.w3.org/2004/02/skos/core#related')
        self.failUnlessEqual(len(relatives), 2)
        for relative in relatives:
            self.failUnless(relative['uri'] in [
                    'http://www.eionet.europa.eu/gemet/concept/51',
                    'http://www.eionet.europa.eu/gemet/concept/7844'])
            self.failUnless(relative['preferredLabel']['string'] in ['acid rain', 'soil acidification'])
    
    def test_getTopmostConcepts(self):
        """
        test the getTopmostConcepts XML-RPC method
        """
        some_top_concepts = {
            'http://www.eionet.europa.eu/gemet/concept/': [25, 95, 232, 3869, 7168],
            'http://www.eionet.europa.eu/gemet/group/': [96, 234, 4856],
            'http://www.eionet.europa.eu/gemet/theme/': [1, 2, 3, 4, 5, 6],
        }
        
        for thesaurus_uri in some_top_concepts.keys():
            top_concepts = self.doXmlRpc('getTopmostConcepts', thesaurus_uri, 'en')
            top_concept_ids = {}
            for concept in top_concepts:
                top_concept_ids[concept['uri'][len(thesaurus_uri):]] = concept
            
            for concept_id in some_top_concepts[thesaurus_uri]:
                self.failUnless(str(concept_id) in top_concept_ids.keys())
                concept = top_concept_ids[str(concept_id)]
                self.failUnlessEqual(concept, self.doXmlRpc('getConcept', concept['uri'], 'en'))
    
    def test_getAvailableLanguages(self):
        """
        test the getAvailableLanguages XML-RPC method
        """
        langs = self.doXmlRpc('getAvailableLanguages', 'http://www.eionet.europa.eu/gemet/concept/7970')
        for lang in ('en', 'bg', 'ru', 'pl', 'es'):
            self.failUnless(lang in langs)
    
    def test_getSupportedLanguages(self):
        """
        test the getSupportedLanguages XML-RPC method
        """
        langs = self.doXmlRpc('getSupportedLanguages', 'http://www.eionet.europa.eu/gemet/concept/')
        for lang in ('en', 'bg', 'ru', 'pl', 'es'):
            self.failUnless(lang in langs)
    
    def test_getAvailableThesauri(self):
        """
        test the getAvailableThesauri XML-RPC method
        """
        thesauri_ref = [{
                'uri': 'http://www.eionet.europa.eu/gemet/concept/',
                'name': 'Concepts',
            },
            {
                'uri': 'http://www.eionet.europa.eu/gemet/group/',
                'name': 'Groups',
            },
            {
                'uri': 'http://www.eionet.europa.eu/gemet/theme/',
                'name': 'Themes',
            },
            {
                'uri': 'http://inspire.jrc.it/theme/',
                'name': 'Inspire Themes',
            },
        ]
        
        thesauri = self.doXmlRpc('getAvailableThesauri')
        
        thesauri_dict = {}
        for thesaurus in thesauri:
            thesauri_dict[thesaurus['uri']] = thesaurus
        
        for thesaurus_ref in thesauri_ref:
            thesaurus = thesauri_dict[thesaurus_ref['uri']]
            for key, value in thesaurus_ref.iteritems():
                self.failUnless(thesaurus[key] == value)
            self.failUnless(thesaurus['version'])
    
    def test_getAllTranslationsForConcept(self):
        """
        test the getAllTranslationsForConcept XML-RPC method
        """
        
        concepts = [
            {
                'uri': 'http://www.eionet.europa.eu/gemet/concept/7970',
                'properties': {
                    'http://www.w3.org/2004/02/skos/core#prefLabel': {
                        'en': "space travel",
                        'pl': u"podróż kosmiczna",
                        'ru': u"космический полет",
                    },
                    'http://www.w3.org/2004/02/skos/core#definition': {
                        'en': "Travel in the space beyond the earth's atmosphere",
                        'pl': u"podróż w przestrzeni poza atmosferą",
                        'ru': u"Путешествие в космосе за пределами земной атмосферы",
                    },
                }
            }
        ]
        
        for concept in concepts:
            for prop_uri, prop_values in concept['properties'].iteritems():
                result = self.doXmlRpc('getAllTranslationsForConcept', concept['uri'], prop_uri)
                self.failUnless(isinstance(result, list))
                result_langs = {}
                for translation in result:
                    self.failUnless(isinstance(translation, dict))
                    result_langs[translation['language']] = translation['string']
                for prop_value_lang, prop_value_str in prop_values.iteritems():
                    self.failUnless(result_langs[prop_value_lang].startswith(prop_value_str))
    
    def test_getConceptsMatchingKeyword(self):
        """
        test the getConceptsMatchingKeyword XML-RPC method
        """
        
        def search(keyword, mode):
            result = self.doXmlRpc('getConceptsMatchingKeyword', keyword, mode,
                    'http://www.eionet.europa.eu/gemet/concept/', 'en')
            return set(concept['preferredLabel']['string'] for concept in result)
        
        result = search('air', 0)
        self.failUnlessEqual(result, set(['air']))
        
        result = search('air', '0')
        self.failUnlessEqual(result, set(['air']))
        
        result = search('air', 1)
        self.failUnless(set(['air', 'airport', 'air safety']).issubset(result))
        self.failIf('waste air' in result)
        
        result = search('air', 2)
        self.failUnless(set(['air', 'waste air', 'soil air']).issubset(result))
        self.failIf('airport' in result)
        
        result = search('air', 3)
        self.failUnless(set(['air', 'airport', 'civil air traffic', 'waste air']).issubset(result))
        
        result = search('travel', 4) # should match exact term
        self.failUnlessEqual(result, set(['travel']))
        
        result = search('trave', 4) # should match prefix terms
        self.failUnlessEqual(result, set(['travel', 'travel cost']))
        
        result = search('ravel', 4) # should match suffix terms
        self.failUnlessEqual(result, set(['gravel', 'travel', 'space travel']))
        
        result = search('xyzasdf', 4) # should match nothing
        self.failUnlessEqual(result, set())
        
        result = search('^air', 0) # should match nothing (regex chars are escaped)
        self.failUnlessEqual(result, set())
        
        result = search("'", 3)
        self.failUnless("earth's crust" in result)
        self.failUnless("woman's status" in result)
        
        # make sure spaces and numbers still work
        try:
            search(' ', 0)
            search('3', 0)
        except:
            self.fail('spaces or digits are broken')
    
    def test_getConceptsMatchingRegexByThesaurus(self):
        """
        test the getConceptsMatchingRegexByThesaurus XML-RPC method
        """
        reference = [
            {
                'regexp': '^space t',
                'namespace': 'http://www.eionet.europa.eu/gemet/concept/',
                'language': 'en',
                'results': ['space travel', 'space transportation'],
            },
            {
                'regexp': '^air.+pol.+$',
                'namespace': 'http://www.eionet.europa.eu/gemet/concept/',
                'language': 'en',
                'results': ['air pollutant', 'air pollution'],
            },
            {
                'regexp': 'so',
                'namespace': 'http://www.eionet.europa.eu/gemet/theme/',
                'language': 'en',
                'results': ['resources', 'social aspects, population', 'soil'],
            },
            {
                'regexp': u'гия$',
                'namespace': 'http://www.eionet.europa.eu/gemet/theme/',
                'language': 'ru',
                'results': [u'биология', u'энергия'],
            },
        ]
        
        def get_match_names(match):
            names = []
            for concept in match:
                names.append(concept['preferredLabel']['string'])
            return names
        
        for query in reference:
            match = self.doXmlRpc('getConceptsMatchingRegexByThesaurus',
                    query['regexp'], query['namespace'], query['language'])
            names = get_match_names(match)
            self.failUnlessEqual(len(names), len(query['results']))
            for name in query['results']:
                self.failUnless(name in names)
    
    def test_fetchThemes(self):
        """
        test the fetchThemes XML-RPC method
        """
        result1 = self.doXmlRpc('fetchThemes', 'en')
        result2 = self.doXmlRpc('getTopmostConcepts', 'http://www.eionet.europa.eu/gemet/theme/', 'en')
        set1 = set(concept['uri'] for concept in result1)
        set2 = set(concept['uri'] for concept in result2)
        self.failUnlessEqual(set1, set2)
    
    def test_fetchGroups(self):
        """
        test the fetchGroups XML-RPC method
        """
        result1 = self.doXmlRpc('fetchGroups', 'en')
        result2 = self.doXmlRpc('getTopmostConcepts', 'http://www.eionet.europa.eu/gemet/group/', 'en')
        set1 = set(concept['uri'] for concept in result1)
        set2 = set(concept['uri'] for concept in result2)
        self.failUnlessEqual(set1, set2)

    def test_search(self):
        # a query with international characters
        result = self.doXmlRpc('getConceptsMatchingKeyword',
                               u'Floresta\xe7\xe3o'.encode('utf-8'),
                               3,
                               'http://www.eionet.europa.eu/gemet/concept/',
                               'pt')
        uris = [item['uri'] for item in result]
        self.assertTrue('http://www.eionet.europa.eu/gemet/concept/167' in uris)

if __name__ == '__main__':
    unittest.main()

