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
# Tomas Hjelmberg, CMG
#

__doc__="""Meeting initialization module"""
__version__= '$Revision: 1.24 $'[11:-2]

from ImageFile import ImageFile
import ManagedMeetings
import Meeting
import Location
import AnnouncedEvent

def initialize(context):
    """ManagedMeetings"""

    context.registerClass(
        ManagedMeetings.ManagedMeetings,
        permission='Add Meetings Folder',
        constructors = (ManagedMeetings.manage_addManagedMeetingsForm,
                        ManagedMeetings.manage_addManagedMeetings,
                        ManagedMeetings.getMailHostList
                        ),
        icon='icons/ManagedMeetings.gif',
        )
    context.registerClass(
        Meeting.Meeting,
        permission='Add Meeting',
        constructors = (Meeting.manage_addMeetingForm,
                        Meeting.manage_addMeeting
                        ),
        icon='icons/Meeting.gif',
        )
    context.registerClass(
        AnnouncedEvent.AnnouncedEvent,
        permission='Add Announced Event',
        constructors = (AnnouncedEvent.manage_addAnnouncedEventForm,
                        AnnouncedEvent.manage_addAnnouncedEvent
                        ),
        icon='icons/AnnouncedEvent.gif',
        )
    context.registerClass(
        Location.Location,
        permission='Add Meeting Location',
        constructors = (Location.manage_addLocationForm,
                        Location.manage_addLocation
                        ),
        icon='icons/Location.gif',
        )
    context.registerHelp()
    context.registerHelpTitle('ManagedMeetings')

# Define shared web objects that are used by products.
# This is usually (always ?) limited to images used
# when displaying an object in contents lists.
# These objects are accessed as:
#   <dtml-var SCRIPT_NAME>/misc_/Product/name

# The first five pictures are for compatibility with previous versions
misc_ = {
        "agenda.gif":   ImageFile("icons/agenda.gif", globals()),
        "track.gif":   ImageFile("icons/track.gif", globals()),
        "session.gif":   ImageFile("icons/session.gif", globals()),
        "break.gif":   ImageFile("icons/break.gif", globals()),
        "Attendee.gif":   ImageFile("icons/Attendee.gif", globals()),
        "ExtraProps.gif":   ImageFile("icons/ExtraProps.gif", globals()),

        "addfile_png":  ImageFile("icons/addfile.png", globals()),
        "attendees_png":  ImageFile("icons/attendees.png", globals()),
        "icalendar_png":  ImageFile("icons/icalendar.png", globals()),
        "sendemail_png":  ImageFile("icons/sendemail.png", globals()),
        "vcalendar_png":  ImageFile("icons/vcalendar.png", globals()),

        "Overview_but.jpg":     ImageFile("icons/overview_but.jpg",     globals()),
        "IWillAttend_but.jpg":  ImageFile("icons/iwillattend_but.jpg",  globals()),
        "SignUp_but.jpg":       ImageFile("icons/signup_but.jpg",       globals()),
        "vCalendar_but.jpg":    ImageFile("icons/vcalendar_but.jpg",    globals()),
        "iCalendar_but.jpg":    ImageFile("icons/icalendar_but.jpg",    globals()),
        "Tracks_but.jpg":       ImageFile("icons/tracks_but.jpg",               globals()),
        "Attendees_but.jpg":    ImageFile("icons/attendees_but.jpg",    globals()),
        "EmailAll_but.jpg":     ImageFile("icons/emailall_but.jpg",     globals()),
        "extradocuments_but.jpg":       ImageFile("icons/extradocuments_but.jpg",       globals()),
        "hint.gif":     ImageFile("icons/hint.gif",     globals()),
        "edit.gif":     ImageFile("icons/edit.gif",     globals()),
        }
