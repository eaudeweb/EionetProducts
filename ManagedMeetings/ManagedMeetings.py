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
# Soren Roug, EEA
# Cornel Nitu, Finsiel Romania
# Rares Vernica, Finsiel Romania

__doc__ = """
              ManagedMeetings product module.
              The ManagedMeetings-Product is a meeting-scheduler/planner

$Id: ManagedMeetings.py 9869 2007-10-17 13:54:11Z nituacor $
"""

__version__='$Revision: 1.26 $'[10:-2]


from OFS import Folder,Image
from Globals import DTMLFile, MessageDialog, InitializeClass, package_home
from AccessControl import getSecurityManager, Permissions, ClassSecurityInfo

import Products
import os
from os.path import join
import re
import string
import tempfile
import types
import StringIO

manage_addManagedMeetingsForm=DTMLFile('www/ManagedMeetings_addForm', globals())

def manage_addManagedMeetings(self, id, title='', description='',
        event_types=[], mailhost='', REQUEST=None):
    """Add a new ManagedMeetings object with id=title."""

    ob=ManagedMeetings(id, title, description, event_types, mailhost)
    ob.id = id
    self._setObject(id, ob)

    indexfile = open(join(package_home(globals()), 'www','ManagedMeetingsIndex.dtml'))
    content = indexfile.read()
    indexfile.close()
    ob.manage_addDTMLMethod('index_html', title='Current/Future Events', file=content)

    indexfile = open(join(package_home(globals()), 'www','ManagedMeetingsPast.dtml'))
    content = indexfile.read()
    indexfile.close()
    ob.manage_addDTMLMethod('past_html', title='Past Events', file=content)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

def getMailHostList(self):
    """ list of mail hosts """
    try:
        mailhost_list=self.superValues('Mail Host')
        newlist=[]
        for host in mailhost_list:
            newlist.append(host.absolute_url(relative=1))
        return newlist
    except:
        return []

class ManagedMeetings(Folder.Folder):
    """A Folder-like product that can contain Attendees and course-material"""

    meta_type="Folder for Meetings"

    # what properties have we?
    _properties=(
        {'id':'title',          'type':'string'},
        {'id':'description',    'type':'text'},
        {'id':'event_types',    'type':'lines'},
        {'id':'mailhost',       'type':'selection', 'select_variable':'getMailHostList'},
        {'id':'mail_enconding', 'type':'string'}
    )

    security = ClassSecurityInfo()

    security.declareProtected('View', 'index_html')

    ################################
    # Public methods               #
    ################################

    def __str__(self): return self.index_html()
    def __len__(self): return 1

    getMailHostList=getMailHostList

    def all_meta_types(self):
        """ What can you put inside me? """
        f = lambda x: x['name'] in ('DTML Method', 'DTML Document',
            'Page Template', 'Meeting Location', 'Meeting', 'File', 'Announced Event')
        return filter(f, Products.meta_types)

    def manage_addObject(self):
        """Add a new object to the Meeting"""
        ob=self._getOb(id)

        checkPermission=getSecurityManager().checkPermission

        if file is not None:
            if not checkPermission('Add Documents, Images, and Files', ob):
                raise 'Unauthorized', (
                    'You are not authorized to add DTML Documents.'
                    )
            return ob.manage_upload(file,subfolders,REQUEST=REQUEST)

        if REQUEST is not None:
            return MessageDialog(title = 'Created',
                     message = 'The ManagedMeetings %s was successfully created!' % id,
                     action = 'manage_main',)

    security.declareProtected('View', 'getLocation')
    def getLocation(self, id):
        """ get location name """
        try:
            return self._getOb(id).title_or_id()
        except AttributeError:
            return id

    ## manage_options=(Folder.Folder.manage_options+
##                    ({ "label": "ManagedMeetings",
##                       "action": "MeetingEdit"},)
##                    )
#   manage_addLocationForm=DTMLFile('www/Location_addForm', globals())
#   manage_addMeetingForm=DTMLFile('www/Meeting_addForm', globals())
#   location_add = DTMLFile('www/location_add', globals()) # Add a location
#   meeting_add = DTMLFile('www/meeting_add', globals()) # Add a meeting

    security.declareProtected('View', 'open_rss')
    open_rss = DTMLFile('www/openrdf', globals())

    ################################
    # Init method                  #
    ################################

    def __init__(self, id, title='', description='',event_types=[], mailhost='', mail_enconding='', REQUEST=None):
        """ initialize a new instance of ManagedMeetings """
        self.id = id
        self.title = title
        self.description = description
        self.event_types = event_types
        self.mailhost = mailhost
        self.mail_enconding = mail_enconding

    def __setstate__(self,state):
        ManagedMeetings.inheritedAttribute("__setstate__") (self, state)
        if not hasattr(self, "event_types"): # backwards compatibility
            self.event_types = []

        if not hasattr(self, "mailhost"): # backwards compatibility
            self.mailhost = []

        if not hasattr(self, "mail_enconding"): # backwards compatibility
            self.mail_enconding = 'utf-8'

    ################################
    # Protected management methods #
    ################################

    security.declareProtected('Change Meetings folders', 'manage_editManagedMeetings')

    def manage_editManagedMeetings(self, title='', description='', event_types=[],mailhost='', mail_enconding='', REQUEST=None):
        """ Manage the edited values """

        self.title = title
        self.description = description
        self.event_types = event_types
        self.mailhost = mailhost
        self.mail_enconding = mail_enconding

        # update ZCatalog
        # self.reindex_object()
        if REQUEST is not None:
            return MessageDialog(
                title = 'Edited',
                message = "The properties of %s have been changed!" % self.id,
                action = './manage_main',
                )


# Initialize the class in order the security assertions be taken into account
InitializeClass(ManagedMeetings)
