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

from OFS import SimpleItem, Image
from Globals import DTMLFile, MessageDialog
from AccessControl import getSecurityManager, Permissions, ClassSecurityInfo
import Globals
from string import *
import re

class AgendaItem(SimpleItem.SimpleItem):
    """
    Agenda Item class
    """

    meta_type = 'Meeting Agendaitem'
    icon='misc_/ManagedMeetings/agenda.gif'

    manage_options = (
        {'label': 'Properties', 'action': 'manage_editForm',},
        {'label': 'View', 'action': 'index_html',},
    )

    # Create a SecurityInfo for this class. We will use this
    # in the rest of our class definition to make security
    # assertions.
    security = ClassSecurityInfo()


#   def __setstate__(self,state):
#       AgendaItem.inheritedAttribute("__setstate__") (self, state)
#       if not hasattr(self, "location"): # backwards compatibility
#           self.location = self.room
#       if not hasattr(self, "speakers"): # backwards compatibility
#           self.speakers = [self.speaker]

    security.declareProtected('Change Meetings', 'manage_editAction')

    def manage_editAction(self, title, track, session, session_ord,
            duration, location, author, abstract,
            paper_url, slides_url, url, keywords, actions_agreed,
            actions_comp, minutes, confirmed=0, speakers=[], REQUEST=None):
        "Changes the product values"
        self.title = title
        self.track = track
        self.session = session
        self.session_ord = session_ord
        self.duration = duration
        self.location = location
        self.speakers = speakers
        self.author = author
        self.abstract = abstract
        self.paper_url = paper_url
        self.slides_url = slides_url
        self.url = url
        self.keywords = keywords
        self.actions_agreed = actions_agreed
        self.actions_comp = actions_comp
        self.minutes = minutes
        self.confirmed = confirmed
        if REQUEST:
            message="Saved changes."
            return self.manage_editForm(self,REQUEST,
               manage_tabs_message=message)

    security.declareProtected('View', 'showlocation')

    def showlocation(self,REQUEST=None):
        """Show location with URL"""
        if self.location != '':
            locobj = self.aq_acquire(self.location)
            return '<a href="%s">%s</a>' % \
             ( locobj.absolute_url(), locobj.title )
        else:
            return None

    security.declareProtected('View', 'showsession')

    def showsession(self,REQUEST=None):
        """Show session title"""
        if self.session != '':
            locobj = self.aq_acquire(self.session)
            return '%s' % locobj.title
        else:
            return None

    security.declareProtected('View', 'trackobj')

    def trackobj(self):
        "Get the track object of the agenda item"
        if self.track != '':
            return self.aq_acquire(self.track)
        else:
            return None

    security.declareProtected('View', 'tracklink')

    def tracklink(self,REQUEST=None):
        """Show track with URL"""
        if self.track != '':
            locobj = self.aq_acquire(self.track)
            return '<a href="%s">%s</a>' % \
             ( locobj.absolute_url(), locobj.title )
        else:
            return ""

    security.declareProtected('View', 'speakerlink')

    def speakerlink(self,speaker):
        """Show track with URL"""
        if speaker != '':
            locobj = self.aq_acquire(speaker)
            return '<a href="%s">%s</a>, %s' % \
             ( locobj.absolute_url(), locobj.title, locobj.organisation )
        else:
            return ""

    security.declareProtected('View', 'index_html')

    index_html = DTMLFile('www/AgendaItemIndex',
                          globals()) # Used to view content of the object

    security.declareProtected('Change Meetings', 'manage_editForm')

    manage_editForm = DTMLFile('www/AgendaItemEditForm',
                               globals()) # Edit the content of the object

    # constructor pages. Only used when the product is added to a folder.

# Initialize the class in order the security assertions be taken into account
Globals.InitializeClass(AgendaItem)

manage_addagendaItemForm = DTMLFile('www/AgendaItemAddForm', globals())

def manage_addAgendaItem(self, id, title, track, session, session_ord,
        duration, location, author, abstract,
        paper_url, slides_url, url, keywords, actions_agreed, actions_comp,
        minutes, speakers=[],confirmed=0, REQUEST=None):
    "Add an agendaItem to a folder."

    ob=AgendaItem()
    ob.id=id
    ob.title = title
    ob.track = track
    ob.session = session
    ob.session_ord = session_ord
    ob.duration = duration
    ob.location = location
    ob.speakers = speakers
    ob.author = author
    ob.abstract = abstract
    ob.paper_url = paper_url
    ob.slides_url = slides_url
    ob.url = url
    ob.keywords = keywords
    ob.actions_agreed = actions_agreed
    ob.actions_comp = actions_comp
    ob.minutes = minutes
    ob.confirmed = confirmed
    self._setObject(id, ob)
    ob=self._getOb(id)
    if REQUEST is not None:
        return MessageDialog(
            title = 'Created',
            message = "The Agenda item %s has been created!" % ob.id,
            action = 'manage_main?update_menu=1',
            )
