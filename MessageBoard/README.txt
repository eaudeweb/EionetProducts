<h3>Introduction</h3>

The Messageboard product lets you create a board for messages.  People can
post, see and reply to messages or replys to messages. It uses a tree-like
view in order for you to see which reply belongs to which.

<h3>Installation</h3>

This is a Python Product.
Installation is very simple. Download the tgz file. Put it in the
Products directory and do tar xzvf MessageBoard-x-x.tgz. If you
haven't done already, create a MailHost and read the README file in
the product. Restart zope and you will now be able to create objects of
the "MessageBoard" and "Message" type. Beware that it was developed on
Zope 2.5.x and probably doesn't run on Zope versions older than that.

In order to allow anonymous people to post messages on your MessageBoard
you must set, for the MessageBoard, in the Security tab, 'Add Messages',
'Use mailhost services' and 'manage properties' for 'Anonymous' role.

To get an example of the available CSS styling you can call
&lt;link href="/misc_/MessageBoard/MessageBoard.css" rel="stylesheet" type="text/css">
from standard_html_header or from your existing stylesheet.

<h3>License</h3>

The contents of this file are subject to the Mozilla Public
License Version 1.1 (the "License"); you may not use this file
except in compliance with the License. You may obtain a copy of
the License at http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS
IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
implied. See the License for the specific language governing
rights and limitations under the License.

The Original Code is MessageBoard version 1.0.

The Initial Owner of the Original Code is European Environment
Agency (EEA).  Portions created by Finsiel Romania are
Copyright (C) European Environment Agency.  All
Rights Reserved.

