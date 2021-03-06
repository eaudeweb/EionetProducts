#####################################################################
#
# test_LDAPMemberDataTool - Tests for the LDAPMemberData tool
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
#
#####################################################################
""" Unit tests for LDAPMemberDataTool module.

$Id: test_LDAPMemberDataTool.py 37061 2005-06-15 14:17:41Z tseaver $
"""

from unittest import TestCase, TestSuite, makeSuite, main
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

import Acquisition

from OFS.Folder import Folder

try:
    from Products.LDAPUserFolder.tests.base.dummy import LDAPDummyUserFolder
    from Products.LDAPUserFolder.tests.base.dummy import LDAPDummyUser
except ImportError:
    pass


class DummyMemberDataTool(Acquisition.Implicit):
    pass


class LDAPMemberDataToolTests(TestCase):

    def _makeOne(self, *args, **kw):
        from Products.LDAPUserFolder.LDAPMemberDataTool import LDAPMemberDataTool

        return LDAPMemberDataTool(*args, **kw)

    def test_z2interfaces(self):
        from Interface.Verify import verifyClass
        from Products.CMFCore.interfaces.portal_actions \
                import ActionProvider as IActionProvider
        from Products.CMFCore.interfaces.portal_memberdata \
                import portal_memberdata as IMemberDataTool
        from Products.LDAPUserFolder.LDAPMemberDataTool import LDAPMemberDataTool

        verifyClass(IActionProvider, LDAPMemberDataTool)
        verifyClass(IMemberDataTool, LDAPMemberDataTool)

    def test_z3interfaces(self):
        try:
            from zope.interface.verify import verifyClass
            from Products.CMFCore.interfaces import IActionProvider
            from Products.CMFCore.interfaces import IMemberDataTool
            from Products.LDAPUserFolder.LDAPMemberDataTool import LDAPMemberDataTool

            verifyClass(IActionProvider, LDAPMemberDataTool)
            verifyClass(IMemberDataTool, LDAPMemberDataTool)
        except ImportError:
            # Running on Zope 2.7
            pass

    def test_deleteMemberData(self):
        tool = self._makeOne()
        tool.registerMemberData('Dummy', 'user_foo')
        self.failUnless( tool._members.has_key('user_foo') )
        self.failUnless( tool.deleteMemberData('user_foo') )
        self.failIf( tool._members.has_key('user_foo') )
        self.failIf( tool.deleteMemberData('user_foo') )

    def test_MemberPropertyManagement(self):
        folder = Folder('test_folder')
        folder._setObject('portal_memberdata', self._makeOne())
        folder._setObject('acl_users', LDAPDummyUserFolder())
        tool = folder.portal_memberdata
        ldap_schema = folder.acl_users.getSchemaConfig()

        # Starting out, no property is registered. All LDAPUserFolder schema
        # items are available for registration.
        self.assertEqual(len(tool.getSortedMemberProperties()), 0)
        available = tool.getAvailableMemberProperties()
        available_keys = [x['ldap_name'] for x in available]
        self.assertEqual( len(ldap_schema.keys())
                        , len(available)
                        )
        for ldap_property in ldap_schema.keys():
            self.failUnless(ldap_property in available_keys)

        # Now I am adding three properties. I'm also attempting to add an
        # unknown property, and add one of them twice. Those will be 
        # disregarded.
        tool.addMemberProperty('sn')
        tool.addMemberProperty('givenName')
        tool.addMemberProperty('telephoneNumber')
        tool.addMemberProperty('FOO')
        tool.addMemberProperty('givenName')
        available = tool.getAvailableMemberProperties()
        available_keys = [x['ldap_name'] for x in available]
        assigned = tool.getSortedMemberProperties()
        self.assertEqual(len(assigned), 3)
        self.assertEqual( len(ldap_schema.keys())
                        , len(available) + 3
                        )
        for property_info in assigned:
            self.failIf(property_info['ldap_name'] in available_keys)
        self.failIf('FOO' in [x['ldap_name'] for x in assigned])

        # One of the premises is that new attributes are always appended,
        # they appear last after they have been registered. We can predict
        # the order.
        assigned = tool.getSortedMemberProperties()
        self.assertEquals( [x['ldap_name'] for x in assigned]
                         , ['sn', 'givenName', 'telephoneNumber']
                         )

        # Now we start sorting them a bit
        tool.moveMemberPropertyUp('givenName')
        assigned = tool.getSortedMemberProperties()
        self.assertEquals( [x['ldap_name'] for x in assigned]
                         , ['givenName', 'sn', 'telephoneNumber']
                         )

        # Moving the top element up does nothing.
        tool.moveMemberPropertyUp('givenName')
        assigned = tool.getSortedMemberProperties()
        self.assertEquals( [x['ldap_name'] for x in assigned]
                         , ['givenName', 'sn', 'telephoneNumber']
                         )

        # Moving an unknown element up does nothing.
        tool.moveMemberPropertyUp('FOO')
        assigned = tool.getSortedMemberProperties()
        self.assertEquals( [x['ldap_name'] for x in assigned]
                         , ['givenName', 'sn', 'telephoneNumber']
                         )

        # Moving one down
        tool.moveMemberPropertyDown('sn')
        assigned = tool.getSortedMemberProperties()
        self.assertEquals( [x['ldap_name'] for x in assigned]
                         , ['givenName', 'telephoneNumber', 'sn']
                         )

        # Moving the bottom element down does nothing
        tool.moveMemberPropertyDown('sn')
        assigned = tool.getSortedMemberProperties()
        self.assertEquals( [x['ldap_name'] for x in assigned]
                         , ['givenName', 'telephoneNumber', 'sn']
                         )

        # Moving an unknown element down does nothing
        tool.moveMemberPropertyDown('FOO')
        assigned = tool.getSortedMemberProperties()
        self.assertEquals( [x['ldap_name'] for x in assigned]
                         , ['givenName', 'telephoneNumber', 'sn']
                         )

        # Now we are deleting one of the elements.
        tool.removeMemberProperty('telephoneNumber')
        assigned = tool.getSortedMemberProperties()
        available = tool.getAvailableMemberProperties()
        available_keys = [x['ldap_name'] for x in available]
        self.assertEquals( [x['ldap_name'] for x in assigned]
                         , ['givenName', 'sn']
                         )
        self.assertEqual(len(assigned), 2)
        self.assertEqual( len(ldap_schema.keys())
                        , len(available) + 2
                        )
        for property_info in assigned:
            self.failIf(property_info['ldap_name'] in available_keys)


