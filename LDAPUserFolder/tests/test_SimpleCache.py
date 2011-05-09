#####################################################################
#
# testSimpleCache   Tests for the cache mechanism used by the 
#                   LDAPUserFolder
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
#
#####################################################################
__version__='$Revision: 1320 $'[11:-2]

# General Python imports
import unittest, time

# Zope Imports
from DateTime.DateTime import DateTime

# LDAPUserFolder package imports
from Products.LDAPUserFolder.SimpleCache import SimpleCache
from Products.LDAPUserFolder.SimpleCache import SharedObject

TESTPWD = 'test'

class CacheObject:

    def __init__(self, id):
        self.id = id
        self._created = time.time()

    def _getPassword(self):
        return TESTPWD

    def getCreationTime(self):
        return DateTime(self._created)


class TestSimpleCache(unittest.TestCase):

    def setUp(self):
        self.cache = SimpleCache()
        self.cache.setTimeout(0.1)

    def testInstantiation(self):
        self.assertEqual(len(self.cache.getCache()), 0)

    def testCaching(self):
        nonauth_ob = CacheObject('nonauth')
        self.cache.set('TestId', nonauth_ob)
        self.assertEqual(len(self.cache.getCache()), 1)
        self.assertEqual( self.cache.get('testid', password=None)
                        , nonauth_ob
                        )
        time.sleep(0.5)
        self.assertEqual( self.cache.get('testid', password=None)
                        , None
                        )
        self.assertEqual(len(self.cache.getCache()), 0)
        auth_ob = CacheObject('auth')
        self.cache.set('NewId', auth_ob)
        self.assertEqual(len(self.cache.getCache()), 1)
        self.assertEqual( self.cache.get('newid', password=TESTPWD)
                        , auth_ob
                        )
        time.sleep(0.5)
        self.assertEqual( self.cache.get('newid', password=TESTPWD)
                        , None
                        )
        self.assertEqual(len(self.cache.getCache()), 0)

    def testRemove(self):
        nonauth_ob = CacheObject('nonauth')
        self.cache.set('TestId', nonauth_ob)
        self.cache.remove('testid')
        self.assertEqual(len(self.cache.getCache()), 0)
        auth_ob = CacheObject('auth')
        self.cache.set('NewId', auth_ob)
        self.cache.remove('newid')
        self.assertEqual(len(self.cache.getCache()), 0)

    def testClear(self):
        nonauth_ob = CacheObject('nonauth')
        self.cache.set('TestId', nonauth_ob)
        auth_ob = CacheObject('auth')
        self.cache.set('NewId', auth_ob)
        self.cache.clear()
        self.assertEqual(len(self.cache.getCache()), 0)
        self.assertEqual(len(self.cache.getCache()), 0)
        
class TestSharedObject(unittest.TestCase):
    def setUp(self):
        self.cache = SharedObject()

    def tearDown(self):
        del self.cache

    def testSetGetClear(self):
        self.cache.set('foo', 'bar')
        self.assertEqual(self.cache.values['foo'], 'bar')
        self.assertEqual(self.cache.get('foo'), 'bar')
        self.cache.set('baz', 'fleeb')
        items = self.cache.values.items()
        items.sort()
        self.assertEqual(items, [('baz', 'fleeb'), ('foo', 'bar')])
        self.cache.clear('foo')
        items = self.cache.values.items()
        items.sort()
        self.assertEqual(items, [('baz', 'fleeb')])
        self.cache.set('foo', 'feez')
        items = self.cache.values.items()
        items.sort()
        self.assertEqual(items, [('baz', 'fleeb'), ('foo', 'feez')])
        self.cache.clear()
        self.assertEqual(self.cache.values.keys(), [])
    

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSimpleCache))
    suite.addTest(unittest.makeSuite(TestSharedObject))

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
    
