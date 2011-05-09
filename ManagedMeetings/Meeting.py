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

from Event import BaseEvent
from webdav.WriteLockInterface import WriteLockInterface
from AccessControl import getSecurityManager, Permissions, ClassSecurityInfo
from Globals import DTMLFile, MessageDialog, InitializeClass, package_home
from OFS import SimpleItem, ObjectManager, FindSupport
import webdav.Collection
import Products


from os.path import join
import re
import string
from DateTime import DateTime
from time import *
from Persistence import Persistent # for setstate backwards compatibility

# product imports
#import AgendaItem
import Attendee
#import BreakItem
#import Session
#import Track
import DefProps

from Utils import setFormError, isEmailValid, genRandomId

#Try to import MessageBoard product
try:
    from Products.MessageBoard import *
    MBinstalled=1
except:
    MBinstalled=0

manage_addMeetingForm=DTMLFile('www/Meeting_addForm', globals())

def manage_addMeeting(self, id, title, event_type, location,
        txtlocation, description, startdate, enddate,
        organiser, organiser_email, max_attendees,
        agenda_url='',minutes_url='',
        allow_registrations=0, allow_anonymous=0, status='', REQUEST=None):
    """Add a new Meeting object"""

    if DateTime(str(startdate)) > DateTime(str(enddate)):
        return self.manage_addMeetingForm(setFormError(REQUEST, 'invalid_date', 'End date is earlier than start date'))
    ob=Meeting()
    ob.id=id
    ob.title = title
    ob.event_type = event_type
    ob.location = location
    if location:
        ob.txtlocation = ''
    else:
        ob.txtlocation=txtlocation
    ob.description = description
    ob.startdate = startdate
    ob.enddate = enddate
    ob.agenda_url = agenda_url
    ob.minutes_url = minutes_url
    ob.organiser = organiser
    ob.organiser_email = organiser_email
    ob.max_attendees = max_attendees
    if allow_registrations:
        ob.allow_registrations = 1
    else:
        ob.allow_registrations = 0
    ob.allow_anonymous = allow_anonymous
    ob.status = status
    ob.generation = 0
    self._setObject(id, ob)
    ob=self._getOb(id)

    dtmlfile = open(join(package_home(globals()), 'www', 'MeetingIndex.dtml'))
    content = dtmlfile.read()
    dtmlfile.close()
    ob.manage_addDTMLMethod('index_html', title='Default View', file=content)

#   dtmlfile = open(join(package_home(globals()), 'www','chooseBar.dtml'))
#   content = dtmlfile.read()
#   dtmlfile.close()
#   ob.manage_addDTMLMethod('choose_bar', title='', file=content)

    dtmlfile = open(join(package_home(globals()), 'www', 'AttendeesList.dtml'))
    content = dtmlfile.read()
    dtmlfile.close()
    ob.manage_addDTMLMethod('list_of_attendees',
        title='Example of attendee list', file=content)

    if MBinstalled:
        mailhost = MessageBoard.getMailHostList(self)
        ob.manage_addProduct['MessageBoard'].manage_addMessageBoard(id='MaillingList', \
            title='Mailing list',
            description='Note: Everything that was emailed to all attendees is automatically posted here also', mailhost=mailhost[0])


    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class Meeting(BaseEvent,ObjectManager.ObjectManager,
                webdav.Collection.Collection,SimpleItem.SimpleItem,
                FindSupport.FindSupport):
    """A Folder-like product that can contain Attendees and course-material"""

    meta_type="Meeting"

    # Create a SecurityInfo for this class. We will use this
    # in the rest of our class definition to make security
    # assertions.
    security = ClassSecurityInfo()
    security.declareProtected('View', 'index_html')

    security.declareProtected('Register for Meetings', 'manage_addAnonAttendeeAction')

    ################################
    # Public methods               #
    ################################

    def __str__(self): return self.index_html()
    def __len__(self): return 1

    genRandomId = genRandomId

    manage_addMeetingForm = manage_addMeetingForm
    # Subobjects constructors
