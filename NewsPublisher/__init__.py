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
from App.ImageFile import ImageFile
from Products.ZCatalog.ZCatalog import manage_addZCatalog

# Product imports
import NewsItem
import NewsList
from StaticServe import StaticServeFromZip

def install_catalog(app):
    if not hasattr(app, 'Catalog'):
        manage_addZCatalog(app, 'Catalog', 'Catalog')
    
    if 'meta_type' not in app.Catalog.indexes():
        app.Catalog.addIndex('meta_type', 'FieldIndex', 'meta_type')
    
    if 'published' not in app.Catalog.indexes():
        app.Catalog.addIndex('published', 'FieldIndex', 'published')
    
    if 'release_date' not in app.Catalog.indexes():
        app.Catalog.addIndex('release_date', 'FieldIndex', 'release_date')

def initialize(context):
    # make sure the catalog exists
    install_catalog(context._ProductContext__app)
    
    # register NewsItem
    context.registerClass(
        NewsItem.NewsItem,
        constructors=(NewsItem.manage_addNewsItem_html,
                       NewsItem.manage_addNewsItem),
        icon='www/news_item.gif',
    )
    
    # register NewsList
    context.registerClass(
        NewsList.NewsList,
        constructors=(NewsList.manage_addNewsList_html,
                       NewsList.manage_addNewsList),
        icon='www/news_feed.png',
    )

misc_ = {
    'jquery.js': ImageFile('www/jquery-1.2.6.min.js', globals()),
    'jquery_calendar.js': ImageFile('www/jquery.datePicker.js', globals()),
    'date.js': ImageFile('www/date.js', globals()),
    'jquery_calendar.css': ImageFile('www/datePicker.css', globals()),
    'tinymce': StaticServeFromZip('tinymce', 'www/tinymce_3_2_0_2.zip', globals()),
    'news_item_manage.css': ImageFile('www/news_item_manage.css', globals()),
}
