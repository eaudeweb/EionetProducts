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
#

import re, copy
from string import *
from DateTime import DateTime

from OFS import SimpleItem, Image
from Globals import DTMLFile, MessageDialog
from AccessControl import getSecurityManager, Permissions, ClassSecurityInfo
from OFS.PropertyManager import PropertyManager
import Globals

from Utils import setFormError, isEmailValid, format_date

class Attendee(SimpleItem.SimpleItem,PropertyManager):
    """
    Course Attendee class
    """

    meta_type = 'Meeting Attendee'
    icon = 'misc_/ManagedMeetings/Attendee.gif'

    manage_options = PropertyManager.manage_options + (
        {'label': 'General', 'action': 'manage_editForm',},
        {'label': 'View', 'action': 'index_html',},
    )

    security = ClassSecurityInfo()
    security.declareProtected('Register for Meetings', 'manage_addAttendee')
    security.declareProtected('Change Meetings', 'manage_editForm')
    security.declareProtected('View', 'index_html')

    def __setstate__(self,state):
       Attendee.inheritedAttribute("__setstate__") (self, state)
       if not hasattr(self, 'passwd'):
           self.passwd = 'xyz'
       if not hasattr(self, 'ldap_id'):
           self.passwd = ''

    security.declareProtected('View', 'extraprops_addin')
    extraprops_addin = DTMLFile('www/DefaultPropsAddIn', globals())

    security.declareProtected('Change Meetings', 'manage_editAction')

    def manage_editAction(self, sn, givenname, organisation, mail,
            tel, postaladdress, attending, resume='', role='',
            verified=0, REQUEST=None):
        "Changes the product values"
        self.title = givenname + ' ' + sn
        self.sn = sn
        self.givenname = givenname
        self.organisation = organisation
        self.mail = mail
        self.tel = tel
        self.postaladdress = postaladdress
        if attending!=self.attending:
            self.subscription=DateTime()
        self.attending = attending
        self.role = role
        self.resume = resume
        self.verified = verified
        if REQUEST is not None:
            return MessageDialog(
                title = 'Edited',
                message = "The Attendee %s has been changed!" % self.id,
                action = 'manage_editForm',
                )

    index_html = DTMLFile('www/AttendeeIndex', globals())
    manage_editForm = DTMLFile('www/AttendeeEditForm', globals())

    security.declareProtected('Register for Meetings', 'AttendeeChangePreferences')
    AttendeeChangePreferences = DTMLFile('www/AttendeeChangePreferences', globals())

    security.declareProtected('Register for Meetings', 'AttendeeChangePreferencesLDAP')
    AttendeeChangePreferencesLDAP = DTMLFile('www/AttendeeChangePreferencesLDAP', globals())

    def propertyLabel(self, id):
        """Return a label for the given property id
        """
        for p in self._properties:
            if id == p['id'] and p.has_key('label'):
                return p['label']
        return id

    def getAttendeePassword(self):
        """Get password"""
        return self.passwd

    def delSession(self, key, REQUEST=None):
        """ delete from session"""
        del REQUEST.SESSION[key]

    security.declareProtected('Register for Meetings', 'changePreferences')
    def changePreferences(self, sn, givenname, organisation, tel, postaladdress, attending, role='Attendee',REQUEST=None):
        """ change preferences for an attendee"""
        if not sn:
            return self.AttendeeChangePreferences(setFormError(REQUEST, 'sn', 'Please enter your surname!'))
        if not givenname:
            return self.AttendeeChangePreferences(setFormError(REQUEST, 'givenname', 'Please enter your givenname!'))
        #if not mail:
        #    return self.AttendeeChangePreferences(setFormError(REQUEST, 'mail', 'Please enter your email address!'))
        #if mail and not isEmailValid(mail):
        #    return self.AttendeeChangePreferences(setFormError(REQUEST, 'mail', 'Your email address is invalid!'))

        try:
            do = self.superValues('Default Attendee Properties')[0]
            self._properties = do.propertyMap()
        except:
            self._properties = ()
        self.title = givenname + ' ' + sn
        self.sn = sn
        self.givenname = givenname
        self.organisation = organisation
        #self.mail = mail
        self.tel = tel
        self.postaladdress = postaladdress
        if attending!=self.attending:
            self.subscription=DateTime()
        self.attending = attending
        self.role = role
        self._p_changed = 1
        self.manage_editProperties(REQUEST) # Update properties
        if REQUEST is not None:
            return MessageDialog(title = 'Changed',
                message = "Your preferences have been changed",  action = 'index_html',)

