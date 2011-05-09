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
# Agency (EEA).  Portions created by Finsiel Romania and Eau de Web are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Authors:
#
# Alex Ghica, Eau de Web
# Alex Morega, Eau de Web
# Cornel Nitu, Eau de Web
#
# -*- coding: utf-8 -*-

# python imports
from MySQLdb import OperationalError
from urllib import quote as urlquote

#zope imports
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

#product imports
from SQLStatements import *
from _exceptions import *
from _constants import *
from Utils import Utils
from Mappings import Mappings
from DatabaseManager import DatabaseManager
from PagingManager import getPagingInformation

class ConceptLink(object):
    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')

    def __init__(self, concept_ns, concept_id, concept_name, concept_scope_name=None, concept_alt_name=None):
        self.concept_ns = concept_ns
        self.concept_id = concept_id
        self.concept_name = concept_name
        self.concept_scope_name = concept_scope_name
        self.concept_alt_name = concept_alt_name

    def get_url(self, here, extra={}):
        params = dict(extra, cp=self.concept_id, ns=self.concept_ns)
        params_str = '&'.join(map(
            lambda key: "%s=%s" % (urlquote(str(key)), urlquote(str(params[key]))),
            params ))
        return "%s/concept?%s" % (here.absolute_url(), params_str)

InitializeClass(ConceptLink)

