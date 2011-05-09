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

import xmlrpclib
import re

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Concept import Concept

class WebService(Concept):
    security = ClassSecurityInfo()
    
    #===== helper functions =====#
    
    def get_namespace_id(self, thesaurus_uri):
        try:
            return dict(self.get_namespaces())[thesaurus_uri]
        except KeyError, e:
            raise xmlrpclib.Fault(-1, 'Thesaurus not found: %s' % thesaurus_uri)
    
    def get_namespaces(self):
        return map(lambda n: (n['namespace_uri'], n['namespace_id']), self.fetch_namespaces())
    
    def parse_concept_uri(self, concept_uri, error_name='Concept'):
        for base_uri, ns in self.get_namespaces():
            if concept_uri.startswith(base_uri):
                # returns tuple: (ns, id, thesaurus_uri)
                return (ns, concept_uri[len(base_uri):], base_uri)
        
        raise TypeError('%s does not belong to known namespaces: %s' % (error_name, concept_uri))
    
    def construct_concept_uri(self, concept_ns, concept_id):
        for base_uri, ns in self.get_namespaces():
            if concept_ns == ns:
                return '%s%s' % (base_uri, concept_id)
        
        raise TypeError('Namespace id not found: %s' % concept_id)
    
    
    
    
    #===== public methods =====#
    
    security.declarePublic('getTopmostConcepts')
    def getTopmostConcepts(self, thesaurus_uri, language='en'):
        """ XML-RPC method: getTopmostConcepts """
        
        namespace_id = self.get_namespace_id(thesaurus_uri)
        
        concepts = []
        for concept in list(self._get_top_concepts(namespace_id, language)):
            concepts.append(self.getConcept(self.construct_concept_uri(namespace_id, concept['concept_id']), language))
        return concepts
    
    security.declarePublic('getAllConceptRelatives')
    def getAllConceptRelatives(self, concept_uri, target_thesaurus_uri=None, relation_uri=None):
        """ XML-RPC method: getAllConceptRelatives """
        (concept_ns, concept_id, thesaurus_uri) = self.parse_concept_uri(concept_uri)
        
        target_ns = None
        if target_thesaurus_uri:
            target_ns = self.parse_concept_uri(target_thesaurus_uri, error_name='Thesaurus')[0]
        
        data = self._get_concept_relatives(concept_ns, concept_id, target_ns, relation_uri)
        mappings = []
        
        for datum in data:
            rel_uri = datum['rel_type_uri']
            
            target_uri = self.construct_concept_uri(datum['rel_concept_ns'], datum['rel_concept_id'])
            
            mappings.append({
                'source': concept_uri,
                'relation': rel_uri,
                'target': target_uri,
            })
        
        return mappings
    
    security.declarePublic('getRelatedConcepts')
    def getRelatedConcepts(self, concept_uri, relation_uri, language='en'):
        """ XML-RPC method: getRelatedConcepts """
        
        concepts = []
        for relation in self.getAllConceptRelatives(concept_uri, relation_uri=relation_uri):
            concepts.append(self.getConcept(relation['target'], language))
        
        return concepts
    
    security.declarePublic('getConcept')
    def getConcept(self, concept_uri, language='en'):
        """ XML-RPC method: getConcept """
        
        try:
            (concept_ns, concept_id, thesaurus_uri) = self.parse_concept_uri(concept_uri)
        except TypeError:
            raise xmlrpclib.Fault(-1, 'Concept not found: %s' % concept_uri)
        
        concept_raw = self.fetch_concept(concept_id, concept_ns, language)
        if not concept_raw:
            raise xmlrpclib.Fault(-1, 'Concept not found: %s' % concept_uri)
        
        concept_name = concept_raw['concept_name']
        concept_definition = concept_raw['concept_definition']
        
        concept = {
            'uri': concept_uri,
            'thesaurus': thesaurus_uri,
            'preferredLabel': {'language': language, 'string': concept_name},
        }
        if concept_definition:
            concept['definition'] = {'language': language, 'string': concept_definition}
        
        return concept
    
    security.declarePublic('hasConcept')
    def hasConcept(self, concept_uri):
        """ XML-RPC method: hasConcept """
        try:
            self.getConcept(concept_uri)
        except xmlrpclib.Fault:
            return False
        else:
            return True
    
    security.declarePublic('hasRelation')
    def hasRelation(self, concept_uri, relation_uri, object_uri):
        """ XML-RPC method: hasRelation """

        try:
            relatives = self.getAllConceptRelatives(concept_uri)
        except TypeError:
            return False
        rel = {'source': concept_uri,
               'relation': relation_uri,
               'target': object_uri}

        if rel in relatives:
            return True
        else:
            return False

    security.declarePublic('getAllTranslationsForConcept')
    def getAllTranslationsForConcept(self, concept_uri, property_uri):
        """ XML-RPC method: getAllTranslationsForConcept """
        
        # FIXME: This methods must use the property_type table.
        properties = {
            'http://www.w3.org/2004/02/skos/core#definition':   'definition',
            'http://www.w3.org/2004/02/skos/core#prefLabel':    'prefLabel',
            'http://www.w3.org/2004/02/skos/core#scopeNote':    'scopeNote',
            'http://www.w3.org/2004/02/skos/core#altLabel':     None, # not implemented
            'http://www.w3.org/2004/02/skos/core#example':      None, # not implemented
        }
        
        prop_name = properties.get(property_uri, None)
        
        if not prop_name:
            # we don't have any data for this property. best to just return an empty list.
            return []
        
        try:
            (concept_ns, concept_id, thesaurus_uri) = self.parse_concept_uri(concept_uri)
        except TypeError:
            raise xmlrpclib.Fault(-1, 'Concept not found: %s' % concept_uri)
        
        raw_translations = self.fetch_concept_property_translations(concept_ns, concept_id, prop_name)
        
        result = []
        for translation in raw_translations:
            result.append({
                'language': translation['langcode'],
                'string': translation['value'],
            })
        return result
    
    security.declarePublic('getConceptsMatchingKeyword')
    def getConceptsMatchingKeyword(self, keyword, search_mode, thesaurus_uri, language):
        """ XML-RPC method: getConceptsMatchingKeyword """
        
        search_mode = int(search_mode)

        if isinstance(keyword, str):
            try:
                keyword = keyword.decode('utf-8')
            except UnicodeDecodeError:
                keyword = keyword.decode('latin-1')

        def escape(match):
            return '\\%s' % match.group(0)
        keyword = re.sub(r'[\.\^\$\*\+\?\{\}\\\[\]\|\(\)]', escape, keyword)
        
        search_regex = lambda regex: self.getConceptsMatchingRegexByThesaurus(regex, thesaurus_uri, language)
        search_exact = lambda: search_regex('^%s$' % keyword)
        search_suffix = lambda: search_regex('^%s' % keyword)
        search_prefix = lambda: search_regex('%s$' % keyword)
        search_both = lambda: search_regex('%s' % keyword)
        
        def search_all():
            res = search_exact()
            if res:
                return res
            
            res = search_suffix()
            if res:
                return res
            
            res = search_prefix()
            if res:
                return res
            
            return []
        
        if search_mode == 0:
            return search_exact()
        
        elif search_mode == 1:
            return search_suffix()
        
        elif search_mode == 2:
            return search_prefix()
        
        elif search_mode == 3:
            return search_both()
        
        elif search_mode == 4:
            return search_all()
        
        else:
            raise xmlrpclib.Fault(-1, 'Invalid search mode. Possible values are 0 .. 4.')
    
    security.declarePublic('getConceptsMatchingRegexByThesaurus')
    def getConceptsMatchingRegexByThesaurus(self, regex, thesaurus_uri, language):
        """ XML-RPC method: getConceptsMatchingRegexByThesaurus """
        
        
        if isinstance(regex, str):
            try:
                regex = regex.decode('utf-8')
            except:
                regex = regex.decode('latin-1')
        namespace_id = self.get_namespace_id(thesaurus_uri)
        
        data = self.fetch_concept_by_regex(namespace_id, regex, language)
        
        concepts = []
        for datum in data:
            concepts.append(self.getConcept(self.construct_concept_uri(namespace_id, datum['concept_id']), language))
        
        return concepts
    
    security.declarePublic('getAvailableLanguages')
    def getAvailableLanguages(self, concept_uri):
        """ XML-RPC method: getAvailableLanguages """
        
        (concept_ns, concept_id, thesaurus_uri) = self.parse_concept_uri(concept_uri)
        data = self.fetch_concept_languages(concept_ns, concept_id)
        
        langs = []
        for datum in data:
            langs.append(datum['langcode'])
        
        return langs
    
    security.declarePublic('getSupportedLanguages')
    def getSupportedLanguages(self, thesaurus_uri):
        """ XML-RPC method: getSupportedLanguages """
        
        data = self.fetch_namespace_languages(self.get_namespace_id(thesaurus_uri))
        
        langs = []
        for datum in data:
            langs.append(datum['langcode'])
        
        return langs
    
    security.declarePublic('getAvailableThesauri')
    def getAvailableThesauri(self):
        """ XML-RPC method: getAvailableThesauri """
        
        data = self.fetch_namespaces()
        
        thesauri = []
        for datum in data:
            thesauri.append({
                'uri': datum['namespace_uri'],
                'name': datum['namespace_name'],
                'version': datum['namespace_version'],
            })
        
        return thesauri

    security.declarePublic('fetchThemes')
    def fetchThemes(self, language):
        """ XML-RPC method: fetchThemes """
        return self.getTopmostConcepts('http://www.eionet.europa.eu/gemet/theme/', language)

    security.declarePublic('fetchGroups')
    def fetchGroups(self, language):
        """ XML-RPC method: fetchGroups """
        return self.getTopmostConcepts('http://www.eionet.europa.eu/gemet/group/', language)


InitializeClass(WebService)
