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
#$Id: SessionManager.py 3445 2005-04-22 19:16:30Z nituacor $

__version__='$Revision: 1.4 $'[11:-2]

#constants
_SESSION_LANG = "site_language"
_SESSION_INFO = "site_infos"
_SESSION_ERROR = "site_errors"

class SessionManager:
    """This class has some methods to work with session variables"""

    def __init__(self):
        """Constructor"""
        pass

    def __isSession(self, key):
        """Test if exists a variable with the given key in SESSION"""
        return self.REQUEST.SESSION.has_key(key)

    def __getSession(self, key, default):
        """Get a key value from SESSION; if that key doesn't exist then return default value"""
        try:
            return self.REQUEST.SESSION[key]
        except:
            return default

    def __setSession(self, key, value):
        """Add a value to SESSION"""
        try:
            self.REQUEST.SESSION.set(key, value)
        except:
            pass

    def __delSession(self, key):
        """Delete a value from SESSION"""
        try:
            self.REQUEST.SESSION.delete(key)
        except:
            pass


    #Public methods
    def getSessionValue(self, key, default):
        """ Returns the session value for one key """
        return self.__getSession(key, default)

    def setSession(self, key, value):
        """ Set the session value for key """
        return self.__setSession(key, value)

    def delSession(self, key):
        """ Delete a key from session """
        return self.__delSession(key)

    def isSession(self, key):
        """ Returns true if this key exists in session """
        return self.__isSession(key)



    #manage information
    def isSessionInfo(self):
        """Returns true if this key exists"""
        return self.__isSession(_SESSION_INFO)

    def getSessionInfo(self, default=None):
        """Returns the session value for errors"""
        return self.__getSession(_SESSION_INFO, default)

    def setSessionInfo(self, value):
        """Set the session value for errors"""
        self.__setSession(_SESSION_INFO, value)

    def delSessionInfo(self):
        """Delete a key"""
        self.__delSession(_SESSION_INFO)



    #language
    def getSessionLanguage(self, default=None):
        """Returns the session value for errors"""
        return self.__getSession(_SESSION_LANG, default)

    def setSessionLanguage(self, value):
        """Set the session value for errors"""
        self.__setSession(_SESSION_LANG, value)

    def delSessionLanguage(self):
        """Delete a key"""
        self.__delSession(_SESSION_LANG)



    #language
    def getSessionErrors(self, default=None):
        """Returns the session value for errors"""
        return self.__getSession(_SESSION_ERROR, default)

    def setSessionErrors(self, value):
        """Set the session value for errors"""
        self.__setSession(_SESSION_ERROR, value)

    def delSessionErrors(self):
        """Delete a key"""
        self.__delSession(_SESSION_ERROR)

    def isSessionErrors(self):
        """Returns true if this key exists"""
        return self.__isSession(_SESSION_ERROR)

    #manage database
    def setDBSession(self, db_host, db_name, db_user, db_password, db_port):
        """ """
        self.__setSession('db_host', db_host)
        self.__setSession('db_name', db_name)
        self.__setSession('db_user', db_user)
        self.__setSession('db_password', db_password)
        self.__setSession('db_port', db_port)

    def delDBSession(self):
        """ """
        self.__delSession('db_host')
        self.__delSession('db_name')
        self.__delSession('db_user')
        self.__delSession('db_password')
        self.__delSession('db_port')

    def getSessionDBHost(self):
        """ """
        return self.__getSession('db_host', self.db_host)

    def getSessionDBName(self):
        """ """
        return self.__getSession('db_name', self.db_name)

    def getSessionDBUser(self):
        """ """
        return self.__getSession('db_user', self.db_user)

    def getSessionDBPassword(self):
        """ """
        return self.__getSession('db_password', self.db_password)

    def getSessionDBPort(self):
        """ """
        return self.__getSession('db_port', self.db_port)