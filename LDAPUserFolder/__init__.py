##############################################################################
#
# __init__.py	Initialization code for the LDAPUserFolder
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
# 
##############################################################################

__doc__     = """ LDAPUserFolder initialization module """
__version__ = '$Revision: 1245 $'[11:-2]

from AccessControl.Permissions import add_user_folders

from LDAPUserFolder import manage_addLDAPUserFolder, LDAPUserFolder
from LDAPUserSatellite import addLDAPUserSatelliteForm, \
                              manage_addLDAPUserSatellite, \
                              LDAPUserSatellite

try:
    from Products.CMFCore.DirectoryView import registerDirectory
    from Products.CMFSetup import EXTENSION

    from Products.CMFSetup import profile_registry 
    # Make the skins available as DirectoryViews
    registerDirectory('skins', globals())

    have_cmf = True
except ImportError:
    have_cmf = False


def initialize(context):
    context.registerClass( LDAPUserFolder
                         , permission=add_user_folders
                         , constructors=(manage_addLDAPUserFolder,)
                         , icon='www/ldapuserfolder.gif'
                         )

    context.registerClass( LDAPUserSatellite
                         , permission=add_user_folders
                         , constructors=( addLDAPUserSatelliteForm
                                        , manage_addLDAPUserSatellite
                                        )
                         , icon='www/ldapusersatellite.gif'
                         )

    context.registerHelp()

    if have_cmf is True:
        profile_registry.registerProfile( 'default'
                                        , 'LDAPUserFolder CMF Tools'
                                        , 'Adds LDAP support to the CMF.'
                                        , 'profiles/default'
                                        , 'LDAPUserFolder'
                                        , EXTENSION
                                        )

