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
# Cornel Nitu, Rares Vernica, Finsiel Romania
# Soren Roug, European Environment Agency

from os.path import join

from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.Folder import Folder
from OFS.PropertyManager import PropertyManager
from Globals import InitializeClass, package_home
import Products

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.ZopePageTemplate import manage_addPageTemplate

from Message import manage_addMessageForm, manage_addMessage, addMessageForm, addMessage
from Products.MessageBoard.Permissions import Permissions

manage_addMessageBoardForm = PageTemplateFile('zpt/MessageBoard_addForm', globals())

def manage_addMessageBoard(self, id, title='',description='',
        filesize=500000, mailhost='', integrated=0, REQUEST=None):
    """ Add a new Meeting object """
    ob=MessageBoard(id, title, description, filesize, mailhost, integrated)
    self._setObject(id, ob)
    object=self._getOb(id)

    indexfile = open(join(package_home(globals()),'zpt','MessageBoardIndex.zpt'))
    content = indexfile.read()
    indexfile.close()
    manage_addPageTemplate(object, id='index_html', title='Default View', text=content)

    indexfile = open(join(package_home(globals()),'zpt','MessageTreeIndex.zpt'))
    content = indexfile.read()
    indexfile.close()
    manage_addPageTemplate(object, id='tree_html', title='Default View', text=content)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)


def getMailHostList(self):
    """ List of mail hosts """
    try:
        list=self.superValues('Mail Host')
        newlist=[]
        for item in list:
            newlist.append(item.absolute_url(relative=1))
        return newlist
    except:
        return []

class MessageBoard(Folder, PropertyManager, Permissions):
    """ The Message class """

    meta_type       = "Message Board"
    product_name    = "MessageBoard"

    _properties=(
            {'id':'title',      'type':'ustring',    'mode':'w'},
            {'id':'description','type':'utext',      'mode':'w'},
            {'id':'mailhost', 'type':'selection', 'mode':'w', 'select_variable':'getMailHostList'},
            {'id':'filesize', 'type':'int', 'mode':'w'},
            {'id':'integrated', 'type':'int', 'mode':'w'},
    )

    manage_options = (Folder.manage_options[0],) + (
            PropertyManager.manage_options + (
            {'label' : 'View',              'action' : 'index_html'},
            {'label' : 'Undo',              'action' : 'manage_undoForm'},
            ) +
            SimpleItem.manage_options )


    security = ClassSecurityInfo()

#    def __str__(self): return self.index_html()
#    def __len__(self): return 1

    def __init__(self, id, title, description, filesize, mailhost, integrated):
        """ initialize the message board """
        self.id = id
        self.title =title
        self.description = description
        self.filesize = filesize
        self.mailhost = mailhost
        self.integrated = integrated

    def __setstate__(self, state):
        """update"""
        MessageBoard.inheritedAttribute('__setstate__')(self, state)
        if not hasattr(self, 'filesize'):
            self.filesize = 500000

    security.declareProtected('View management screens', 'all_meta_types')
    def all_meta_types(self):
        """return a filtered list of meta types"""

        f = lambda x: x['name'] in ('Message','DTML Method',
            'Page Template','DTML Document')
        return filter(f, Products.meta_types)

    getMailHostList=getMailHostList

    security.declareProtected('Add Message','manage_addMessageForm')
    manage_addMessageForm=manage_addMessageForm
    manage_addMessage=manage_addMessage

    security.declareProtected('Add Message','addMessageForm')
    addMessageForm=addMessageForm
    addMessage=addMessage

    security.declarePublic('messageTree')
    def messageTree(self, folder, x='0'):
        """ returns the tree of messages """
        tree = []
        copii = folder.objectValues('Message')
        for i in range(0, len(copii)):
            buf = x
            if i == 0:
                if i < len(copii)-1:
                    tree.append(('%s2' % buf, copii[i]))
                    buf = '%s3' % buf
                else:
                    tree.append(('%s1' % buf, copii[i]))
                    buf = '%s0' % buf
            elif i == len(copii)-1:
                tree.append(('%s1' % buf, copii[i]))
                buf = '%s0' % buf
            else:
                tree.append(('%s2' % buf, copii[i]))
                buf = '%s3' % buf
            tree.extend(self.messageTree(copii[i], buf))
        return tree

    security.declarePublic('showFullDateTime')
    def showFullDateTime(self, date):
        """date is a DateTime object. This function returns a string 'dd month_name yyyy hh:mm:ss'"""
        try: return date.strftime('%d %b %Y %H:%M')
        except: return ''

    security.declarePublic('getMPAbsolutePath')
    def getMPAbsolutePath(self):
        """Returns object's absolute path"""
        return self.absolute_url(0)

    security.declarePublic('getMBPath') #???
    def getMBPath(self):
        return self.absolute_url()

    security.declarePublic('get_message')
    def get_message(self, id):
        return getattr(self, id)

    security.declareProtected('View', 'mesgboard_css')
    mesgboard_css = PageTemplateFile('zpt/style', globals())

InitializeClass(MessageBoard)
