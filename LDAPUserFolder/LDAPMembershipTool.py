#####################################################################
#
# LDAPMembershipTool       LDAP-enabled CMF Membership Tool
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
#
#####################################################################
__version__='$Revision: 1297 $'[11:-2]

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ManageUsers
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Globals import InitializeClass
from Products.CMFDefault.MembershipTool import MembershipTool


class LDAPMembershipTool(MembershipTool):
    """ LDAP-enabled CMF Membership Tool """
    security = ClassSecurityInfo()
    meta_type = 'LDAP Membership Tool'
    title = 'LDAP Membership Tool'


    security.declarePrivate('addMember')
    def addMember(self, id, password, roles, domains, properties=None):
        """ Adds a new member to the user folder.  Security checks will have
        already been performed.  Called by portal_registration.
        """
        args = {}
        acl = self.acl_users
        login_attribute = acl.getProperty('_login_attr')
        rdn_attribute = acl.getProperty('_rdnattr')

        if ( rdn_attribute != login_attribute and 
             rdn_attribute not in properties.keys() ):
            raise ValueError, 'RDN attribute %s not provided.' % rdn_attribute
        
        args['user_pw'] = args['confirm_pw'] = password
        args[login_attribute] = id
        args['user_roles'] = roles

        if rdn_attribute != login_attribute:
            args[rdn_attribute] = properties[rdn_attribute]
        
        if properties.get('email', None):
            args['mail'] = properties['email']

        acl.manage_addUser(REQUEST=None, kwargs=args)
        self.createMemberarea(id)

        if properties is not None:
            member = self.getMemberById(id)
            member.setMemberProperties(properties)

    security.declareProtected(ManageUsers, 'deleteMembers')
    def deleteMembers(self, member_ids, delete_memberareas=1,
                      delete_localroles=1):
        """ Delete members specified by member_ids.
        """

        # Delete members in acl_users.
        acl_users = self.acl_users
        if _checkPermission(ManageUsers, acl_users):
            if isinstance(member_ids, basestring):
                member_ids = (member_ids,)
            member_ids = list(member_ids)
            member_dns = []
            for member_id in member_ids[:]:
                user = acl_users.getUserById(member_id)
                if user is None:
                    member_ids.remove(member_id)
                else:
                    member_dns.append(user.getUserDN())

            acl_users.manage_deleteUsers(dns=member_dns)

        else:
            raise AccessControl_Unauthorized('You need the \'Manage users\' '
                                 'permission for the underlying User Folder.')

        # Delete member data in portal_memberdata.
        mdtool = getToolByName(self, 'portal_memberdata', None)
        if mdtool is not None:
            for member_id in member_ids:
                mdtool.deleteMemberData(member_id)

        # Delete members' home folders including all content items.
        if delete_memberareas:
            for member_id in member_ids:
                 self.deleteMemberArea(member_id)

        # Delete members' local roles.
        if delete_localroles:
            utool = getToolByName(self, 'portal_url', None)
            self.deleteLocalRoles( utool.getPortalObject(), member_ids,
                                   reindex=1, recursive=1 ) 

        return tuple(member_ids)


InitializeClass(LDAPMembershipTool)
