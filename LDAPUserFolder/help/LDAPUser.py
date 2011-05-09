#####################################################################
#
# LDAPUser Interface: The User object interface for the LDAPUserFolder
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
#
#####################################################################

class LDAPUser:
    """
    This interface is supported by user objects which
    are returned by user validation through the LDAPUserFolder 
    product and used for access control.

    Some implementations are inherited from the base class 
    AccessControl.User.BasicUser, so if you don't find a method 
    in this listing in the LDAPUser module, look there.
    """

    def getUserName():
        """

        Return the login of a user

        Permission - Always available
        
        """

    def getId():
        """

        Return the User ID (which can be different from the login)

        Permission - Always available

        """

    def getRoles(object):
        """

        Returns a list of the roles the user has on the given object
        (in the current context?)

        Permission - Always available

        """

    def getProperty(name, default=''):
        """

        Retrieve the value of a property of name "name". If this 
        property does not exist, the default value is returned.

        Properties can be any public attributes that are part of the 
        user record in LDAP. Refer to them by their LDAP attribute
        name or the name they have been mapped to in the LDAP User 
        Folder

        Permission - View

        """

    def getUserDN():
        """

        Retrieve the user object's Distinguished Name attribute.

        Permission - View

        """

    def notexpired():
        """

        Returns 1 if the user record has not expired, 0 otherwise.

        Permission - Always available

        """
