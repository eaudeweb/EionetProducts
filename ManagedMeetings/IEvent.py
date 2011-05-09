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

from Interface import Base

class IEvent(Base):
    """ """
    def show_ics(self,REQUEST,RESPONSE):
        """Generate iCalendar file"""

    def show_vcs(self,REQUEST,RESPONSE):
        """Generate vCalendar file"""

    def textdescription(self,REQUEST,RESPONSE):
        """Produce a plain text version of the description"""

