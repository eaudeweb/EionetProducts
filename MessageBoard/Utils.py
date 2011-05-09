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
# Cornel Nitu, Rares Vernica Finsiel Romania
#
import types
import re
import time
import MimeWriter
import mimetools
import cStringIO
from DateTime import DateTime
from Products.PythonScripts.standard import html_quote
from types import UnicodeType


def isUnicode(s):
    return isinstance(s, UnicodeType)

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

    if re.compile(r'^[_\-\.0-9a-z]+@([0-9a-z][_\-0-9a-z\.]+)\.([a-z]{2,4}$)', re.IGNORECASE).search(email) is None:
        return 0

    return 1


def createEmail(eContent, eTo, eFrom, eSubject):
    """Create a mime-message that will render as text"""
    out = cStringIO.StringIO() # output buffer for our message
    writer = MimeWriter.MimeWriter(out)

    # set up some basic headers
    writer.addheader("From", eFrom)
    writer.addheader("To", eTo)
    writer.addheader("Subject", eSubject)
    writer.addheader("MIME-Version", "1.0")
    writer.addheader("Date", time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))

    # start the multipart section of the message
    writer.startmultipartbody("alternative")
    writer.flushheaders()

    # the plain text section
    subpart = writer.nextpart()
    pout = subpart.startbody("text/plain", [("charset", 'utf-8')])
    pout.write(eContent)

    #close your writer and return the message body
    writer.lastpart()
    msg = out.getvalue()
    out.close()
    return msg


def extract_urls(msg):
    """ Functions to identify and replace URLs with hrefs"""
    msg = _newlineToBr(msg)
    strg = re.sub(r'(?P<url>http[s]?://[-_&;,?:~=%#+/.0-9a-zA-Z]+)', 
                  r'<a href="\g<url>">\g<url></a>', msg)
    return strg.strip()


def _newlineToBr(s):
    return html_quote(s).replace('\n', '<br />')


def generateId():
    return int(time.time())


def getToday():
    """Returns today date in a DateTime object"""
    return DateTime()