class Concept(Mappings, Utils):
    """ concept class """

    def __init__(self):
        """ contructor """
        pass

    security = ClassSecurityInfo()

    security.declarePrivate('_get_concept_relatives')
    def _get_concept_relatives(self, concept_ns, concept_id, target_ns=None, relation_uri=None):
        """ get all concepts related to a given concept """
        conn = DatabaseManager()
        conn.openConnection(self)

        err, res, msg = conn.query(sql_get_concept_relatives(concept_ns, concept_id, target_ns, relation_uri))

        conn.closeConnection()

        return res

    security.declarePublic('GetBackbone')
    def GetBackbone(self):
        """ return data for backbone.rdf """
        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            return ((), 1)

        err, relations, msg = conn.query(sql_get_all_concepts_groups())

        if err:
            return ((), 1)

        #alias
        get_concept_id = self.mp_concept_id
        get_group_id = self.mp_group_id
        get_theme_id = self.mp_theme_id

        results = {}

        for record in relations:
            current = get_concept_id(record)

            if not results.has_key(current):
                results[current] = [[]]

            results[current][0].append(get_group_id(record))


        err, relations, msg = conn.query(sql_select_all_concepts_themes())
        if err:
            return ((), 1)

        for record in relations:
            current = get_concept_id(record)

            if not results.has_key(current):
                results[current] = [[], []]

            th = get_theme_id(record)
            if len(results[current]) == 1:
                results[current].append([])
            results[current][1].append(th)

        conn.closeConnection()
        conn = None

        return results


    security.declarePublic('GetConceptsInfo')
    def GetConceptsInfo(self, langcode, ns=1, REQUEST=None):
        """ return the concept name and the concept definition for a given language """
        conn = DatabaseManager()
        conn.openConnection(self)

        err, res, msg = conn.query(sql_get_all_concepts_name(ns, langcode))

        conn.closeConnection()

        if err:
            return ((), 1)

        return res

    security.declarePrivate('_get_top_concepts')
    def _get_top_concepts(self, namespace_id, lang, conn=None):
        """ """
        destroy = 0
        if conn is None:
            destroy = 1
            conn = DatabaseManager()
            conn.openConnection(self)

        #get language collation
        collation = self._get_language_collation(lang, conn)

        err, res, msg = conn.query(sql_get_top_concepts(namespace_id, lang, collation))

        if destroy:
            conn.closeConnection()
            conn = None

        if err:
            raise DatabaseError, msg
        return res

    security.declarePublic('searchThesaurus')
    def searchThesaurus(self, term, langcode='en', ns=1):
        """ """
        if not term:
            return []

        conn = DatabaseManager()
        conn.openConnection(self)

        collation = self._get_language_collation(langcode, conn)
        err, res, msg = conn.query(sql_find_concept(term, langcode, collation))
        if err:
            # log error
            return []

        conn.closeConnection()

        results = []
        for i in res:
            if i['scope_name'] is None:
                i['scope_name'] = ''
            if i['concept_alt_name'] is None:
                i['concept_alt_name'] = ''
            results.append(ConceptLink(ns, i['concept_id'], i['concept_name'], i['scope_name'], i['concept_alt_name']))

        return results

    security.declarePublic('GetConceptName')
    def GetConceptName(self, concept_ns, concept_id, langcode):
        """ return a concepts name in requested language """

        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            return (0, 1)

        err, res, msg = conn.query(sql_get_concept_name(concept_ns, concept_id, langcode))

        conn.closeConnection()
        conn = None

        #process result
        if err:
            #write in log file
            print err, msg
            return (0, 1)
        else:
            return (1, res)


    security.declarePublic('GetConceptsName')
    def GetConceptsName(self, langcode, start=0, letter=0, ns=1):
        """ return the concepts name for a given language """

        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            return ((), [], 1)

        #get language collation
        collation = self._get_language_collation(langcode, conn)

        err, res, msg = conn.query(sql_get_concepts_letter(langcode, collation, letter))

        conn.closeConnection()
        conn = None

        concepts = []
        for r in res:
            concepts.append(ConceptLink(ns, r['concept_id'], r['concept_name']))

        #process result
        paging_info = (0, 0, 0, -1, -1, 0, NUMBER_OF_RESULTS_PER_PAGE, [0])
        if err:
            #write in log file
            return (paging_info, [], 0)
        else:
            try: start = abs(int(start))
            except: start = 0
            if len(concepts) > 0:
                paging_info = getPagingInformation(NUMBER_OF_RESULTS_PER_PAGE, len(concepts), start)
        if concepts:
            return (paging_info, concepts[paging_info[0]:paging_info[1]], 0)
        else:
            return (paging_info, [], 0)


    security.declarePublic('GetConceptDetails')
    def GetConceptDetails(self, concept_id, langcode, concept_ns=1):
        """ return all the information available for a given concept """
        nt_list = []
        bt_list = []
        rt_list = []
        ct_name = {}
        ct_trans = []
        ct_definition = ''
        ct_note = ''
        errors = 0

        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            return ({}, [], [], [], [], '', '', '', (), (), (), (), 1)

        #get language collation
        collation = self._get_language_collation(langcode, conn)

        err, res_rel, msg = conn.query(sql_get_relation(concept_ns, concept_id, langcode, collation))

        if err:
            #write in log file
            errors = 1
        else:
            for dic in res_rel:
                concept = ConceptLink(concept_ns, dic['relation_id'], dic['relation_name'])
                if self.mp_relation_descr(dic) == 'narrower':
                    nt_list.append(concept)
                elif self.mp_relation_descr(dic) == 'broader':
                    bt_list.append(concept)
                elif self.mp_relation_descr(dic) == 'related':
                    rt_list.append(concept)

        err, res_name, msg = conn.query(sql_get_concept_names(concept_ns, concept_id))

        if err or len(res_name)==0:
            #write in log file
            errors = 1
            return ({}, [], [], [], [], '', '', '', (), (), (), (), errors)
        else:
            for dic in res_name:
                if self.mp_langcode(dic) == langcode:
                    ct_name = dic.copy()
                    _, alt_names, _ = conn.query(
                            sql_get_concept_property_lang('alt_name', concept_ns, concept_id, 'altLabel', langcode))
                    ct_name['alt_names'] = []
                    for alt_label in alt_names:
                        ct_name['alt_names'].append(alt_label['alt_name'])
                else:
                    ct_trans.append(dic)

        # get relations in current language
        err, raw_relations, msg = conn.query(sql_get_concept_relations(concept_ns, concept_id, langcode, collation))
        relations_dic = {}
        for relation in raw_relations:
            ns = relation['concept_ns_name']
            if ns not in relations_dic:
                relations_dic[ns] = []
            relations_dic[ns].append(relation['concept_name'])

        # get relations in english
        err, raw_relations, msg = conn.query(sql_get_concept_relations(concept_ns, concept_id, 'en', collation))
        en_relations_dic = {}
        for relation in raw_relations:
            ns = relation['concept_ns_name']
            if ns not in en_relations_dic:
                en_relations_dic[ns] = []
            en_relations_dic[ns].append(relation['concept_name'])

        # merge them
        namespaces = []
        for ns in relations_dic.keys() + en_relations_dic.keys():
            if ns not in namespaces:
                namespaces.append(ns)
        namespaces.sort()

        relations = []
        for ns in namespaces:
            if ns in relations_dic.keys():
                relations.append({'thesaurus': ns, 'concepts': relations_dic[ns], 'available_in_lang': True})
            else:
                relations.append({'thesaurus': ns, 'concepts': en_relations_dic[ns], 'available_in_lang': False})

        foreign_relations = {}
        err, foreign_relations_rows, msg = conn.query(sql_get_concept_foreign_relations(concept_ns, concept_id, langcode, collation))
        if foreign_relations_rows:
            for row in foreign_relations_rows:
                key = (row['concept_relation_type'], row['concept_property_label'], )
                if key not in foreign_relations:
                    foreign_relations[key] = []
                foreign_relations[key].append(( row['foreign_relation_uri'], row['foreign_relation_label']))

        marker = "00" #scope definition, scope note

        err, scope, msg = conn.query(sql_get_concept_note_definition(concept_ns, concept_id, langcode))
        if err:
            #write in log file
            errors = 1
        else:
            if len(scope) > 0:
                marker = "11"
                ct_definition = self.mp_concept_definition(scope[0])
                ct_note = self.mp_concept_note(scope[0])
                if ct_definition == '':
                    marker = "01"
                    err, scope, msg = conn.query(sql_get_concept_definition(concept_ns, concept_id, DEFAULT_LANGUAGE))
                    if err:
                        #write in log file
                        errors = 1
                    if len(scope): ct_definition = self.mp_concept_definition(scope[0])
                elif ct_note == '':
                    marker = "10"
                    err, scope, msg = conn.query(sql_get_concept_note(concept_ns, concept_id, DEFAULT_LANGUAGE))
                    if err:
                        #write in log file
                        errors = 1
                    if len(scope): ct_note = self.mp_concept_note(scope[0])
            else:
                marker = "00"
                err, scope, msg = conn.query(sql_get_concept_note_definition(concept_ns, concept_id, DEFAULT_LANGUAGE))
                if err:
                    #write in log file
                    errors = 1
                else:
                    if len(scope):
                         ct_definition = self.mp_concept_definition(scope[0])
                         ct_note = self.mp_concept_note(scope[0])
                    else:
                        ct_definition = ""
                        ct_note = ""

            #Get property.name = 'source'
            err, source, msg = conn.query(sql_get_concept_property_lang('value', concept_ns, concept_id, 'source', langcode))

        conn.closeConnection()
        conn = None
        return (ct_name, nt_list, bt_list, rt_list, ct_trans, ct_definition,
                ct_note, marker, relations, foreign_relations, source, errors)

    def fetch_concept_property_translations(self, concept_ns, concept_id, prop_name):
        conn = DatabaseManager()
        conn.openConnection(self)

        err, res, msg = conn.query(sql_get_concept_property(concept_ns, concept_id, prop_name))
        if err:
            print err, msg

        conn.closeConnection()
        return res

    def fetch_namespaces(self):
        conn = DatabaseManager()
        conn.openConnection(self)

        err, res, msg = conn.query(sql_get_namespaces())
        if err:
            print err, msg

        conn.closeConnection()
        return res

    def fetch_concept(self, concept_id, concept_ns, language):
        conn = DatabaseManager()
        conn.openConnection(self)

        err, res, msg = conn.query(sql_get_concept(concept_id, concept_ns, language))
        if err:
            print err, msg

        conn.closeConnection()
        if len(res) > 0:
            return res[0]
        return None

    def fetch_concept_languages(self, concept_ns, concept_id):
        conn = DatabaseManager()
        conn.openConnection(self)

        err, res, msg = conn.query(sql_get_concept_languages(concept_ns, concept_id))
        if err:
            print err, msg

        conn.closeConnection()

        return res

    def fetch_namespace_languages(self, namespace_id):
        conn = DatabaseManager()
        conn.openConnection(self)

        err, res, msg = conn.query(sql_get_namespace_languages(namespace_id))
        if err:
            print err, msg

        conn.closeConnection()

        return res

    def fetch_concept_by_regex(self, namespace_id, regex, language):
        conn = DatabaseManager()
        conn.openConnection(self)

        err, res, msg = conn.query(sql_get_concept_by_regex(namespace_id, regex, language))
        if err:
            print err, msg

        conn.closeConnection()

        return res

#---------------interface-------------------------------------------------#
    def get_narrower_concepts(self, level, id_concept, langcode, collation, dbman):
        """ return all the narrower concepts given a concept """
        errors = 0
        narrower = []

        #some optimizations
        get_id = self.mp_concept_id
        get_name = self.mp_concept_name

        err, res, msg = dbman.query(sql_get_concept_narrower(id_concept, langcode, collation))
        if err:
            #write in log file
            errors = 1
        if res:
            for record in res:
                narrower.append((level, get_id(record),get_name(record)))

        return (narrower, errors)

InitializeClass(Concept)
