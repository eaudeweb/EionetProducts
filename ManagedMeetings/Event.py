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

from html2text import html2text
from IEvent import IEvent
from Globals import MessageDialog

import string
from time import *


# QuotedPrintable functions
ESCAPE = '='
MAXLINESIZE = 76
HEX = '0123456789ABCDEF'
CDATE =  "%Y%m%dT%H%M%S"
CDATEZ = "%Y%m%dT%H%M%SZ"

def _needsquoting(c):
    """Decide whether a particular character needs to be quoted."""

    return c == ESCAPE or not(' ' < c <= '~')

def _quote(c):
    """Quote a single character."""
    i = ord(c)
    if i == 13:
        return ""
    if i == 10:    # Handle UNIX newline
        return ESCAPE + '0D' + ESCAPE + '0A'
    else:
        return ESCAPE + HEX[i/16] + HEX[i%16]

def _qp_encode(line,offset):
    """Read 'line', apply quoted-printable encoding, and return it.
        """
    output=''
    if not line:
        return None
    new = ''
    prev = ''
    for c in line:
        if _needsquoting(c):
            c = _quote(c)
        if offset + len(new) + len(c) >= MAXLINESIZE:
            output = output + new + ESCAPE + '\r\n '
            offset = 0
            new = ''
        new = new + c
        prev = c
    if prev in (' ', '\t'):
        output = output + new + ESCAPE + '\r\n'
    else:
        output = output + new + '\r\n'
    return output

def _slash_encode(line,offset):
    "Backslash-escape a string"
    new = ''
    output=''
    for c in line:
        x = c
        if c in [';','\\', ',' ]:
            x = '\\' + c
        if c == '\n':
            x = '\\n'
        if offset + len(new) + len(c) >= MAXLINESIZE:
            output = output + new + '\r\n '
            offset = 0
            new = ''
        new = new + x
    output = output + new + '\r\n'
    return output

class OutputHelp:
    """ This class is here so incremental output works.
        Apache will send a Content-Length = 0 if you use RESPONSE.write
        and doesn't set content length manually.
    """
    def __init__(self):
        self.body = ""

    def write(self,data):
        self.body = self.body + data

    def flush(self):
        pass
    
    def purge(self):
        return self.body

class BaseEvent:
    """ BaseEvent class, implements IEvent interface"""

    __implements__=IEvent


    def show_vcs(self,REQUEST,RESPONSE):
        """Generate vCalendar file"""
        outobj = OutputHelp()
        RESPONSE.setHeader('Content-Type', 'text/x-vCalendar')
        RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s.vcs"' % self.id)
        outobj.write("BEGIN:VCALENDAR\r\n")
        outobj.write("PRODID:-//European Environment Agency//Managed Meetings//EN\r\n")
        outobj.write("VERSION:1.0\r\n")
        outobj.write("BEGIN:VEVENT\r\n")
        outobj.write("DTSTART:%s\r\n" % self.startdate.strftime(CDATE))
        outobj.write("DTEND:%s\r\n" % self.enddate.strftime(CDATE))
        if hasattr(self, "location") and self.location != '' :
            outobj.write("LOCATION;ENCODING=8-bit:%s\r\n" % self.location)
        elif hasattr(self, "txtlocation") and self.txtlocation!='':
            outobj.write("LOCATION;ENCODING=8-bit:%s\r\n" % self.txtlocation)
        elif hasattr(self, "urllocation") and self.urllocation!='':
            outobj.write("LOCATION;ENCODING=8-bit:%s\r\n" % self.urllocation)
        outobj.write("UID:%s\r\n" % REQUEST.URL0)
        outobj.write("URL:%s\r\n" % REQUEST.URL1)
        outobj.write("SUMMARY:%s\r\n" % self.title)
        if self.description != '':
            outobj.write("DESCRIPTION;ENCODING=QUOTED-PRINTABLE:%s" % \
               _qp_encode(self.description,37))
# Check for relative address.
#       if self.agenda_url:
#           outobj.write("ATTACH;VALUE=URL:%s\r\n" % self.agenda_url)

        for t in self.objectValues(['File', 'DTML Document','Image']):
            outobj.write("ATTACH;VALUE=URL:%s\r\n" % t.absolute_url())

#       for a in self.objectValues('Meeting Attendee'):
#           outobj.write("ATTENDEE;ROLE=%s;STATUS=%s:%s %s <%s>\r\n" % \
#                      (a.role, a.attending, a.givenname, a.sn, a.mail))
        outobj.write("END:VEVENT\r\n")
        outobj.write("END:VCALENDAR\r\n")
        return outobj.purge()


    def show_ics(self,REQUEST,RESPONSE):
        """Generate iCalendar file"""
        outobj = OutputHelp()
        RESPONSE.setHeader('Content-Type', 'text/calendar')
        RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s.ics"' % self.id)
        outobj.write("BEGIN:VCALENDAR\r\n")
        outobj.write("PRODID:-//European Environment Agency//Managed Meetings//EN\r\n")
        outobj.write("VERSION:2.0\r\n")
        outobj.write("METHOD:PUBLISH\r\n")
        outobj.write("BEGIN:VEVENT\r\n")
#       for a in self.objectValues('Meeting Attendee'):
#           outobj.write('ATTENDEE;ROLE=REQ-PARTICIPANT:MAILTO:%s %s <%s>\r\n' % \
#                      ( a.givenname, a.sn, a.mail))
        if self.organiser!='':
            email=''
            if hasattr(self,"organiser_email"):
                email=self.organiser_email
            outobj.write('ORGANIZER;CN="%s":MAILTO="%s"\r\n' % ( self.organiser, email))
        outobj.write("DTSTART:%s\r\n" % self.startdate.strftime(CDATE))
        outobj.write("DTEND:%s\r\n" % self.enddate.strftime(CDATE))
        if hasattr(self,"location") and self.location != '' :
            outobj.write('LOCATION;ALTREP="%s/%s":%s\r\n' % \
             (REQUEST.URL2, self.location, self.location))
        elif hasattr(self,"txtlocation"):
            outobj.write("LOCATION:%s\r\n" % self.txtlocation)
        elif hasattr(self,"urllocation") and self.urllocation !='' :
            outobj.write("LOCATION:%s\r\n" % self.urllocation)
        outobj.write("TRANSP:OPAQUE\r\n")
        outobj.write("SEQUENCE:%d\r\n" % self.generation)
        outobj.write("UID:%s\r\n" % REQUEST.URL0)
        outobj.write("URL:%s\r\n" % REQUEST.URL1)
        outobj.write("LAST-MODIFIED:%s\r\n" % \
            self.bobobase_modification_time().toZone('UTC').strftime(CDATEZ))

        outobj.write("DTSTAMP:%s\r\n" % \
            strftime(CDATEZ,gmtime(time())))
        if self.description != '':
            outobj.write("DESCRIPTION:%s" % _slash_encode(self.description,12))
        outobj.write("SUMMARY:%s\r\n" % self.title)

        outobj.write("PRIORITY:5\r\n")
        outobj.write("CLASS:PUBLIC\r\n")
        outobj.write("END:VEVENT\r\n")
        outobj.write("END:VCALENDAR\r\n")
        return outobj.purge()

    def textdescription(self,REQUEST=None):
        """ Generate a text equivalent of description in HTML """
        return html2text(self.description.decode('utf8'), self.absolute_url()).encode('utf8')