# Initialize the class in order the security assertions be taken into account
Globals.InitializeClass(Attendee)

manage_addattendeeForm = DTMLFile('www/AttendeeAddForm', globals())

def manage_addAttendee(self,id , sn, givenname, organisation, mail,
        tel, postaladdress, attending, passwd, resume='', role='', verified=0,
        sendconfirm=0, ldap_id='', REQUEST=None):
    """ Add an attendee to a folder """

    title = givenname + ' ' + sn
    ob=Attendee()
    try:
        do = self.superValues('Default Attendee Properties')[0]
        ob._properties = do.propertyMap()
    except:
        ob._properties = ()
    if id == '':
        id = replace(mail.lower(), '@', '_')
    ob.id=id
    ob.title = title
    ob.sn = sn
    ob.givenname = givenname
    ob.organisation = organisation
    ob.mail = mail
    ob.tel = tel
    ob.postaladdress = postaladdress
    ob.attending = attending
    ob.role = role
    ob.resume = resume
    ob.verified = verified
    ob.subscription = DateTime()
    ob.passwd = passwd
    ob.ldap_id = ldap_id
    self._setObject(id, ob)
    ob=self._getOb(id)
    ob.manage_editProperties(REQUEST) # Update properties

    #send mail

    if self.location:
        location = self.getLocation(self.location)
    else:
        location = self.txtlocation

    if sendconfirm and len(ob.ldap_id)<>0:
        l_organizer_email = getattr(self, 'organiser_email', '')
        subject = "You have registered to participate at the " + self.title + "."
        sender = 'registration@eionet.europa.eu'
        comments = "You have been registered as " + ob.role + " to participate at the " + \
                self.title + " which will take place from " + format_date(self.startdate) + " to " + \
                format_date(self.enddate) + " at " + location + \
                ". \nIf you want to change your options go to the following link " + \
                ob.absolute_url() + "/attendeelist, click on your name and press `Edit`. For signing up use your LDAP account." + "\n\n"
        comments += "************************************************************************\n"
        comments += "THIS IS AN AUTOMATICALLY GENERATED MESSAGE.\n"
        if l_organizer_email != '':
            comments += "IF YOU REPLY TO IT, AN EMAIL WILL BE SENT TO THE ORGANISER OF THE EVENT.\n"
        else:
            comments += "DO NOT REPLY TO IT!\n"
            l_organizer_email = sender
        comments += "************************************************************************\n"
        ob.aq_parent._send_email(comments, subject, [], l_organizer_email, ob.mail, sender)
    else:
        l_organizer_email = getattr(self, 'organiser_email', '')
        subject = "You have registered to participate at the " + self.title + "."
        sender = 'registration@eionet.europa.eu'
        comments = "You have been registered as " + ob.role + " to participate at the " + \
                self.title + " which will take place from " + format_date(self.startdate) + " to " + \
                format_date(self.enddate) + " at " + location + \
                ". \nIf you want to change your options go to the following link " + \
                ob.absolute_url() + "/attendeelist, click on your name and press `Edit`" + \
                " to modify your profile using the password: " + ob.passwd + "\n\n"
        comments += "************************************************************************\n"
        comments += "THIS IS AN AUTOMATICALLY GENERATED MESSAGE.\n"
        if l_organizer_email != '':
            comments += "IF YOU REPLY TO IT, AN EMAIL WILL BE SENT TO THE ORGANISER OF THE EVENT.\n"
        else:
            comments += "DO NOT REPLY TO IT!\n"
            l_organizer_email = sender
        comments += "************************************************************************\n"
        ob.aq_parent._send_email(comments, subject, [], l_organizer_email, ob.mail, sender)

    if REQUEST is not None:
        return MessageDialog(
            title = 'Created',
            message = "The Attendee %s has been created!" % ob.id,
            action = 'manage_main?update_menu=1',
            )
