import sys
import os
import json
import unittest

testDir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.dirname(testDir))
import flow360client
assert(os.path.dirname(flow360client.__file__) == os.path.abspath(os.path.join(testDir,'..','flow360client')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from flow360client.version import Flow360Version

class TestVersionCompare(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestVersionCompare, self).__init__(*args, **kwargs)

    def test_versionBasic(self):
        self.assertTrue(Flow360Version('beta-0.3.0').tail == [0,3,0])
        self.assertTrue(Flow360Version('be--ta-0.3.1').tail == [0,3,1])
        self.assertTrue(Flow360Version('release-22.1.3.0').tail == [22,1,3,0])
        self.assertTrue(Flow360Version('dummy-22.1.3.0').tail == [22,1,3,0])
        self.assertTrue(Flow360Version('du-1m-m2y3-22.1.3.0').tail == [22,1,3,0])
        self.assertTrue(Flow360Version('du-1m-m2y3-22.1.3.0').head == 'du-1m-m2y3')

    def test_versionCompareLt(self):
        self.assertTrue(Flow360Version('beta-21.4.999.999') < Flow360Version('beta-22.1.3.0'))
        self.assertTrue(Flow360Version('release-21.4.999.999') < Flow360Version('beta-22.1.3.0'))
        self.assertTrue(Flow360Version('release-20.4.999.1') < Flow360Version('beta-22.1.3.0'))
        self.assertTrue(Flow360Version('release-0.3.0') < Flow360Version('beta-20.4.1.0'))
        self.assertTrue(Flow360Version('release-0.3.0.999') < Flow360Version('release-0.3.1'))
        self.assertTrue(Flow360Version('release-22.1.1.0') < Flow360Version('beta-22.1.1.1'))
        self.assertTrue(Flow360Version('release-22.3.4.0') < Flow360Version('beta-22.3.4.100'))
        self.assertTrue(Flow360Version('release-22.3.4.0') < Flow360Version('beta-22.3.10'))
        self.assertTrue(Flow360Version('release-22.3.4.0') < Flow360Version('beta-22.20.10'))
        self.assertTrue(Flow360Version('release-22.3.4.0') < Flow360Version('beta-100.20.10'))

        self.assertFalse(Flow360Version('release-0.3.1') < Flow360Version('release-0.3.1'))
        self.assertFalse(Flow360Version('release-22.1.3.0') < Flow360Version('release-22.1.3.0'))
        self.assertFalse(Flow360Version('release-22.2.1.0') < Flow360Version('release-0.3.1'))

    def test_versionCompareGe(self):
        self.assertTrue(Flow360Version('release-22.2.1.0') >= Flow360Version('release-22.2.1.0'))
        self.assertTrue(Flow360Version('beta-22.10.1.1') >= Flow360Version('release-22.3.1.3'))

    def test_versionCompareEq(self):
        self.assertTrue(Flow360Version('release-22.2.1.0') == Flow360Version('release-22.2.1.0'))

    def test_versionCompareNe(self):
        self.assertTrue(Flow360Version('beta-22.2.1.0') != Flow360Version('release-22.2.1.0'))
        self.assertTrue(Flow360Version('release-22.2.1.1') != Flow360Version('release-22.2.1.0'))

if __name__ == '__main__':
    unittest.main()
