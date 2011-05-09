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

__version__='$Revision: 1.49 $'[11:-2]

# python imports
from MySQLdb import OperationalError

# Zope imports
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder
from Globals import InitializeClass, package_home
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
import Products

# product imports
from SQLStatements import *
from Utils import Utils
from DatabaseManager import DatabaseManager
from Mappings import Mappings

from SessionManager import SessionManager
from ErrorCodes import *
from _exceptions import *
from _constants import *

from Concept import Concept
from Group import Group
from Theme import Theme
from WebService import WebService
from cgi import escape


def get_first_accept(req_dict):
    """ Figures out which type of content the webbrowser prefers
        If it is 'application/rdf+xml', then send RDF
    """
    s = req_dict.get_header('HTTP_ACCEPT','*/*')
    segs = s.split(',')
    firstseg = segs[0].split(';')
    return firstseg[0].strip()

manage_addThesaurus_html = PageTemplateFile('zpt/thesaurus_add', globals())

def manage_addThesaurus(self, id, title='', description='', db_host='', db_name='', db_user='', db_password='', db_port='3306', REQUEST=None):
    """ Adds a new GimmeThesaurus object """
    ob = Thesaurus(id, title, description,db_host, db_name, db_user, db_password, db_port)
    self._setObject(id, ob)

    th = self._getOb(id)
    th.loadRDF()

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)


class Thesaurus(Folder, Concept, Group, Theme, Mappings, Utils, SessionManager, WebService):
    """ Gimme Thesaurus """

    meta_type = 'Gimme Thesaurus'
    product_name = 'Gimme Thesaurus'

    manage_options =((Folder.manage_options[0],) +
                (Folder.manage_options[3],) +
                ({'label':'View',                'action':'index_html'},
                 {'label':'Administration',      'action':'administration'},
                 {'label':'Undo',                'action':'manage_UndoForm'},))

    security = ClassSecurityInfo()


    def __init__(self, id, title, description, db_host, db_name, db_user, db_password, db_port):
        """ constructor """
        self.id = id
        self.title = title
        self.description = description

        #database stuff
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = int(db_port)

        #default language
        self.langcode = DEFAULT_LANGUAGE
        SessionManager.__dict__['__init__'](self)


#------------ manage properties -----------------------------------------------------#
    def all_meta_types(self):
        """ What can you put inside me? """
        local_meta_types = []
        f = lambda x: x['name'] in ('Page Template', 'Script (Python)', 'File',
           'Folder','DTML Method', 'Site Error Log', 'Gimme Thesaurus Webservice')
        for x in filter(f, Products.meta_types):
            local_meta_types.append(x)
        return local_meta_types

    security.declareProtected('Manage GimmeThesaurus', 'manageProperties')
    def manageProperties(self, title='', description='', langcode='', REQUEST=None, RESPONSE=None):
        """ manage basic properties """
        self.langcode = langcode
        self.title = title
        self.description = description
        self._p_changed = 1
        if REQUEST is not None:
            #set info message to session
            self.setSessionInfo(MSG_PROPERTIES_SAVED)
            if REQUEST is not None:
                return RESPONSE.redirect('administration')

    security.declareProtected('Manage GimmeThesaurus', 'manageDatabaseConnection')
    def manageDatabaseConnection(self, REQUEST=None, RESPONSE=None):
        """Update database connection configuration"""
        #load form data
        db_host = REQUEST.get('db_host', self.db_host)
        db_name = REQUEST.get('db_name', self.db_name)
        db_user = REQUEST.get('db_user', self.db_user)
        db_password = REQUEST.get('db_password', self.db_password)
        db_port = REQUEST.get('db_port', self.db_port)

        try:    db_port = int(db_port)
        except: pass

        #test connection
        err = DatabaseManager().testConnection(db_host, db_user, db_password, db_name, db_port)
        if err:
            if REQUEST is not None:
                #save form data to session
                self.setDBSession(db_host, db_name, db_user, db_password, db_port)
                #put error to session
                self.setSessionErrors(self.utDBError([err]))
                return RESPONSE.redirect('administration')
            return "error"

        #delete form data from session
        self.delDBSession()

        #delete error from session
        self.delSessionErrors()

        #save data
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port
        self._p_changed = 1

        if REQUEST is not None:
            #set info message to session
            self.setSessionInfo(MSG_DB_CONECTED)
            return RESPONSE.redirect('administration')

