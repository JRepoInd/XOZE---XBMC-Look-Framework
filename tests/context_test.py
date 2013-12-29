'''
Created on Oct 12, 2013

@author: ajju
'''
from xoze.context import XozeContext, AddonContext
import unittest


class ContextTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_load_xml(self):
        addon_context = AddonContext(addon_id='addon.id', conf={'contextFiles':['xoze.xml'], 'webServiceEnabled':True, 'webServicePath':'/Xoze', 'webServicePort':8080})
        addon_context.do_clean()
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