#   security.declareProtected('Add Meeting', 'manage_addagendaItemForm')
#   manage_addagendaItemForm = AgendaItem.manage_addagendaItemForm
#   security.declareProtected('Add Meeting', 'manage_addAgendaItem')
#   manage_addAgendaItem = AgendaItem.manage_addAgendaItem

    security.declareProtected('Add Meeting', 'manage_addattendeeForm')
    manage_addattendeeForm = Attendee.manage_addattendeeForm
    security.declareProtected('Add Meeting', 'manage_addAttendee')
    manage_addAttendee = Attendee.manage_addAttendee

#   security.declareProtected('Add Meeting', 'manage_addbreakItemForm')
#   manage_addbreakItemForm = BreakItem.manage_addbreakItemForm
#   security.declareProtected('Add Meeting', 'manage_addBreakItem')
#   manage_addBreakItem = BreakItem.manage_addBreakItem

#   security.declareProtected('Add Meeting', 'manage_addSessionForm')
#   manage_addSessionForm = Session.manage_addSessionForm
#   security.declareProtected('Add Meeting', 'manage_addSession')
#   manage_addSession = Session.manage_addSession

#   security.declareProtected('Add Meeting', 'manage_addTrackForm')
#   manage_addTrackForm = Track.manage_addTrackForm
#   security.declareProtected('Add Meeting', 'manage_addTrack')
#   manage_addTrack = Track.manage_addTrack

    security.declareProtected('Add Meeting', 'manage_addDefaultPropsForm')
    manage_addDefaultPropsForm = DefProps.manage_addDefaultPropsForm
    security.declareProtected('Add Meeting', 'manage_addDefaultProps')
    manage_addDefaultProps = DefProps.manage_addDefaultProps

    def all_meta_types(self):
        """ What can you put inside me? """
        y = [  {'name': 'Default Attendee Properties', 'action': 'manage_addDefaultPropsForm'},
        {'name': 'Meeting Attendee', 'action': 'manage_addattendeeForm'},
#       {'name': 'Meeting Session', 'action': 'manage_addSessionForm'},
#       {'name': 'Meeting Agendaitem', 'action': 'manage_addagendaItemForm'},
#       {'name': 'Meeting Track', 'action': 'manage_addTrackForm'},
#       {'name': 'Meeting Break', 'action': 'manage_addbreakItemForm'}
        ]
        additional_meta_types = ['DTML Method', 'DTML Document', 'Page Template',
                                'Image', 'File', 'Meeting Location', 'Message Board']

        for x in Products.meta_types:
            if x['name'] in additional_meta_types:
                y.append(x)

        return y

    def manage_addObject(self):
        """Add a new object to the Meeting"""
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
                                 message = 'The Meeting %s was successfully created!' % id,
                                 action = 'manage_main?update_menu=1',)

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

#   security.declareProtected('View', 'agenda')
#   agenda= DTMLFile('www/MeetingAgenda', globals()) # the agenda

    security.declareProtected('Use mailhost services','SendEmail_form')
    SendEmail_form=DTMLFile('www/SendEmail_form', globals())

#   security.declareProtected('View', 'tracks')
#   tracks= DTMLFile('www/MeetingTracks', globals()) # the tracks

#   speakerlist = DTMLFile('www/MeetingSpeakers', globals())

