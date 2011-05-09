NewsPublisher
=============

A simple Zope product for publishing news items. Each news item acts as a
container, holding images and file attachments. The product provides a "latest
news" view, along with an atom 1.0 feed. News items can be placed anywhere in
the Zope object hierarchy; they are indexed using a top-level Catalog object.



Installation
------------

The "NewsPublisher" folder must be placed in Zope's Products folder. At
startup, the product will create a top-level Catalog object with three indexes
(meta_type, published, release_date) - only if these don't exist.

Recommended: for proper Unicode support, the root Zope folder should have
a "management_page_charset" property of type "string" with the value "utf-8"
(this can be set from the "Properties" tab in the ZMI).

See MIGRATION.txt for migrating old-style NewsFolder announcements.


Usage
-----

For each news article create "News Item" objects from the ZMI. Create a "News
List" object to generate a listing of the latest news (this listing is not a
standalone HTML document, it's intended to be embedded in another page). The
"News List" object also generates a feed with the latest news items. Note that
only news items with the "Published" attribute are visible in the "latest news"
listing and the feed, regardless of their "Release date" attribute.


Source
------

The source code is maintained on the EEA Subversion repository:
  http://svn.eionet.europa.eu/repositories/Zope/trunk/NewsPublisher