#------------ language & alphabets -----------------------------------------------------#
    security.declarePrivate('_get_language_collation')
    def _get_language_collation(self, lang, conn=None):
        """ get a languages collation by its code """

        destroy = 0
        if conn is None:
            destroy = 1
            conn = DatabaseManager()
            conn.openConnection(self)

        err, res, msg = conn.query(sql_get_language_collation(lang))

        if destroy:
            conn.closeConnection()
            conn = None

        if err:
            raise DatabaseError, msg

        return self.mp_charset(res[0])

    security.declarePublic('GetLanguages')
    def GetLanguages(self, concept_ns=None, concept_id=None):
        """ get languages """

        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            return None

        err, res, msg = conn.query(sql_get_languages(concept_ns, concept_id))
        conn.closeConnection()
        conn = None

        if err:
            #write in log file
            pass

        return res


    security.declarePublic('GetUnicodeLangs')
    def GetUnicodeLangs(self):
        """ return the unicode languages list """
        return unicode_langs()


    security.declarePublic('GetUnicodeMaps')
    def GetUnicodeMap(self, lang):
        """ return unicode set of characters """
        return unicode_map(lang)

    security.declarePublic('GetLanguage')
    def GetLanguage(self, lang):
        """ get a language by its code """

        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            return ({}, 1)

        err, res, msg = conn.query(sql_get_language(lang))
        conn.closeConnection()
        conn = None

        if err:
            #write in log file
            return ({}, 1)

        return (res, 0)

    security.declarePublic('GetLanguage')
    def GetLanguageDirection(self, lang):
        """ get a language by its code """

        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            return ({}, 1)

        err, res, msg = conn.query(sql_get_language_dirention(lang))
        conn.closeConnection()
        conn = None

        if err:
            #write in log file
            return ({}, 1)

        return (res, 0)

    security.declarePublic('getAlphabet')
    def getAlphabet(self, lang, theme, case, theme_ns=''):
        """ return the alphabet (default small letters) for a given language """
        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            conn.closeConnection()
            return ((), [], 1, '')

        #get language collation
        collation = self._get_language_collation(lang, conn)

        alphabet = []
        #l_case = self.utFormatCase(int(p_case))
        case = int(case)
        i = 1
        for letter in self.GetUnicodeMap(lang):
            if theme != '':
                err, res, msg = conn.query(sql_get_theme_concepts(theme, theme_ns, lang, collation, i))
            else:
                err, res, msg = conn.query(sql_get_concepts_letter(lang, collation, i))

            alphabet.append((letter[case].encode('utf-8'), len(res)))
            i += 1

        conn.closeConnection()
        conn = None
        return alphabet

#------------ definition sources -----------------------------------------------------#
    security.declarePublic('getDefinitionSources')
    def getDefinitionSources(self):
        """ return definition sources """
        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            return ({}, 1)

        err, res, msg = conn.query(sql_get_definition_sources())
        conn.closeConnection()
        conn = None

        if err:
            #write in log file
            return ({}, 1)

        return (res, 0)