#   security.declareProtected('View', 'daybyday')
#   daybyday = DTMLFile('www/MeetingDayByDay', globals())

    security.declarePublic('signup_add')
    signup_add=DTMLFile('www/authenticated_add', globals())

    security.declarePublic('attendeelist')
    attendeelist=DTMLFile('www/MeetingAttendees', globals())

    security.declarePublic('choose_bar')
    choose_bar=DTMLFile('www/chooseBar', globals())

    security.declareProtected('Register for Meetings', 'signup')
    signup=DTMLFile('www/MeetingSignUp', globals())

    security.declareProtected('Register for Meetings', 'typeofsignup')
    typeofsignup=DTMLFile('www/typeofsignup', globals())

    # Method to call if someone is logged in and wants to register himself
    security.declareProtected('Authenticated Registration', 'authenticatedsignup')
    authenticatedsignup=DTMLFile('www/authenticatedsignup', globals())

    security.declarePublic('registration')
    registration=DTMLFile('www/Registration', globals())

    def manage_addAnonAttendeeAction(self, sn, givenname, organisation, mail,
            tel, postaladdress, attending, REQUEST=None):
        "Create an attendee, by calling the constructor"
        if not sn:
            return self.signup(setFormError(REQUEST, 'sn', 'Please enter your surname!'))
        if not givenname:
            return self.signup(setFormError(REQUEST, 'givenname', 'Please enter your givenname!'))
        if not mail:
            return self.signup(setFormError(REQUEST, 'mail', 'Please enter your email address!'))
        if mail and not isEmailValid(mail):
            return self.signup(setFormError(REQUEST, 'mail', 'Your email address is invalid!'))

        mail = str(mail)
        pat = re.compile(r'([a-zA-Z][\w-]*@[\w-]+(?:\.[\w-]+)*)')
        if pat.search(mail) is None:
            return MessageDialog(
                title = 'Bad email address',
                message = "Your registration couldn't succeed due to invalid email address",
                action = 'signup',
                )
        id = self.parseEmail(mail)
        passwd = genRandomId()

        if self.checkID(id):
           return self.signup(setFormError(REQUEST, 'mail', 'This email account was already used to make a reservation!'))

        self.manage_addProduct['ManagedMeetings'].manage_addAttendee(
                id , sn, givenname, organisation, mail,
                tel, postaladdress, attending, passwd, '', 'Attendee', 0, 1, '', REQUEST)

        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('registration')

    security.declareProtected('Authenticated Registration',
            'manage_addAttendeeAction')

    def manage_addAttendeeAction(self, sn, givenname, organisation, mail,
            tel, postaladdress, attending, passwd, role, ldap_id, REQUEST=None):
        "Create an attendee, by calling the constructor"

        id = self.parseEmail(mail)
        passwd = genRandomId()

        if self.checkID(id):
            return self.authenticatedsignup(setFormError(REQUEST, 'mail', 'This email account was already used to make a reservation!'))

        self.manage_addProduct['ManagedMeetings'].manage_addAttendee(
                id , sn, givenname, organisation, mail,
                tel, postaladdress, attending, passwd, '', role, 1, 1, ldap_id, REQUEST)
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('registration')

    security.declarePrivate('saveIntoMaillingList')
    def saveIntoMaillingList(self,title,text,author,email,notify,date):
        """ Save the message into the MaillingList,
            if the MessageBoard product is installed """
        from time import time
        if hasattr(self,'MaillingList'):
            obj=getattr(self,'MaillingList')
            id = str(int(time()))
            ob=Message.Message(id, title, text, author, email, notify , date)
            ob.id = id
            obj._setObject(id, ob)

    security.declareProtected('Use mailhost services', 'send_email')
    def send_email(self, subject, comments='', email='', notify=0, date='', attached=[], REQUEST=None,RESPONSE=None):
        """ Sends an email """

        if not subject:
            return self.SendEmail_form(setFormError(REQUEST, 'subject', 'Please enter a subject!'))
        if not comments:
            return self.SendEmail_form(setFormError(REQUEST, 'comments', 'Empty email is not allowed!'))
        if not email:
            return self.SendEmail_form(setFormError(REQUEST, 'email', 'Please enter your email address!'))
        if email and not isEmailValid(email):
            return self.SendEmail_form(setFormError(REQUEST, 'email', 'Your email address is invalid!'))

        userid = REQUEST.AUTHENTICATED_USER.getUserName()

        if MBinstalled and REQUEST.has_key('saveMessage'):
            self.saveIntoMaillingList(subject, comments, userid, email, notify, date)

        reciplist = []
        for t in self.objectValues('Meeting Attendee'):
            if t.mail != '':
                reciplist.append('<' + t.mail + '>')
        recipients = string.join(reciplist,',\n  ') #Unused

        sendermail = 'MeetingManager@' + REQUEST['SERVER_NAME']
        if hasattr(self, 'organiser_email'):
            if getattr(self, 'organiser_email') != '':
                organiser_email = self.organiser_email
        fromaddr = userid + ' <' + email + '>'

        self._send_email(comments, subject, attached, fromaddr, reciplist, sendermail)

        if REQUEST.has_key('destinationURL'):
            return RESPONSE.redirect(REQUEST['destinationURL'])

        if REQUEST is not None:
            return MessageDialog(
                title = 'Mailed',
                message = "The mail %s has been sent!" % self.id,
                action = './manage_main',
                )

    def _send_email(self, comments, subject, attached, fromaddr, reciplist, sender):
        """ """
        import smtplib
        message = self.createhtmlmail( comments, subject, attached, fromaddr, reciplist, sender)

        mailhost=self.unrestrictedTraverse(self.superValues('Mail Host')[0].id)
        host=mailhost.smtp_host
        port=int(mailhost.smtp_port)
        server = smtplib.SMTP(host, port)
        server.sendmail(fromaddr, reciplist, message)
        server.quit()

    security.declarePrivate('createhtmlmail')
    def createhtmlmail (self, text, subject, filein, fromaddr, eto, sender):
        """Create a mime-message that will render HTML in popular
        MUAs, text in better ones"""
        import MimeWriter
        import mimetools
        import cStringIO
        from types import StringType

        out = cStringIO.StringIO() # output buffer for our message
        txtin = cStringIO.StringIO(text)
        if hasattr(self, 'mail_enconding') and self.mail_enconding:
            encoding = self.mail_enconding
        else:
            encoding = 'iso-8859-1'
        writer = MimeWriter.MimeWriter(out)
        #
        # set up some basic headers... we put subject here
        # because smtplib.sendmail expects it to be in the
        # message body
        #
        writer.addheader("From", fromaddr)
        if type(eto) is StringType:
            writer.addheader("To", eto)
        else:
            writer.addheader("To", string.join(eto,','))
        writer.addheader("Subject", subject)
        if sender != fromaddr:
            writer.addheader("Sender", sender)
        writer.addheader("Date", strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        writer.addheader("MIME-Version", "1.0")
        #
        # start the multipart section of the message
        # multipart/alternative seems to work better
        # on some MUAs than multipart/mixed
        #
        writer.startmultipartbody("mixed")
        writer.flushheaders()
        #
        # the plain text section
        #
        subpart = writer.nextpart()
        subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
        pout = subpart.startbody("text/plain", [("charset", encoding)])
        mimetools.encode(txtin, pout, 'quoted-printable')
        txtin.close()
        #
        # start the attach subpart of the message
        #
        #context = self.getContext()
        #meetingfolder = context[id]

        for t in self.objectValues(['File', 'DTML Document', 'ExtFile', 'URL Reference',]):
            if (filein.count(t.getId())):
                fil = cStringIO.StringIO(str(t))
                subpart = writer.nextpart()
                subpart.addheader("Content-Transfer-Encoding", 'base64')
                #
                # returns us a file-ish object we can write to
                #
                if hasattr(t, 'content_type'):
                    pout = subpart.startbody(t.content_type, [('name', t.getId())])
                else:
                    pout = subpart.startbody("application/octet-stream", [('name', t.getId())])
                mimetools.encode(fil, pout, 'base64')
                fil.close()
        #
        # Now that we're done, close our writer and
        # return the message body
        #
        writer.lastpart()
        msg = out.getvalue()
        out.close()
        return msg

    security.declareProtected('View', 'locationtitle')
    def locationtitle(self,REQUEST=None):
        """Show location with URL"""
        if self.location != '':
            locobj = self.aq_acquire(self.location)
            return locobj.title
        else:
            return self.txtlocation

    security.declareProtected('View', 'showlocation')
    def showlocation(self,REQUEST=None):
        """Show location with URL"""
        if self.location != '':
            locobj = self.aq_acquire(self.location)
            return '<a href="%s">%s</a>' % \
             ( locobj.absolute_url(), locobj.title )
        else:
            return self.txtlocation


    security.declarePublic('getAttendeeSeat')
    def getAttendeeSeat(self):
        """ get the list of Attendees with seat """
        def cmp(x, y):
            rez=x.subscription-y.subscription
            if (rez<0):
                return -1
            elif (rez==0):
                return 0
            return 1
        newlist=[]
        list=self.objectValues('Meeting Attendee')
        list.sort(cmp)
        for item in list:
            if item.attending=="CONFIRMED" \
             and ( len(newlist) < self.max_attendees or self.max_attendees == 0 ) \
             and item.role=="Attendee":
                newlist.append(item)
        return newlist

    security.declarePrivate('getAttendeeStand')
    def getAttendeeStand(self):
        """ get the list of Attendees without seat """
        def cmp(x, y):
            rez=x.subscription-y.subscription
            if (rez<0):
                return -1
            elif (rez==0):
                return 0
            return 1
        newlist=[]
        list=self.objectValues('Meeting Attendee')
        list.sort(cmp)
        cnt=0
        for item in list:
            if item.attending=="CONFIRMED" \
             and ( cnt < self.max_attendees or self.max_attendees == 0 ) \
             and item.role=="Attendee":
                cnt=cnt+1
            elif item.role=="Attendee":
                newlist.append(item)
        return newlist

    security.declarePublic('getVIP')
    def getVIP(self):
        """ get the list of Speakers, Chairmans and Organigers """
        newlist=[]
        for item in self.objectValues('Meeting Attendee'):
            if item.role!="Attendee":
                newlist.append(item)
        return newlist

    def parseEmail(self, mail):
        """ """
        return string.replace(mail.lower(), '@', '_')

    security.declarePrivate('ifAttendee')
    def ifAttendee(self,userid):
        """ check if attendee exists"""
        for user in self.objectValues('Meeting Attendee'):
            if userid == user.id:
                return user
        return None

    security.declarePublic('loginUser')
    def loginUser(self,REQUEST=None):
        """ login an user """
        if REQUEST is not None:
            email = REQUEST.get('email', None)
            password = REQUEST.get('passwd', None)
            if email and password:
                attendee = self.ifAttendee(self.parseEmail(email))
                redirect_string = REQUEST.HTTP_REFERER
                if attendee is not None:
                    if password == attendee.getAttendeePassword():
                        #REQUEST.SESSION.delete('error')
                        REQUEST.SESSION.set('userkey',self.parseEmail(email))
                    else:
                        REQUEST.SESSION.set('error',1)
                else:
                    REQUEST.SESSION.set('error',1)
                REQUEST.RESPONSE.redirect(redirect_string)

    security.declarePublic('mailPassword')
    def mailPassword(self, email, REQUEST=None, RESPONSE=None):
        """ Mail the password to subscriber"""
        userid=self.parseEmail(email)
        if self.ifAttendee(userid) is not None:
            eTo=email
            eFrom='registration@eionet.europa.eu'
            eSubject= 'password reminder'
            passwd = self[userid].getAttendeePassword()
            eContent="YOUR PASSWORD IS:  " + passwd + "\n\n\r" + \
                "If you want to change your options go to the following link " + \
                self.absolute_url() + "/attendeelist, click on your name and press `Edit`" + \
                " to modify your profile using the password: " + passwd
            self._send_email(eContent, eSubject, '', eFrom, eTo, eFrom)
            if REQUEST is not None:
                return MessageDialog(title = 'Mailed', message = "An email has been sent to %s " % email, action = REQUEST.HTTP_REFERER,)

        else:
            if REQUEST is not None:
                return MessageDialog(title = 'Mailed', message = "An user with this email is not registered!", action = REQUEST.HTTP_REFERER,)

    security.declarePublic('getAbsoluteURL')
    def getAbsoluteURL(self):
        """ return the absolute_url of the meeting """
        return self.absolute_url(0)

    def checkID(self, p_id):
        """ check if this attendee already exist """
        try:
            ob = self._getOb(p_id)
            return 1
        except:
            return 0

    def antispam(self, address):
        """ All email adresses will be obfuscated. """
        a = address.replace('@','<span style="display:none">%deletethis%</span>@')
        return a

#   def antispam(self, address):
#       """ All email adresses will be obfuscated. """
#       from whrandom import choice
#       buffer = map(None, address)
#       for i in range(0, len(address), choice((2,3,4))):
#           buffer[i] = '&#%d;' % ord(buffer[i])

#       return string.join(buffer,'')
    #######################
    # LDAP registration   #
    #######################

    security.declareProtected('loginLDAP', 'loginLDAP')
    def loginLDAP(self,REQUEST=None):
        """ login an LDAP user """
        username = REQUEST.get('username', None)
        REQUEST.SESSION.set('userkey', username)
        redirect_string = REQUEST.HTTP_REFERER
        REQUEST.RESPONSE.redirect(redirect_string)

    ################################
    # Init method                  #
    ################################

    def __setstate__(self,state):
        Meeting.inheritedAttribute("__setstate__") (self, state)
        if not hasattr(self, "allow_anonymous"): # backwards compatibility
            self.allow_anonymous = 1
        if not hasattr(self, "txtlocation"): # backwards compatibility
            self.txtlocation = ""
        if not hasattr(self, "agenda_url"): # backwards compatibility
            self.agenda_url = ""
        if not hasattr(self, "minutes_url"): # backwards compatibility
            self.minutes_url = ""
        if not hasattr(self, "generation"): # backwards compatibility
            self.generation = 0
        if not hasattr(self, "status"): # backwards compatibility
            if self.active:
                self.status = 'active'
            else:
                self.status = 'inactive'

    ################################
    # Management Interface         #
    ################################

    security.declareProtected('Change Meetings', 'manage_propertiesForm')
    manage_propertiesForm= DTMLFile('www/MeetingEdit', globals())

    security.declareProtected('Change Meetings', 'manage_editMeeting')
    def manage_editMeeting(self, title='', event_type='', location='',
            txtlocation='',
            description='', startdate='', enddate='',
            agenda_url='',minutes_url='',
            organiser='', organiser_email='', max_attendees=0,
            allow_registrations=0, allow_anonymous=0, status='', REQUEST=None):
        """ Change the edited values """
        self.title = title
        self.event_type = event_type
        self.location = location
        if location:
            self.txtlocation = ''
        else:
            self.txtlocation = txtlocation
        self.description = description
        self.startdate = startdate
        self.enddate = enddate
        self.agenda_url = agenda_url
        self.minutes_url = minutes_url
        self.organiser = organiser
        self.organiser_email = organiser_email
        self.max_attendees = max_attendees
        if allow_registrations:
            self.allow_registrations = 1
        else:
            self.allow_registrations = 0
        self.allow_anonymous = allow_anonymous
        self.status = status
        self.generation = self.generation + 1
        # update ZCatalog
        # self.reindex_object()
        if REQUEST:
            message="Saved changes."
            return self.manage_propertiesForm(self,REQUEST,manage_tabs_message=message)

InitializeClass(Meeting)
