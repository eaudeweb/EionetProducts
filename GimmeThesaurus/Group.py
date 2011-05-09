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

# python imports
import sys

from MySQLdb import OperationalError

from SQLStatements import *
from Utils import Utils
from Mappings import Mappings
from _exceptions import *
from DatabaseManager import DatabaseManager

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Concept import ConceptLink

class Group(Mappings, Utils):
    """ group class """

    security = ClassSecurityInfo()

    security.declarePrivate('_get_group')
    def _get_group(self, id, lang, conn=None):
        """ get group info """
        destroy = 0
        if conn is None:
            destroy = 1
            conn = DatabaseManager()
            conn.openConnection(self)

        err, res, msg = conn.query(sql_get_group_name(id, lang))

        if destroy:
            conn.closeConnection()
            conn = None

        if err:
            raise DatabaseError, msg

        return res


    security.declarePrivate('_get_supergroups')
    def _get_supergroups(self, lang, collation, conn=None):
        """ get all supergroups """
        destroy = 0
        if conn is None:
            destroy = 1
            conn = DatabaseManager()
            conn.openConnection(self)

        err, res, msg = conn.query(sql_get_supergroups(lang, collation))

        if destroy:
            conn.closeConnection()
            conn = None

        if err:
            raise DatabaseError, msg

        return res


    security.declarePrivate('_get_groups_super')
    def _get_groups_super(self, id, lang, collation, conn=None):
        """ get all the groups belonging to a supergroup """

        destroy = 0
        if conn is None:
            destroy = 1
            conn = DatabaseManager()
            conn.openConnection(self)

        err, res, msg = conn.query(sql_get_groups_super(id, lang, collation))

        if destroy:
            conn.closeConnection()
            conn = None

        if err:
            raise DatabaseError, msg

        return res


    security.declarePrivate('_get_groups')
    def _get_groups(self, lang, conn=None):
        """ get all groups """

        destroy = 0
        if conn is None:
            destroy = 1
            conn = DatabaseManager()
            conn.openConnection(self)

        err, res, msg = conn.query(sql_get_groups(lang))

        if destroy:
            conn.closeConnection()
            conn = None

        if err:
            raise DatabaseError, msg

        return res


    security.declarePrivate('_get_group_top_concepts')
    def _get_group_top_concepts(self, group, lang, collation, conn=None):

        destroy = 0
        if conn is None:
            destroy = 1
            conn = DatabaseManager()
            conn.openConnection(self)

        err, res, msg = conn.query(sql_get_group_top_concepts(group, lang, collation))

        if destroy:
            conn.closeConnection()
            conn = None

        if err:
            raise DatabaseError, msg

        return res

    security.declarePublic('GetGroups')
    def GetGroups(self, langcode=None, REQUEST=None):
        """ return all the super_groups with all their childrens """

        results = {} #{(id_super, def_super):[{id:id_group, def:def_group},...]}

        if langcode is None:
            return ((), 1)

        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, err:
            self.error_log.raising(sys.exc_info())
            return ((), 1)

        #get all the supergroups
        try:
            collation = self._get_language_collation(langcode, conn)
            super = self._get_supergroups(langcode, collation, conn)
        except DatabaseError, error:
            self.error_log.raising(sys.exc_info())
            return ((), 1)

        if super:
            #optimizations
            get_descr = self.mp_group_descr
            get_id = self.mp_group_id

            for s in super:
                #get all the groups belonging to a supergroup
                try:
                    groups = self._get_groups_super(get_id(s), langcode, collation)
                except DatabaseError, error:
                    return ((), 1)

                gr_list = []    #will contain {id_group:def_group}
                if groups:
                    for gr in groups:
                        gr_list.append({'group_id':str(get_id(gr)), 'group_description':get_descr(gr)})
                    results[(str(get_id(s)), get_descr(s))] = gr_list

        conn.closeConnection()
        conn = None

        return (results, 0)

    def rec_get_norrow(self, depth, p_id, langcode, collation, conn, params):
        l_tree = []
        if len(params) != 0:
            narr, errors = self.get_narrower_concepts(2, p_id, langcode, collation, conn)
            params = self.utRemoveFromList(params, params[0])
            if not errors:
                for x in narr:
                    if str(x[1]) in params:
                        l_tree.append((ConceptLink(1, x[1], x[2]), 0, depth))
                        l_tree.extend(self.rec_get_norrow(depth + 1, str(x[1]), langcode, collation, conn, params))
                    else:
                        l_tree.append((ConceptLink(1, x[1], x[2]), 1, depth))
        return l_tree

    security.declarePublic('GetGroupConcepts')
    def GetGroupConcepts(self, params, langcode=None, REQUEST=None):
        """ return all the narrower concepts beloging to a group """

        relations = []
        top_cp = []

        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            self.error_log.raising(sys.exc_info())
            return ((), 1)

        if len(params) >= 1:
            #get the group name
            try:
                res = self._get_group(params[0], langcode, conn)
            except DatabaseError, error:
                return ((), 1)

            if res:
                res = self.mp_group_descr(res[0])

            relations.append((ConceptLink(1, params[0], res), -1, 0))

            #get top concepts for id_group
            try:
                collation = self._get_language_collation(langcode, conn)
                res = self._get_group_top_concepts(params[0], langcode, collation, conn)
            except DatabaseError, error:
                return ((), 1)

            #remove group id
            params = self.utRemoveFromList(params, params[0])

            get_id = self.mp_concept_id
            get_name = self.mp_concept_name

            [top_cp.append((1, get_id(x),get_name(x))) for x in res]

            for tc in top_cp:
                if str(tc[1]) in params:
                    relations.append((ConceptLink(1, tc[1], tc[2]), 0, 1))
                    narr = self.rec_get_norrow(2, tc[1], langcode, collation, conn, params)
                    relations.extend(narr)
                else:
                    relations.append((ConceptLink(1, tc[1], tc[2]), 1, 1))
        else:
            pass

        conn.closeConnection()
        conn = None

        return (relations, 0)


InitializeClass(Group)
