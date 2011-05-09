###############################################################################
### NOTE: This script is OBSOLETE. The Web-services API has changed
###############################################################################

import xmlrpclib

_SERVER = 'http://www.eionet.europa.eu/gemet'

def xmlrpc_open():
    server = xmlrpclib.ServerProxy(_SERVER, allow_none=True)
    return server

def searchForConcepts(query, langcode, level):
    """ search for a concept """
    server = xmlrpc_open()
    return server.searchForConcepts(query, langcode, level)

def fetchThemes(lang):
    """ return all themes """
    server = xmlrpc_open()
    return server.fetchThemes(lang)

def fetchGroups(lang):
    """ return all groups """
    server = xmlrpc_open()
    return server.fetchGroups(lang)

def fetchConcepts(nameScopeList, attributes, lang):
    """ fetch concepts """
    server = xmlrpc_open()
    return server.fetchConcepts(nameScopeList, attributes, lang)

def fetchHier(concept, scope, level, direction, lang):
    """ fetch either the parents or children of indx to specified level """
    server = xmlrpc_open()
    nameScope = {'name':concept, 'scope':scope}
    return server.fetchHier(nameScope, level, direction, lang)

def fetchSiblings(nameScopeList, attributes, lang):
    """ return all the children of all the parents
        of the terms specified in nameScopeList"""
    server = xmlrpc_open()
    return server.fetchSiblings(nameScopeList, attributes, lang)

def fetchConceptsById(ids, attributes, lang):
    """ return the matching concepts """
    server = xmlrpc_open()
    return server.fetchConceptsById(ids, attributes, lang)

def fetchTopConcepts(lang):
    """ return all top concepts """
    server = xmlrpc_open()
    return server.fetchTopConcepts(lang)

###
#   Absolute API
######

#def fetchHierById(id, level, direction, lang):
#    """ fetch hierarchy """
#    server = xmlrpc_open()
#    return server.fetchHierById(id, level, direction, lang)
#
#def fetchCluster(nameScopeList, attributes, lang):
#    """ """
#    server = xmlrpc_open()
#    return server.fetchCluster(nameScopeList, attributes, lang)
#
#def identifyConceptById(id, lang):
#    """ return concept's name and scope given the id"""
#    server = xmlrpc_open()
#    return server.identifyConceptById(id, lang)
