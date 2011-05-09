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
#$Id: ErrorCodes.py 5926 2006-02-21 13:56:10Z roug $

__version__='$Revision: 1.2 $'[11:-2]


MSG_DB_CONECTED = "Succesful database connection"
MSG_PROPERTIES_SAVED = "General properties saved"

DATABASE_ERROR = """
An error was encountered while publishing this resource.

Troubleshooting Suggestions
The URL may be incorrect.
The parameters passed to this resource may be incorrect. 
A resource that this resource relies on may be encountering an error.

If the error persists please contact the administrator. Thank you for your patience."""
