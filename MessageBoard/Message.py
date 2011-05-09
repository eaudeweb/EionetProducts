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
# The Original Code is MessageBoard version 1.0.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Cornel Nitu, Rares Vernica Finsiel Romania
#

import smtplib
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder
from OFS.PropertyManager import PropertyManager
from Globals import InitializeClass
from Products.ZCatalog.CatalogAwareness import CatalogAware
import Products

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.MessageBoard.Utils import *

manage_addMessageForm = PageTemplateFile('zpt/Message_addForm', globals())
def manage_addMessage(self, title='', text='', attachment='', author='', email='', 
        notify=0, date='', REQUEST=None, RESPONSE=None):
    """Add a new Message object"""

    id = str(generateId())
 #   if self.meta_type != 'Message':
    if not title:
        return getattr(self,REQUEST['form_name'])(setFormError(REQUEST, 'title', 'Please enter a subject!'))
    if not text:
        return getattr(self,REQUEST['form_name'])(setFormError(REQUEST, 'text', 'Please enter the message!'))
    if not author:
        return getattr(self,REQUEST['form_name'])(setFormError(REQUEST, 'author', 'Please enter your name!'))
    if not email:
        return getattr(self,REQUEST['form_name'])(setFormError(REQUEST, 'email', 'Please enter your email address!'))
    if email and not isEmailValid(email):
        return getattr(self,REQUEST['form_name'])(setFormError(REQUEST, 'email', 'Your email address is invalid!'))

    if attachment.filename and len(attachment.read(self.filesize + 1)) > self.filesize:
        return getattr(self,REQUEST['form_name'])(setFormError(REQUEST, 'file', 'Your file is larger than %s bytes!' % self.filesize))

    ob=Message(id, title, text, author, email, notify, date)
    ob.id = id

    self._setObject(id, ob)

    if attachment.filename:
        ob.manage_addFile(id='', file=attachment, title='')

    obj = self._getOb(id)
    old = self.aq_parent
    if hasattr(old,'notify') and old.notify:
        topic = self.getTopic()
        msg_url = "%s/tree_html?msg=%s&expand=0&selectedmsg=%s#Msg%s" % (self.getMBPath(), topic.id, id, id)
        content = """ A reply to your original message has been posted at %s """ % msg_url
        self.sendEmail(content, '%s <%s>' % (old.author, old.email), '%s <%s>' % (author, email), 'Re:%s' % old.getSubject())

    if REQUEST.has_key('destinationURL'):
        return RESPONSE.redirect(REQUEST['destinationURL'])

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)


addMessageForm = PageTemplateFile('zpt/MessageBoard_add_message', globals())
def addMessage(self, title='', text='', attachment='', author='', email='', notify=0, REQUEST=None):
    """add message (Front)"""
    id = str(generateId())
    if self.meta_type != 'Message':
        if not title:
            return getattr(self, 'addMessageForm')(setFormError(REQUEST, 'title', 'Please enter a subject!'))
    if not text:
        return getattr(self, 'addMessageForm')(setFormError(REQUEST, 'text', 'Please enter the message!'))
    if not author:
        return getattr(self, 'addMessageForm')(setFormError(REQUEST, 'author', 'Please enter your name!'))
    if not email:
        return getattr(self, 'addMessageForm')(setFormError(REQUEST, 'email', 'Please enter your email address!'))
    if email and not isEmailValid(email):
        return getattr(self, 'addMessageForm')(setFormError(REQUEST, 'email', 'Your email address is invalid!'))

    if attachment.filename and len(attachment.read(self.filesize + 1)) > self.filesize:
        return getattr(self, 'addMessageForm')(setFormError(REQUEST, 'file', 'Your file is larger than %s bytes!' % self.filesize))

    ob=Message(id, title, text, author, email, notify, getToday())
    ob.id = id
    self._setObject(id, ob)

    if attachment.filename:
        ob.manage_addFile(id='', file=attachment, title='')

    obj = self._getOb(id)
    old = self.aq_parent

    if hasattr(old,'notify') and old.notify:
        topic = self.getTopic()
        msg_url = "%s/tree_html?msg=%s&expand=0&selectedmsg=%s#Msg%s" % (self.getMBPath(), topic.id, id, id)
        content = """ A reply to your original message has been posted at %s """ % msg_url
        self.sendEmail(content, '%s <%s>' % (old.author, old.email), '%s <%s>' % (author, email), 'Re:%s' % old.getSubject())
    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(self.getMPAbsolutePath() + '/index_html')


