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
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Authors:
#
# Alex Ghica, Finsiel Romania
# Cornel Nitu, Finsiel Romania
#
#$Id: __init__.py 11250 2008-05-06 10:02:03Z roug $

__version__='$Revision: 1.11 $'[11:-2]

from App.ImageFile import ImageFile

import GimmeThesaurus

def initialize(context):
    """ Gimme Thesaurus """

    # Gimme Thesaurus
    context.registerClass(
        GimmeThesaurus.Thesaurus,
        constructors=(GimmeThesaurus.manage_addThesaurus_html,
                       GimmeThesaurus.manage_addThesaurus),
        icon='www/thesaurus.gif',
        )

misc_ = {
    #layout images
    'thesaurus.gif':ImageFile('www/thesaurus.gif', globals()),
    'search.gif':ImageFile('www/search.gif', globals()),
    'background.gif':ImageFile('www/background.gif', globals()),
    'help.gif':ImageFile('www/help.gif', globals()),
    'forward.gif':ImageFile('www/forward.gif', globals()),
    'back.gif':ImageFile('www/back.gif', globals()),
    'branch.gif':ImageFile('www/branch.gif', globals()),
    'categ.gif':ImageFile('www/categ.gif', globals()),
    'leaf_top.gif':ImageFile('www/leaf_top.gif', globals()),
    'leaf_mid.gif':ImageFile('www/leaf_mid.gif', globals()),
    'leaf_end.gif':ImageFile('www/leaf_end.gif', globals()),
    'leaf_only.gif':ImageFile('www/leaf_only.gif', globals()),
    'back_horizontal.gif':ImageFile('www/back_horizontal.gif', globals()),
    'minus.gif':ImageFile('www/minus.gif', globals()),
    'plus.gif':ImageFile('www/plus.gif', globals()),
    'square.gif':ImageFile('www/square.gif', globals()),
    'back_to_top.gif':ImageFile('www/back_to_top.gif', globals()),
    'err.gif':ImageFile('www/err.gif', globals()),
    'done.gif':ImageFile('www/done.gif', globals()),
    }
