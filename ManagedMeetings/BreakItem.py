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
#


from OFS import SimpleItem
from Globals import DTMLFile, MessageDialog
from AccessControl import getSecurityManager, Permissions, ClassSecurityInfo
import Globals
from string import *
import re

class BreakItem(SimpleItem.SimpleItem):
    """
    Break class
    """

    meta_type = 'Meeting Break'
    icon = 'misc_/ManagedMeetings/break.gif'

    manage_options = (
        {'label': 'Properties', 'action': 'manage_editForm',},
        {'label': 'View', 'action': 'index_html',},
    )

    security = ClassSecurityInfo()

    def __setstate__(self,state):
        BreakItem.inheritedAttribute("__setstate__") (self, state)
        if not hasattr(self, "startdate"): # backwards compatibility
            self.startdate = self.starttime
        if not hasattr(self, "enddate"): # backwards compatibility
            self.enddate = self.endtime

    def manage_editAction (self, title, startdate, enddate, cost, REQUEST=None):
        "Changes the product values"
        self.title = title
        self.startdate = startdate
        self.enddate = enddate
#       self.track = track
        self.cost = cost
        if REQUEST:
            message="Saved changes."
            return self.manage_editForm(self,REQUEST,manage_tabs_message=message)


    index_html = DTMLFile('www/BreakItemIndex', globals())

    manage_editForm = DTMLFile('www/BreakItemEditForm', globals())

#   def tracklink(self,REQUEST=None):
#       """Show track with URL"""
#       if self.track != '':
#           locobj = self.aq_acquire(self.track)
#           return '<a href="%s">%s</a>' % \
#            ( locobj.absolute_url(), locobj.title )
#       else:
#           return ""

manage_addbreakItemForm = DTMLFile('www/BreakItemAddForm', globals())

def manage_addBreakItem(self, id, title, startdate, enddate, cost, REQUEST=None):
    """ Add an breakItem to a folder """

    ob=BreakItem()
    ob.id=id
    ob.title = title
    ob.startdate = startdate
    ob.enddate = enddate
#   ob.track = track
    ob.cost = cost
    ob.confirmed = 1
    self._setObject(id, ob)
    ob=self._getOb(id)
    if REQUEST is not None:
        return MessageDialog(
            title = 'Created',
            message = "The Meeting Break %s has been created!" % ob.id,
            action = 'manage_main?update_menu=1',
            )