class LDAPMemberDataTests(TestCase):

    def _makeOne(self, *args, **kw):
        from Products.LDAPUserFolder.LDAPMemberDataTool import LDAPMemberData

        return LDAPMemberData(*args, **kw)

    def test_z2interfaces(self):
        from Interface.Verify import verifyClass
        from Products.CMFCore.interfaces.portal_memberdata \
                import MemberData as IMemberData
        from Products.LDAPUserFolder.LDAPMemberDataTool import LDAPMemberData

        verifyClass(IMemberData, LDAPMemberData)

    def test_z3interfaces(self):
        try:
            from zope.interface.verify import verifyClass
            from Products.CMFCore.interfaces import IMemberData
            from Products.LDAPUserFolder.LDAPMemberDataTool import LDAPMemberData

            verifyClass(IMemberData, LDAPMemberData)
        except ImportError:
            # running on Zope 2.7
            pass

    def test_setSecurityProfile(self):
        from Products.LDAPUserFolder.LDAPMemberDataTool import LDAPMemberDataTool
        folder = Folder('test')
        folder._setOb('portal_memberdata', LDAPMemberDataTool())
        folder._setOb('acl_users', LDAPDummyUserFolder())
        user = LDAPDummyUser('bob', 'pw', ['Role'], ['domain'])
        folder.acl_users._addUser(user)
        user = folder.acl_users.getUser(user.getId())
        member = folder.portal_memberdata.wrapUser(user)
        member.setSecurityProfile(password='newpw')
        self.assertEqual(user.__, 'newpw')
        self.assertEqual(list(user.roles), ['Role'])
        self.assertEqual(list(user.domains), ['domain'])
        member.setSecurityProfile(roles=['NewRole'])
        self.assertEqual(user.__, 'newpw')
        self.assertEqual(list(user.roles), ['NewRole'])
        self.assertEqual(list(user.domains), ['domain'])
        member.setSecurityProfile(domains=['newdomain'])
        self.assertEqual(user.__, 'newpw')
        self.assertEqual(list(user.roles), ['NewRole'])
        self.assertEqual(list(user.domains), ['newdomain'])


def test_suite():
    try:
        from Products import CMFCore
        return TestSuite((
            makeSuite( LDAPMemberDataToolTests ),
            makeSuite( LDAPMemberDataTests ),
            ))
    except ImportError:
        # No CMF, no tests.
        return TestSuite(())

if __name__ == '__main__':
    main(defaultTest='test_suite')
