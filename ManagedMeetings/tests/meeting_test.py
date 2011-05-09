#zope installation directory

zope_path = "D:\zope_farms\Nila\lib\python"

def fixpath():
    import sys
    sys.path.append(zope_path)

try:
    import Zope
except ImportError:
    fixpath()
    import Zope

import ZODB
from Testing import makerequest
import Globals
import App.Product
from Products.ManagedMeetings.ManagedMeetings import ManagedMeetings, manage_addManagedMeetings


import unittest

#constants
meet_folder = "meetings"
meet = "training"

class MyTest(unittest.TestCase):

    def setUp(self):
        """ """
        import Zope
        Zope.startup()
        self.connection = Zope.DB.open()
        get_transaction().begin()
        try:
            self.root = makerequest.makerequest(self.connection.root()['Application'])
        except:
            print "error1"
            self.tearDown()
            raise

    def tearDown(self):
        """ """
        #get_transaction().abort()
        get_transaction().commit()
        self.connection.close()

        ###########
        #     getters     #
        ###########

    def get_meeting_folder(self):
        """ """
        obj = getattr(self.root, meet_folder)
        return obj

    def get_meeting(self):
        """ """
        folder = getattr(self.root, meet_folder)
        obj = getattr(folder, meet)
        return obj

    ###############
    #       add objects      #
    ###############

    def test01_addmeetingfolder(self):
        """ test meeting folder"""
        self.root.manage_addProduct['ManagedMeetings'].manage_addManagedMeetings(id=meet_folder, title='test meeting folder', 
                description='testmeeting', event_types=['Event', 'Meeting'], mailhost=['MailHost'])
        print "add meeting folder successfully"

    def test02_addmeeting(self):
        """ test add meeting """
        m_folder = self.get_meeting_folder()
        m_folder.manage_addProduct['ManagedMeetings'].manage_addMeeting(id=meet, title='', event_type=[], location="", txtlocation="", description="", 
                startdate="2004/07/16 9:00", enddate="2004/07/17 9:00", organiser="", organiser_email="", max_attendees=0)
        #tine minte ca asta dadea eroare fiindca MB nu era instalat - line 113
        print "added meeting successfully"

    def test03_addlocation(self):
        """ test add location"""
        m_folder = self.get_meeting_folder()
        m_folder.manage_addProduct['ManagedMeetings'].manage_addLocation(id='bucharest', description='', title='', address='', url='', map_url='', 
            roadmap_url='', max_seats=0)
        print "added location successfully"

    def test04_addagenda(self):
        """ """
        m_obj = self.get_meeting()
        m_obj.manage_addProduct['ManagedMeetings'].manage_addAgendaItem(id='agenda', title='', track='', session='', 
                session_ord='', duration='', location='', author='', abstract='', paper_url='', slides_url='', url='', keywords='', 
                actions_agreed='', actions_comp='', minutes='', speakers=[], confirmed=0)
        #tine minte ca asta dadea eroare la agenda
        print "added location successfully"

#
#    def test_addattendee(self):
#        """ """
#        pass
#

#    def test11_deleteeverything(self):
#        """ delete the meeting """
#        m_folder = getattr(self.root, meet_folder)
#        print 'title1: %s' % m_folder.title
#        self.root._delObject(meet_folder)
#        print "delete everything"
#        m_folder = getattr(self.root, meet_folder)
#        print 'title2: %s' % m_folder.title


#
#    def test_addsession(self):
#        """ """
#        pass
#
#    def test_addtrack(self):
#        """ """
#        pass
#
#    def test_addbreak(self):
#        """ """
#        pass
#
#    def test_addboard(self):
#        """ """
#        pass
#
#    def test_addattendeeprops(self):
#        """ """
#        pass

def test_suite():
    return unittest.makeSuite(MyTest)

def main():
    unittest.TextTestRunner().run(test_suite())

if __name__ == "__main__":
    fixpath()
    main()
