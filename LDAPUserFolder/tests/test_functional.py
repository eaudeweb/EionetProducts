#####################################################################
#
# test_join     "Functional" tests for adding members
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
#
#####################################################################
""" Unit tests for adding members.

$Id: test_join.py 37761 2005-08-06 14:52:28Z jens $
"""

from unittest import TestSuite, makeSuite, main, TestCase
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

from AccessControl.SecurityManagement import newSecurityManager

try:
    from Products.CMFCore.tests.base.testcase import RequestTest
    from Products.CMFDefault.tests.test_join import MembershipTests
except ImportError:
    RequestTest = MembershipTests = TestCase


class LDAPMembershipTests(MembershipTests):

    def _makePortal(self):
        from Acquisition import aq_base
        from Products.LDAPUserFolder.tests.base.dummy import LDAPDummyUserFolder
        try:
            factory = self.root.manage_addProduct['CMFDefault'].addConfiguredSite
        except AttributeError:
            # CMF 1.5.x
            factory = self.root.manage_addProduct['CMFSetup'].addConfiguredSite
        factory( 'site'
               , 'CMFDefault:default'
               , snapshot=False
               , extension_ids=('LDAPUserFolder:default',)
               )

        # Remove the "standard" user folder and replace it with a
        # LDAPDummyUserFolder
        self.root.site.manage_delObjects(['acl_users'])
        self.root.site._setObject('acl_users', LDAPDummyUserFolder())

        # Register one new attribute for testing
        self.root.site.portal_memberdata.addMemberProperty('sn')

        if hasattr(aq_base(self.root.site), 'clearCurrentSkin'):
            self.root.site.clearCurrentSkin()
        else: # CMF 1.4
            self.root.site._v_skindata = None

        self.root.site.changeSkin('Basic')
        return self.root.site


    def test_join_rdn_not_login( self ):
        # Test joing for situations where the login attribute is not the
        # same as the RDN attribute
        site = self._makePortal()
        site.acl_users._login_attr = 'sn'
        member_id = 'MyLastName'

        # If the RDN attribute is not provided, a ValueError is raised
        self.assertRaises( ValueError
                         , site.portal_registration.addMember
                         , member_id
                         , 'zzyyxx'
                         , properties={ 'username': member_id
                                      , 'email' : 'foo@bar.com'
                                      }
                         )
        u = site.acl_users.getUser(member_id)
        self.failIf(u)

        # We provide it, so this should work
        site.portal_registration.addMember( member_id
                                          , 'zzyyzz'
                                          , properties={ 'username': member_id
                                                       , 'email' : 'foo@bar.com'
                                                       , 'cn' : 'someuser'
                                                       }
                                          )
        u = site.acl_users.getUser(member_id)
        self.failUnless(u)


class LDAPMembershipFunctionalTests(RequestTest):

    def _makePortal(self):
        from Products.LDAPUserFolder.tests.base.dummy import LDAPDummyUserFolder
        try:
            factory = self.root.manage_addProduct['CMFDefault'].addConfiguredSite
        except AttributeError:
            # CMF 1.5.x
            factory = self.root.manage_addProduct['CMFSetup'].addConfiguredSite

        factory( 'site'
               , 'CMFDefault:default'
               , snapshot=False
               , extension_ids=('LDAPUserFolder:default',)
               )

        # Remove the "standard" user folder and replace it with a
        # LDAPDummyUserFolder
        self.root.site.manage_delObjects(['acl_users'])
        self.root.site._setObject('acl_users', LDAPDummyUserFolder())

        # Register member properties with the shiny new member data tool
        mdt = self.root.site.portal_memberdata
        mdt.addMemberProperty('sn')
        mdt.addMemberProperty('givenName')
        mdt.addMemberProperty('telephoneNumber')

        return self.root.site


    def test_join_superhighlevel(self):
        # Make sure the member data wrapper carries correct properties
        # after joining
        site = self._makePortal()
        member_id = 'test_user'

        controller_script = site.members_add_control
        status = controller_script(member_id, 'zzyyzz', 'foo@bar.com')

        # If everything worked correctly, the status will be False and the
        # portal_status_message will proclaim success
        self.assertEqual(status, False)
        self.assertEqual( str(site.REQUEST.other['portal_status_message'])
                        , 'Success!'
                        )

        m = site.portal_membership.getMemberById('test_user')
        self.assertEqual(m.getProperty('email'), 'foo@bar.com')
        self.assertEqual(m.getMemberId(), member_id)
        self.assertEqual(m.getRoles(), ('Member', 'Authenticated'))


    def test_personalize(self):
        site = self._makePortal()
        member_id = 'test_user'

        join_script = site.members_add_control
        personalize_script = site.personalize

        join_script(member_id, 'zzyyzz', 'foo@bar.com')
        m = site.portal_membership.getMemberById('test_user')

        # Log in as the new member because the personalization step is
        # operating on whoever is logged in at that moment
        newSecurityManager(None, m.getUser())

        # Stuff all values into the request becausse that's what the personalize
        # script uses to get values from
        req = self.root.REQUEST
        req.form = {}
        req.form['email'] = 'baz@foo.com'
        req.form['listed'] = 'on'
        req.form['portal_skin'] = 'Nouvelle'
        req.form['sn'] = 'Blow'
        req.form['givenName'] = 'Joe'
        req.form['telephoneNumber'] = '(888) 555-1212'

        personalize_script()

        m = site.portal_membership.getMemberById('test_user')
        self.assertEqual(m.getProperty('email'), 'baz@foo.com')
        self.failUnless(m.getProperty('listed'))
        self.assertEqual(m.getProperty('portal_skin'), 'Nouvelle')
        self.assertEqual(m.getProperty('sn'), 'Blow')
        self.assertEqual(m.getProperty('givenName'), 'Joe')
        self.assertEqual(m.getProperty('telephoneNumber'), '(888) 555-1212')


def test_suite():
    try:
        from Products import CMFCore
        return TestSuite((
            makeSuite(LDAPMembershipTests),
            makeSuite(LDAPMembershipFunctionalTests),
            ))
    except ImportError:
        # No CMF, no tests.
        return TestSuite(())

if __name__ == '__main__':
    main(defaultTest='test_suite')
