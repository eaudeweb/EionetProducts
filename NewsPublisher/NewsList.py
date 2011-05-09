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

# Zope imports
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.ZCatalog.ZCatalog import manage_addZCatalog

def _add_indexes(self):
    app = self.restrictedTraverse('/')

    if not hasattr(app, 'Catalog'):
        manage_addZCatalog(app, 'Catalog', 'Catalog')

    if 'meta_type' not in app.Catalog.indexes():
        app.Catalog.addIndex('meta_type', 'FieldIndex', 'meta_type')

    if 'published' not in app.Catalog.indexes():
        app.Catalog.addIndex('published', 'FieldIndex', 'published')

    if 'release_date' not in app.Catalog.indexes():
        app.Catalog.addIndex('release_date', 'FieldIndex', 'release_date')

manage_addNewsList_html = PageTemplateFile('zpt/list_add', globals())
def manage_addNewsList(self, id, title='', items_in_list=5, items_in_feed=15, REQUEST=None):
    """ Adds a new News List object """
    ob = NewsList(id, title, items_in_list, items_in_feed)
    self._setObject(id, ob)
    th = self._getOb(id)
    _add_indexes(th)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class NewsList(SimpleItem):
    """ News List """

    meta_type = 'News List'
    product_name = 'News List'
    manage_options = (
        {'label':'Edit', 'action':'manage_propertiesForm'},
        {'label':'View', 'action':'index_html'},
        {'label':'Feed', 'action':'feed_atom'},
    ) + SimpleItem.manage_options

    security = ClassSecurityInfo()

    def __init__(self, id, title, items_in_list, items_in_feed):
        """ constructor """

        self.id = id
        self.title = title
        self.items_in_list = int(items_in_list)
        self.items_in_feed = int(items_in_feed)

    security.declareProtected('View management screens', 'manageProperties')
    def manageProperties(self, title, items_in_list, items_in_feed, REQUEST=None, RESPONSE=None):
        """ manage basic properties """
        self.title = title
        self.items_in_list = int(items_in_list)
        self.items_in_feed = int(items_in_feed)

        self._p_changed = 1

        if REQUEST is not None:
            # self.setSessionInfo("News Item modified successfully")
            return RESPONSE.redirect('manage_propertiesForm')

    security.declareProtected('View management screens', 'manage_propertiesForm')
    manage_propertiesForm = PageTemplateFile('zpt/list_edit', globals())

    security.declarePublic('index_html')
    _index_html = PageTemplateFile('zpt/list_index', globals())
    def index_html(self, REQUEST=None):
        """ List all news items """
        news_items = self.Catalog.search({'meta_type': "News Item", 'published': True},
                sort_index='release_date', reverse=True, limit=self.items_in_list)
        return self._index_html(self, REQUEST, news_items=news_items)

    security.declarePublic('feed_atom')
    _feed_atom = PageTemplateFile('zpt/list_feed_atom', globals())
    def feed_atom(self, REQUEST=None):
        """ List all news items """
        news_items = self.Catalog.search({'meta_type': "News Item", 'published': True},
                sort_index='release_date', reverse=True, limit=self.items_in_feed)
        return self._feed_atom(REQUEST, news_items=news_items)

InitializeClass(NewsList)
