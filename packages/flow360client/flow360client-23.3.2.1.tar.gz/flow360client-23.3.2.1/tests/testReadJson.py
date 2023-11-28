import sys
import os
import json
import unittest

testDir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.dirname(testDir))
import flow360client
assert(os.path.dirname(flow360client.__file__) == os.path.abspath(os.path.join(testDir,'..','flow360client')))
from flow360client.IOutils import readJsonFileOrDict

def abspath(fname):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fname))

class TestReadInput(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestReadInput, self).__init__(*args, **kwargs)

    def setUp(self):
        self.jsonFile = abspath('data/rotation_2vol_radial_mesh.json')
        with open(self.jsonFile) as fh:
            self.jsonObj = json.load(fh)

    def test_FileSuccess(self):
        self.assertTrue(self.jsonObj == readJsonFileOrDict(self.jsonFile))

    def test_FileNotExist(self):
        with self.assertRaises(FileNotFoundError) as context:
            readJsonFileOrDict('fakeDir/fakeFile.json')
        self.assertTrue(context.exception.errno == 2)

    def test_WrongType(self):
        with self.assertRaises(TypeError) as context:
            readJsonFileOrDict(1)
        self.assertTrue('Input file has wrong type.' == str(context.exception))

    def test_JsonSuccess(self):
        self.assertTrue(self.jsonObj == readJsonFileOrDict(self.jsonObj))

if __name__ == '__main__':
    unittest.main()
