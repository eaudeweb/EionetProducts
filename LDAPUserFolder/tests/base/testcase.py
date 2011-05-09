#####################################################################
#
# testcase      Test fixtures for LDAPUserFolder tests
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
#
#####################################################################
__version__='$Revision: 1010 $'[11:-2]

# General Python imports
import unittest, sys

# Zope imports
from OFS.Folder import Folder
import Testing
try:
    import Zope2
    import transaction
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
    transaction = None
Zope2.startup()

# Do some namespace manipulation to make use of FakeLDAP
from Products.LDAPUserFolder.tests import FakeLDAP
if sys.modules.has_key('_ldap'):
    del sys.modules['_ldap']
sys.modules['ldap'] = FakeLDAP
from Products.LDAPUserFolder import LDAPDelegate
LDAPDelegate.c_factory = FakeLDAP.ldapobject.ReconnectLDAPObject

# LDAPUserFolder package imports
from Products.LDAPUserFolder import manage_addLDAPUserFolder

# Tests imports
from Products.LDAPUserFolder.tests.config import defaults
from Products.LDAPUserFolder.tests.config import alternates
from Products.LDAPUserFolder.tests.config import user
from Products.LDAPUserFolder.tests.config import user2
from Products.LDAPUserFolder.tests.config import manager_user
dg = defaults.get
ag = alternates.get
ug = user.get
u2g = user2.get

class LDAPTest(unittest.TestCase):

    def setUp(self):
        FakeLDAP.clearTree()
        try:
            transaction.begin()
        except AttributeError:
            # Zope 2.7
            get_transaction().begin()
        self.connection = Zope2.DB.open()
        self.root =  self.connection.root()[ 'Application' ]
        self.root._setObject('luftest', Folder('luftest'))
        self.folder = self.root.luftest
        manage_addLDAPUserFolder(self.folder)
        luf = self.folder.acl_users
        host, port = dg('server').split(':')
        luf.manage_addServer(host, port=port)
        luf.manage_edit( dg('title')
                       , dg('login_attr')
                       , dg('uid_attr')
                       , dg('users_base')
                       , dg('users_scope')
                       , dg('roles')
                       , dg('groups_base')
                       , dg('groups_scope')
                       , dg('binduid')
                       , dg('bindpwd')
                       , binduid_usage = dg('binduid_usage')
                       , rdn_attr = dg('rdn_attr')
                       , local_groups = dg('local_groups')
                       , implicit_mapping = dg('implicit_mapping')
                       , encryption = dg('encryption')
                       , read_only = dg('read_only')
                       )
        FakeLDAP.addTreeItems(dg('users_base'))
        FakeLDAP.addTreeItems(dg('groups_base'))

    def tearDown( self ):
        try:
            transaction.abort()
        except AttributeError:
            # Zope 2.7
            get_transaction().abort()
        self.connection.close()

