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
# The Original Code is ManagedMeetings version 1.0.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by CMG and Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Tomas Hjelmberg, CMG
#

from OFS import SimpleItem, ObjectManager, FindSupport
import AccessControl.Role, webdav.Collection
from webdav.WriteLockInterface import WriteLockInterface
from Globals import DTMLFile, MessageDialog, InitializeClass, package_home
from AccessControl import getSecurityManager, Permissions, ClassSecurityInfo

import os
from os.path import join
import re
import string
import tempfile
import types
import StringIO
import Products

manage_addLocationForm=DTMLFile('www/Location_addForm', globals())

def manage_addLocation(self, id, description, title,
        address, url, map_url, roadmap_url,
        max_seats, REQUEST=None):
    """Add a new Location object with id=title, uploading file."""

    ob=Location()
    ob.id = id
    ob.title = title
    ob.description = description
    ob.address = address
    ob.url = url
    ob.map_url = map_url
    ob.roadmap_url = roadmap_url
    ob.max_seats = max_seats
    self._setObject(id, ob)
    ob=self._getOb(id)

    indexfile = open(join(package_home(globals()), 'www','LocationIndex.dtml'))
    content = indexfile.read()
    indexfile.close()

    ob.manage_addDTMLMethod('index_html', title='Default View', file=content)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class Location(
    ObjectManager.ObjectManager,
    AccessControl.Role.RoleManager,
    webdav.Collection.Collection,
    SimpleItem.Item,
    FindSupport.FindSupport,
    ):
    """Meeting location"""

    __implements__ = (WriteLockInterface,)

    meta_type="Meeting Location"

    security = ClassSecurityInfo()

    security.declareProtected('Change Meetings', 'manage_editLocation')
    security.declareProtected('Change Meetings', 'LocationEdit')
    security.declareProtected('View', 'index_html')

    ################################
    # Public methods               #
    ################################

    def __str__(self): return self.index_html()
    def __len__(self): return 1

    def all_meta_types(self):
        """ What can you put inside me? """
        f = lambda x: x['name'] in ('DTML Method', 'DTML Document', 'File','Image')
        return filter(f, Products.meta_types)

    def manage_addObject(self):
        """Add a new object to the Location"""
        #ob=self._getOb(id)

        checkPermission=getSecurityManager().checkPermission

        if file is not None:
            if not checkPermission('Add Documents, Images, and Files', ob):
                raise 'Unauthorized', (
                    'You are not authorized to add DTML Documents.'
                    )
            return ob.manage_upload(file,subfolders,REQUEST=REQUEST)

        if REQUEST is not None:
            return MessageDialog(title = 'Created',
                                 message = 'The Location %s was successfully created!' % id,
                                 action = 'manage_main?update_menu=1',)

    manage_options=(
        (ObjectManager.ObjectManager.manage_options[0],)+
        (
        {'label':'Properties', 'action':'LocationEdit',
         'help':('ManagedMeetings','Location_Edit.stx')},
        {'label':'View', 'action':'index_html', },
        )+
        AccessControl.Role.RoleManager.manage_options+
        SimpleItem.Item.manage_options+
        FindSupport.FindSupport.manage_options
        )

    LocationEdit= DTMLFile('www/LocationEdit', globals()) # Edit the content of the object

#   index_html = DTMLFile('www/LocationIndex', globals()) # Show the content of the object

    ################################
    # Protected management methods #
    ################################

    # Management Interface
    #manage_main = DTMLFile('www/LocationEdit', globals())

    def manage_editLocation(self, title='', description='',
            address='', url='', map_url='', roadmap_url='',
            max_seats='', REQUEST=None):
        """ Manage the edited values """

        self.title = title
        self.description = description
        self.title = title
        self.address = address
        self.url = url
        self.map_url = map_url
        self.roadmap_url = roadmap_url
        self.max_seats = max_seats

        # update ZCatalog
        # self.reindex_object()
        if REQUEST:
            message="Saved changes."
            return self.LocationEdit(self,REQUEST,manage_tabs_message=message)

# Initialize the class in order the security assertions be taken into account
InitializeClass(Location)
