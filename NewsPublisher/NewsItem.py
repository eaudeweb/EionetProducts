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
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Eau de Web are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Authors:
#
# Alex Morega, Eau de Web

__version__='0.1'

# Python imports
from datetime import date, time, datetime

# Zope imports
from AccessControl import ClassSecurityInfo
from App.ImageFile import ImageFile
from OFS.Folder import Folder
from OFS.Application import Application
from Products.ZCatalog.CatalogAwareness import CatalogAware
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from DateTime import DateTime
import Products


def make_slug(string):
    import re
    if isinstance(string, unicode):
        string = string.encode('utf-8')
    return re.sub(r'[^\w\d]', '_', re.sub(r'[^\w\d\s]', '', string.lower()))

def make_date(raw):
    if isinstance(raw, basestring):
        y, m, d = raw.split('-')
        return date(int(y), int(m), int(d))
    else:
        return raw

def make_rfc3339_date(t):
    if isinstance(t, date):
        t = datetime.combine(t, time(0))
    elif isinstance(t, DateTime):
        t = datetime(t._year, t._month, t._day, t._hour, t._minute, int(t._second))
    
    if t.tzinfo:
        time_str = t.strftime('%Y-%m-%dT%H:%M:%S')
        offset = t.tzinfo.utcoffset(date)
        timezone = (offset.days * 24 * 60) + (offset.seconds / 60)
        hour, minute = divmod(timezone, 60)
        return time_str + "%+03d:%02d" % (hour, minute)
    else:
        return t.strftime('%Y-%m-%dT%H:%M:%SZ')

manage_addNewsItem_html = PageTemplateFile('zpt/item_add', globals())
def manage_addNewsItem(self, id=None, REQUEST=None, title='', author='', release_date=None, published=False, teaser='', details=''):
    """ Adds a new News Item object """
    if not id:
        if not title:
            raise ValueError('Title is mandatory')
        id = make_slug(title)
    ob = NewsItem(id, title, author, release_date, published, teaser, details)
    self._setObject(id, ob)
    
    th = self._getOb(id)
    
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class NewsItem(CatalogAware, Folder):
    """ News Item """
    
    meta_type = 'News Item'
    product_name = 'News Item'
    manage_options = (
        Folder.manage_options[2], # Properties
        Folder.manage_options[0], # Contents
        Folder.manage_options[1], # View
        Folder.manage_options[3], # Security
        Folder.manage_options[-1], # Find
    )
    
    security = ClassSecurityInfo()
    
    def __init__(self, id, title='', author='', release_date=None, published=False, teaser='', details=''):
        """ constructor """
        if not release_date:
            release_date = date.today()
        
        self.id = id
        self.title = title
        self.author = author
        self.release_date = make_date(release_date)
        self.teaser = teaser
        self.details = details
        self.published = bool(published)
    
    def all_meta_types(self):
        """ What can you put inside me? """
        allowed_types = (
            'File',
            'Image',
        )
        
        local_meta_types = []
        for x in Products.meta_types:
            if x['name'] in allowed_types:
                local_meta_types.append(x)
        
        return local_meta_types
    
    security.declarePublic('rfc3339_release_date')
    def rfc3339_release_date(self):
        return make_rfc3339_date(self.release_date)
    
    security.declarePublic('rfc3339_change_date')
    def rfc3339_change_date(self):
        return make_rfc3339_date(self.bobobase_modification_time())
    
    security.declareProtected('View management screens', 'PrincipiaSearchSource')
    def PrincipiaSearchSource(self):
        """ Return all content """
        return self.title + ' ' + self.author + ' ' + self.teaser + ' ' + self.details
    
    
    security.declareProtected('View management screens', 'manageProperties')
    def manageProperties(self, title, author, release_date, teaser, details, published=False, REQUEST=None, RESPONSE=None):
        """ manage basic properties """
        self.title = title
        self.author = author
        self.release_date = make_date(release_date)
        self.teaser = teaser
        self.details = details
        self.published = bool(published)
        
        self._p_changed = 1
        self.reindex_object()
        
        if REQUEST is not None:
            # self.setSessionInfo("News Item modified successfully")
            return RESPONSE.redirect('manage_propertiesForm')
    
    security.declarePublic('index_html')
    index_html = PageTemplateFile('zpt/item_index', globals())
    
    security.declareProtected('View management screens', 'manage_propertiesForm')
    manage_propertiesForm = PageTemplateFile('zpt/item_edit', globals())
    
    security.declareProtected('View management screens', 'manage_fileList')
    manage_fileList = PageTemplateFile('zpt/item_file_list', globals())

InitializeClass(NewsItem)