#------------ RDF methods -----------------------------------------------------#
    security.declarePublic('GetLabelsRDF')
    def GetLabelsRDF(self, rdf_lang, REQUEST=None):
        """."""
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/gemet-definitions.rdf?langcode=%s' % (self.absolute_url(0), rdf_lang))


    security.declarePublic('GetLabelsRDF')
    def GetGroupsRDF(self, rdf_lang, REQUEST=None):
        """."""
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/gemet-groups.rdf?langcode=%s' % (self.absolute_url(0), rdf_lang))


    security.declareProtected('Manage GimmeThesaurus', 'loadRDF')
    def loadRDF(self):
        """ loads rdf files """
        from os.path import join
        from Products.PythonScripts.PythonScript import manage_addPythonScript

        file_list = [
            'gemet-backbone.html',
            'gemet-backbone.rdf',
            'gemet-definitions.html',
            'gemet-definitions.rdf',
            'gemet-groups.html',
            'gemet-groups.rdf',
            'gemet-relations.html',
            'gemet-skoscore.rdf'
        ]

        for file_name in file_list:
            file_content = open(join(package_home(globals()), 'rdfs', file_name + '.py'), 'r').read()
            manage_addPythonScript(self, file_name)
            self._getOb(file_name).write(file_content)

    security.declarePublic('GetAllRelations')
    def GetAllRelations(self):
        """ return all relations """
        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            #write log
            return ((), 1)

        err, relations, msg = conn.query(sql_get_relations())
        err, foreign_relations, msg = conn.query(sql_get_foreign_relations())

        #alias
        get_concept_id = self.mp_concept_id
        get_relation_name = self.mp_relation_name
        get_relation_id = self.mp_relation_id

        results = {}
        for record in (relations + foreign_relations):
            current = get_concept_id(record)
            relation_name = get_relation_name(record)
            relation_id = get_relation_id(record)

            if current not in results:
                results[current] = {}
            if relation_name not in results[current]:
                results[current][relation_name] = []

            results[current][relation_name].append(relation_id)

        conn.closeConnection()
        conn = None

        return results

    security.declarePublic('GetGroupsAndThemes')
    def GetGroupsAndThemes(self, langcode):
        """ return all the groups and all the themes for a given language """
        errors = 0
        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, err:
            #write log
            errors = 1
            return ((), (), (), err)

        collation = self._get_language_collation(langcode, conn)

        err, groups, msg = conn.query(sql_get_all_groups(langcode))
        if err:
            #write log
            errors = 1

        err, supergroups, msg = conn.query(sql_get_supergroups(langcode, collation))
        if err:
            #write log
            errors = 1

        err, themes, msg = conn.query(sql_get_themes(4, langcode, collation))
        if err:
            #write log
            errors = 1

        conn.closeConnection()
        conn = None

        return (groups, supergroups, themes, errors)

    def get_namespace_version(self, namespace_id=1):
        for ns in self.fetch_namespaces():
            if ns['namespace_id'] == namespace_id:
                return ns['namespace_version']

        # if we get this far then we have an error
        return ''


    #####################
    #   MANAGEMENT TABS #
    #####################

