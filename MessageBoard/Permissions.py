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


from AccessControl import ClassSecurityInfo, getSecurityManager
from Globals import InitializeClass

class Permissions:
    """  Class that implements permissions and rights checking. """

    security = ClassSecurityInfo()

    def checkPermission(self, permission):
        """ Generic function to check a given permission on the current object. """
        return getSecurityManager().checkPermission(permission, self) is not None

    def checkPermissionReply(self):
        """  """
        return self.checkPermission('Add Message')

    def checkPermissionEmail(self):
        """  """
        return self.checkPermission('Send direct email')

    def checkPermissionAdd(self):
        """  """
        return self.checkPermission('Add Message')

    def checkPermissionUpload(self):
        """  """
        return self.checkPermission('Upload attachement')

InitializeClass(Permissions)
