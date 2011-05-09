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
# Soren Roug, EEA
#

from OFS import SimpleItem, Image
from Globals import DTMLFile, MessageDialog
from AccessControl import getSecurityManager, Permissions, ClassSecurityInfo
from OFS.PropertyManager import PropertyManager
from ZPublisher.Converters import type_converters
from DateTime import DateTime
import Globals
from string import *
import re

class DefaultProps(SimpleItem.SimpleItem,PropertyManager):
    """
    Course DefaultProps class
    """

    meta_type = 'Default Attendee Properties'
    icon = 'misc_/ManagedMeetings/ExtraProps.gif'

    manage_options = PropertyManager.manage_options + (
        {'label': 'View', 'action': 'index_html',},
    )

    security = ClassSecurityInfo()
    security.declareProtected('Change Meetings', 'manage_addDefaultProps')
    security.declareProtected('View', 'index_html')

    index_html = DTMLFile('www/DefaultPropsIndex', globals())

    def propertyLabel(self, id):
        """Return a label for the given property id
        """
        for p in self._properties:
            if id == p['id'] and p.has_key('label'):
                return p['label']
        return id

    security.declareProtected('View', 'extraprops_addin')
    extraprops_addin = DTMLFile('www/DefaultPropsAddIn', globals())

    manage_propertiesForm=DTMLFile('dtml/properties', globals(),
                                       property_extensible_schema__=1)
    # Web interface

    def manage_addProperty(self, id, value, type, label, REQUEST=None):
        """Add a new property via the web. Sets a new property with
        the given id, type, and value."""
        if type_converters.has_key(type):
            value=type_converters[type](value)
        self._setProperty(id.strip(), value, type)
        if label != '':
            self._setPropLabel(id.strip(), label)
        if REQUEST is not None:
            return self.manage_propertiesForm(self, REQUEST)

    def manage_editProperties(self, REQUEST):
        """Edit object properties via the web.
        The purpose of this method is to change all property values,
        even those not listed in REQUEST; otherwise checkboxes that
        get turned off will be ignored.  Use manage_changeProperties()
        instead for most situations.
        """
        for prop in self._propertyMap():
            name=prop['id']
            if 'w' in prop.get('mode', 'wd'):
                value=REQUEST.get(name, '')
                self._updateProperty(name, value)
                label=REQUEST.get('lbl-'+name, '')
                if label != '':
                    self._setPropLabel(name, label)
                else:
                    self._delPropLabel(name)
        if REQUEST:
            message="Saved changes."
            return self.manage_propertiesForm(self,REQUEST,
                                              manage_tabs_message=message)
    def _setPropLabel(self, id, label):
        """Set the label of property 'id'"""
        for md in self._properties:
            if md['id']==id:
                md['label']=label

    def _delPropLabel(self, id):
        """Delete the label of property 'id'"""
        for md in self._properties:
            if md['id']==id and md.has_key('label'):
                del md['label']

# Initialize the class in order the security assertions be taken into account
Globals.InitializeClass(DefaultProps)


# constructor pages. Only used when the product is added to a folder.
manage_addDefaultPropsForm = DTMLFile('www/DefaultPropsAddForm', globals())

def manage_addDefaultProps(self, id, title, REQUEST=None):
    "Add an defaultprops to a folder."

    ob=DefaultProps()
    ob.id=id
    ob.title = title
    ob._properties = (
            {'id':'fax', 'type':'string',
             'label':'Telefax number', 'mode':'wd'},
        )
    for p in ob._properties:
        t = p['type']
        if t in ('string','text','boolean'):
            setattr(ob,p['id'],'')
        elif t == 'date':
            setattr(ob,p['id'],DateTime())
    self._setObject(id, ob)
    ob=self._getOb(id)
    if REQUEST is not None:
        return MessageDialog(
            title = 'Created',
            message = "The DefaultProps %s has been created!" % ob.id,
            action = 'manage_main?update_menu=1',
            )