#   security.declareProtected('Manage GimmeThesaurus', 'manage_properties')
#   manage_properties = PageTemplateFile('zpt/thesaurus_properties', globals())

    security.declarePublic('index_html')
    index_html = PageTemplateFile('zpt/thesaurus_index', globals())

    security.declarePublic('inspire_themes')
    inspire_themes = PageTemplateFile('zpt/thesaurus_inspire_themes', globals())

    security.declarePublic('gimme_template')
    thesaurus_template = PageTemplateFile('zpt/thesaurus_template', globals())

    security.declarePublic('style_css')
    style_css = PageTemplateFile('zpt/thesaurus_style_css', globals())

    security.declarePublic('_thesaurus_concept_link')
    thesaurus_concept_link = PageTemplateFile('zpt/thesaurus_concept_link', globals())

    security.declarePublic('theme_concepts')
    _theme_concepts_zpt = PageTemplateFile('zpt/thesaurus_themeconcepts', globals())
    def theme_concepts(self, REQUEST, th, langcode='en', start=0, letter=0, ns=4):
        """ """
        result = self.GetThemeConcepts(theme=th, langcode=langcode, start=start, letter=letter, namespace=ns)
        return self._theme_concepts_zpt(REQUEST, result=result, namespace=ns)

    _concept_zpt = PageTemplateFile('zpt/thesaurus_concept', globals())

    security.declarePublic('concept')
    def concept(self, REQUEST, cp, langcode='en', ns='1'):
        """ """
        if get_first_accept(REQUEST) == 'application/rdf+xml':
            return self.concept_as_rdf(REQUEST, cp, ns)

        result = self.GetConceptDetails(concept_id=cp, langcode=langcode, concept_ns=int(ns))
        return self._concept_zpt(REQUEST, result=result, concept_id=cp)

    security.declareProtected('View', 'concept_as_rdf')
    def concept_as_rdf(self, REQUEST, cp, ns='1'):
        """ Return a concept in RDF format """
        conn = DatabaseManager()
        try:
            conn.openConnection(self)
        except OperationalError, error:
            return None

        REQUEST.RESPONSE.setHeader('content-type', 'application/rdf+xml')
        err, prop_res, msg = conn.query(sql_get_properties_as_rdf(ns, cp))

        prefixes = {
          'http://www.w3.org/1999/02/22-rdf-syntax-ns#':'rdf',
          'http://www.w3.org/2004/02/skos/core#':'skos',
          'http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#':'gemet'
        }
        res = []
        res_a = res.append  #optimisation

        res_a('<?xml version="1.0" encoding="utf-8"?>')
        res_a('<rdf:RDF ')
        for u,p in prefixes.items():
           res_a(' xmlns:%s="%s"' % ( p, u))
        res_a('>')

        # Load necessary information about prefix and rdf:type from namespace table

        err, ns_res, msg = conn.query(sql_get_namespaces())
        thesauri = {}
        for ns_info in ns_res:
            thesauri[ns_info['namespace_id']] = ns_info

        res_a('<rdf:Description rdf:about="%s%s">' % (thesauri[long(ns)]['namespace_uri'], cp))
        res_a('<rdf:type rdf:resource="%s"/>' % thesauri[long(ns)]['namespace_type'])

        for property in prop_res:
            predicate = property['uri']
            prefixname = predicate
            for u,p in prefixes.items():
                if predicate[:len(u)] == u:
                    prefixname = p + ":" + predicate[len(u):]
            if property['is_resource'] == 1:
                res_a('<%s rdf:resource="%s"/>' % (prefixname, escape(property['value'])))
            else:
                res_a('<%s xml:lang="%s">%s</%s>' % (prefixname,property['langcode'],
                   escape(property['value']), prefixname))

        res_a('</rdf:Description>')
        res_a('</rdf:RDF>')
        conn.closeConnection()
        conn = None
#       return prop_res
        return '\n'.join(res)

    security.declareProtected('Manage GimmeThesaurus', 'administration')
    administration = PageTemplateFile('zpt/thesaurus_administration', globals())

    security.declarePublic('thesaurus_error')
    thesaurus_error = PageTemplateFile('zpt/thesaurus_error_page', globals())

    security.declarePublic('thesaurus_language_bar')
    thesaurus_language_bar = PageTemplateFile('zpt/thesaurus_language_bar', globals())

    security.declarePublic('alphabets')
    alphabets = PageTemplateFile('zpt/thesaurus_alphabets', globals())

    security.declarePublic('about')
    about = PageTemplateFile('zpt/thesaurus_about', globals())

    security.declarePublic('definition_sources')
    definition_sources = PageTemplateFile('zpt/thesaurus_definition_sources', globals())

    security.declarePublic('groups')
    groups = PageTemplateFile('zpt/thesaurus_groups', globals())

    security.declarePublic('relations')
    relations = PageTemplateFile('zpt/thesaurus_relations', globals())

    security.declarePublic('alphabetic')
    alphabetic = PageTemplateFile('zpt/thesaurus_alphabetic', globals())

    security.declarePublic('rdf')
    rdf = PageTemplateFile('zpt/thesaurus_rdfs', globals())

    security.declarePublic('search')
    search = PageTemplateFile('zpt/thesaurus_search', globals())

    security.declarePublic('getLangURL')
    def getLangURL(self, langcode, REQUEST=None):
        """ create the URLs for language icons """
        l_params =    'langcode=%s' % langcode
        l_qstr =      self.REQUEST['QUERY_STRING']

        for p in l_qstr.split('&'):
            param_name = p.split('=')[0]

            if param_name not in ['langcode', 'query'] and p:
                l_params ='%s&%s' % (l_params, p)

        return '%s?%s' % (self.REQUEST['URL0'], l_params)

    security.declarePublic('searchDB')
    def searchDB(self, query, langcode, REQUEST=None):
        """ """
        if REQUEST:
            return REQUEST.RESPONSE.redirect('search?langcode=%s&query=%s' % (langcode, query.encode('utf8')))

InitializeClass(Thesaurus)
