import os, sys, time
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
ZopeTestCase.installProduct('GimmeThesaurus')

class GimmeTestCase(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        self.app.manage_addProduct['GimmeThesaurus'].manage_addThesaurus('gemet')
        self.assertTrue(hasattr(self.app, 'gemet'),'Counter did not get created')
        self.assertNotEqual(self.app.gemet, None)

    # Test example
    def test_ex(self):
        RESPONSE = self.app.REQUEST.RESPONSE
        self.app.REQUEST.set('path', 'something')
        self.assertEquals(1,1)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(GimmeTestCase))
    return suite

if __name__ == '__main__':
    framework()
