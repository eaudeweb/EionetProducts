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
# The Original Code is ManagedMeetings version 1.0.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by CMG and Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Cornel Nitu, Finsiel Romania
# Rares Vernica, Finsiel Romania

import types
import string, re
from whrandom import choice
from time import strftime

def format_date(date):
    try:
        return date.strftime("%Y/%m/%d %H:%M")
    except:
        return date

def setFormError(req, key, msg):
    req.set('FORM_ERROR', 1)
    req.set('FORM_ERROR_' + key, msg)
    return req

def isEmailValid(email, bad_domains=''):
    if type(bad_domains) == type([]) and len(bad_domains) > 0:
        for dom in bad_domains:
            if re.compile('@'+dom).search(email) is not None:
                return 0

    if re.compile('\s').search(email) is not None:
        return 0

    if re.compile(r'^[_\-\.0-9a-z]+@([\-0-9a-z][\-_0-9a-z\.]+)\.([a-z]{2,4}$)', re.IGNORECASE).search(email) is None:
        return 0

    return 1

def genRandomId(self=None, p_length=6, p_chars=string.digits):
    """Generate a random numeric id."""
    return ''.join([choice(p_chars) for i in range(p_length)])