class Message(CatalogAware, Folder, PropertyManager):
    """The Message class """

    meta_type       = "Message"
    product_name    = "MessageBoard"

    manage_options = (Folder.manage_options[0],) + (
                    PropertyManager.manage_options + (
                    {'label' : 'View',              'action' : 'index_html'},
                    {'label' : 'Reply',             'action' : 'reply_Message'},))

    _properties=(
            {'id':'title',          'type':'ustring',        'mode':'w'},
            {'id':'text',           'type':'utext',          'mode':'w'},
            {'id':'author',         'type':'ustring',        'mode':'w'},
            {'id':'email',          'type':'string',        'mode':'w'},
            {'id':'notify',         'type':'boolean',       'mode':'w'},
            {'id':'date',           'type':'date',          'mode':'w'},
    )

    security = ClassSecurityInfo()
    security.setPermissionDefault('Send direct email', ('Anonymous','Manager'))

    def __init__(self, id, title, text, author, email, notify, date):
        """ initialize a new instance of Message"""
        self.id = id
        self.title =title
        self.text = text
        self.author = author
        self.email = email
        self.notify = notify
        self.date = date

    security.declareProtected('View management screens', 'all_meta_types')
    def all_meta_types(self):
        """return a filtered list of meta types"""
        f = lambda x: x['name'] in ('File','Image', 'Message')
        return filter(f, Products.meta_types)

    security.declarePublic('getBody')
    def getBody(self):
        """ return the message content """
        return extract_urls(self.text)

    security.declareProtected('Send direct email', 'sendEmailMessageCopy')
    def sendEmailMessageCopy(self, email='', REQUEST=None, RESPONSE=None):
        """Send a copy of current message to a given email address"""
        if not email:
            return getattr(self, 'emailMessageCopy')(setFormError(REQUEST, 'email', 'Please enter user\'s email address!'))
        if email and not isEmailValid(email):
            return getattr(self, 'emailMessageCopy')(setFormError(REQUEST, 'email', 'User\'s email address is invalid!'))
        email_text = self.text + '\n\r'
        for attach in self.objectValues('File'):
            email_text = email_text + '\n\rDownload attachment: ' + str(attach.absolute_url(0))
        self.sendEmail(email_text, self.author + ' <' + email + '>', self.author + ' <' + self.email + '>', 'Copy of message "' + self.title + '"')
        if REQUEST.has_key('destinationURL'):
            return RESPONSE.redirect(REQUEST['destinationURL'])
        return RESPONSE.redirect(self.getMPAbsolutePath() + '/index_html')

    security.declareProtected('Send direct email', 'sendEmailMessageAuthor')
    def sendEmailMessageAuthor(self, email='', content='', REQUEST=None, RESPONSE=None):
        """Send an email to current message's author"""
        if not email:
            return getattr(self, 'emailMessageAuthor')(setFormError(REQUEST, 'email', 'Please enter an email address!'))
        if email and not isEmailValid(email):
            return getattr(self, 'emailMessageAuthor')(setFormError(REQUEST, 'email', 'Please enter a valid email address!'))
        if not content:
            return getattr(self, 'emailMessageAuthor')(setFormError(REQUEST, 'content', 'Please enter some comments!'))
        self.sendEmail(content, self.author + ' <' + self.email + '>', '<' + email + '>', 'Comments for message "' + self.title + '"')
        if REQUEST.has_key('destinationURL'):
            return RESPONSE.redirect(REQUEST['destinationURL'])
        return RESPONSE.redirect(self.getMPAbsolutePath() + '/index_html')

    security.declarePrivate('sendEmail')
    def sendEmail(self, eContent, eTo, eFrom, eSubject):
        """Sends an email (works with 'notify')"""
        if isUnicode(eContent):
            eContent = eContent.encode('utf-8')
        if isUnicode(eTo):
            eTo = eTo.encode('utf-8')
        if isUnicode(eSubject):
            eSubject = eSubject.encode('utf-8')
        if isUnicode(eFrom):
            eFrom = eFrom.encode('utf-8')
        message = createEmail(eContent, eTo, eFrom, eSubject)
        mailhost=self.unrestrictedTraverse(self.superValues('Message Board')[0].mailhost)
        #print mailhost.id
        host=mailhost.smtp_host
        port=int(mailhost.smtp_port)
        server = smtplib.SMTP(host, port)
        server.sendmail(eFrom, eTo, message)
        server.quit()
        return 1

    security.declarePublic('count_children')
    def count_children(self):
        x = self.objectItems(['Message'])
        sum = len(x)
        for child_name, child in x:
            sum = sum + child.count_children()
        return sum

    security.declarePublic('getTopic')
    def getTopic(self):
        """ return topic message  """
        parent = self
        while parent.getParentNode().meta_type != 'Message Board':
            parent = parent.getParentNode()
        return parent

    security.declarePublic('getSubject')
    def getSubject(self):
        topic = self.getTopic()
        return topic.title

    security.declarePublic('index_html')
    index_html    = PageTemplateFile("zpt/viewMessage", globals())

    security.declareProtected('Add Message', 'reply_Message')
    reply_Message = PageTemplateFile("zpt/replyMessage", globals())

    security.declareProtected('Add Message','manage_addMessageForm')
    manage_addMessageForm = manage_addMessageForm

    security.declareProtected('Send direct email', 'emailMessageCopy')
    emailMessageCopy = PageTemplateFile("zpt/emailMessageCopy", globals())

    security.declareProtected('Send direct email', 'emailMessageAuthor')
    emailMessageAuthor = PageTemplateFile('zpt/emailMessageAuthor', globals())

InitializeClass(Message)

