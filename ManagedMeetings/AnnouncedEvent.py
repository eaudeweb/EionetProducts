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
# Cornel Nitu, Finsiel Romania
# Rares Vernica, Finsiel Romania

from Event import BaseEvent
from Globals import DTMLFile, InitializeClass, package_home
from AccessControl import ClassSecurityInfo
from OFS import SimpleItem, ObjectManager, FindSupport
import webdav.Collection
import Products

from os.path import join
from time import *

manage_addAnnouncedEventForm=DTMLFile('www/AnnouncedEvent_addForm', globals())

def manage_addAnnouncedEvent(self, id, title, event_type, organiser,
       txtlocation, urllocation, description, startdate, enddate, status='', REQUEST=None):
    """Add a new Meeting object"""
    ob=AnnouncedEvent(id, title, event_type, organiser, txtlocation, urllocation,
          description, startdate, enddate, status, REQUEST)
    self._setObject(id, ob)
    ob=self._getOb(id)

    indexfile = open(join(package_home(globals()), 'www','AnnouncedEventIndex.dtml'))
    content = indexfile.read()
    indexfile.close()

    ob.manage_addDTMLMethod('index_html', title='Default View', file=content)

#   barfile = open(join(package_home(globals()), 'www','chooseBar.dtml'))
#   content = barfile.read()
#   barfile.close()

#   ob.manage_addDTMLMethod('choose_bar', title='', file=content)


    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class AnnouncedEvent(BaseEvent,ObjectManager.ObjectManager, webdav.Collection.Collection,
        SimpleItem.SimpleItem, FindSupport.FindSupport):
    """ A Folder-like product for EEA official holidays"""

    meta_type="Announced Event"
    security=ClassSecurityInfo()

    security.declareProtected('View management screens','manage_propertiesForm')
    manage_propertiesForm= DTMLFile('www/AnnouncedEventEdit', globals())

    def __str__(self): return self.index_html()
    def __len__(self): return 1

    security.declareProtected('View management screens','all_meta_types')
    def all_meta_types(self):
        """ What can you put inside me? """
        f = lambda x: x['name'] in (
                'DTML Method', 'DTML Document', 'Page Template',
                'Image', 'File','Meeting Location')
        return filter(f, Products.meta_types)

    manage_options=(
            (ObjectManager.ObjectManager.manage_options[0],)+
            (
            {'label':'Properties', 'action':'manage_propertiesForm',
             'help':('ManagedMeetings','Meeting_Edit.stx')},
            {'label':'View', 'action':'index_html', },
            )+
            SimpleItem.SimpleItem.manage_options+
            FindSupport.FindSupport.manage_options
            )

    def __init__(self, id, title, event_type, organiser, txtlocation, urllocation, description, startdate, enddate, status, REQUEST=None):
        """ initialize a new instance of AnnouncedEvent"""
        self.id=id
        self.title = title
        self.event_type = event_type
        self.organiser = organiser
        self.txtlocation = txtlocation
        self.urllocation = urllocation
        self.description = description
        self.startdate = startdate
        self.enddate = enddate
        self.status = status
        self.generation = 0

    security.declareProtected('View management screens','manage_editAnnouncedEvent')
    def manage_editAnnouncedEvent(self, title='', event_type='', txtlocation='', urllocation='',
            description='', startdate='', enddate='', organiser='', status='', REQUEST=None):
        """ Change the edited values """

        self.title = title
        self.event_type = event_type
        self.txtlocation = txtlocation
        self.urllocation = urllocation
        self.description = description
        self.startdate = startdate
        self.enddate = enddate
        self.organiser = organiser
        self.status = status
        self.generation = self.generation + 1
        if REQUEST:
            message="Saved changes."
            return self.manage_propertiesForm(self,REQUEST,manage_tabs_message=message)

    security.declarePublic('choose_bar')
    choose_bar=DTMLFile('www/chooseBar', globals())

    security.declarePublic('getAbsoluteURL')
    def getAbsoluteURL(self):
        """ return the absolute_url of the meeting """
        return self.absolute_url(0)


    security.declareProtected('View', 'locationtitle')
    def locationtitle(self,REQUEST=None):
        """Show location as text, same as for Meeting.py"""
        return self.txtlocation

    security.declareProtected('View', 'showlocation')
    def showlocation(self,REQUEST=None):
        """Show location with URL"""
        return self.txtlocation

InitializeClass(AnnouncedEvent)
