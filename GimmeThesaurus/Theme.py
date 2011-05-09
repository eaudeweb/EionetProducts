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
#$Id: Utils.py 3357 2005-04-13 16:35:01Z nituacor $
# -*- coding: utf-8 -*-

__version__='$Revision: 1.7 $'[11:-2]
# python imports
from MySQLdb import OperationalError

#zope imports
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

#product imports
from _exceptions import *
from _constants import *
from SQLStatements import *
from Utils import Utils
from Mappings import Mappings
from DatabaseManager import DatabaseManager
from PagingManager import getPagingInformation
from Concept import ConceptLink


class Theme(Mappings, Utils):
    """ """

    security = ClassSecurityInfo()

    security.declarePrivate('_get_themes')
    def _get_themes(self, namespace, lang, conn=None):
        destroy = 0
        if conn is None:
            destroy = 1
            conn = DatabaseManager()
            conn.openConnection(self)

        collation = self._get_language_collation(lang, conn)
        err, res, msg = conn.query(sql_get_themes(namespace, lang, collation))

        if destroy:
            conn.closeConnection()
            conn = None

        if err:
            raise DatabaseError, msg

        return res


    security.declarePublic('GetThemes')
    def GetThemes(self, lang=None, REQUEST=None, namespace=4):
        """ return all the themes for a given langcode """

        flag = 0
        if lang is None:
            return ((), 1)

        conn = DatabaseManager()
        conn.openConnection(self)

        try:
            res = self._get_themes(namespace, lang, conn)
        except OperationalError, err:
            print err
            flag = 1
        except DatabaseError, err:
            print err
            flag = 1

        conn.closeConnection()

        if flag:
            #write log err
            return ((), 1)

        return (res, 0)

    security.declarePublic('GetThemeConcepts')
    def GetThemeConcepts(self, theme, langcode, start=0, letter=0, namespace=4):
        """ return all the concepts for a given theme tagged with their language """

        def wrap_concept(concept):
            return concept

        th_name = ''

        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            return ((), [], 1, '')

        #get language collation
        collation = self._get_language_collation(langcode, conn)

        err, res, msg = conn.query(sql_get_theme_concepts(theme, namespace, langcode, collation, letter))
        #fix this
        if err:
            return ((), [], 1, '')

        concepts = []
        for r in res:
            concepts.append(ConceptLink(r['concept_ns'], r['concept_id'], r['concept_name']))

        err, res_th, msg = conn.query(sql_get_current_theme(theme, namespace, langcode))
        th_orig = 1
        if err or len(res_th)==0:
            th_orig = 0
            err, res_th, msg = conn.query(sql_get_current_theme(theme, namespace, 'en'))
#            return ((), [], 1, '')
        for th in res_th:
            th_name = self.mp_theme_descr(th)
            th_def = self.mp_theme_definition(th)

        conn.closeConnection()
        conn = None

        #process result
        paging_info = (0, 0, 0, -1, -1, 0, NUMBER_OF_RESULTS_PER_PAGE, [0])

        if err:
            #write in log file
            return (paging_info, [], 1, '')
        else:
            try: start = abs(int(start))
            except: start = 0
            if len(concepts) > 0:
                paging_info = getPagingInformation(NUMBER_OF_RESULTS_PER_PAGE, len(concepts), start)

        if concepts:
            return (paging_info, concepts[paging_info[0]:paging_info[1]], 0, (th_name, th_orig, th_def))
        else:
            return (paging_info, [], 0, (th_name, th_orig, th_def))

InitializeClass(Theme)
