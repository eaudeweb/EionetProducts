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

from App.ImageFile import ImageFile

import EionetLDAP

def initialize(context):
    # register EionetLDAP
    context.registerClass(
        EionetLDAP.EionetLDAP,
        constructors=(EionetLDAP.manage_addEionetLDAP_html,
                       EionetLDAP.manage_addEionetLDAP),
        icon='www/eionet_ldap.gif',
    )

misc_ = {
    'eionet_ldap.gif': ImageFile('www/eionet_ldap.gif', globals()),
}
