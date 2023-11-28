import sys
import os
import json
import unittest

testDir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.dirname(testDir))
import flow360client
assert(os.path.dirname(flow360client.__file__) == os.path.abspath(os.path.join(testDir,'..','flow360client')))
from flow360client.meshUtils import validateMeshAndMeshJson, validateMeshAndCaseJson
from flow360client.mesh import DeleteMesh

def abspath(fname):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fname))

class TestValidateTwoBlockCGNSmesh(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestValidateTwoBlockCGNSmesh, self).__init__(*args, **kwargs)

    def setUp(self):
        self.meshFile = abspath('data/rotation_2vol_radial.cgns')
        with open(abspath('data/rotation_2vol_radial_mesh.json')) as fh:
            self.meshJson = json.load(fh)
        with open(abspath('data/rotation_2vol_radial_case.json')) as fh:
            self.caseJson = json.load(fh)

    def test_meshMeshJsonCorrect(self):
        valid = validateMeshAndMeshJson(self.meshFile, self.meshJson)
        self.assertTrue(valid)

    def test_meshMeshJsonWrong(self):
        self.meshJson['boundaries']['noSlipWalls'].append('fakeWall')
        self.meshJson['slidingInterfaces'][0]['stationaryPatches'].append('fakePatch')
        self.meshJson['slidingInterfaces'][0]['rotatingPatches'].append('fakePatch2')
        with self.assertRaises(ValueError) as context:
            valid = validateMeshAndMeshJson(self.meshFile, self.meshJson)
        self.assertTrue('not found in mesh: fakeWall, fakePatch, fakePatch2' in str(context.exception))

    def test_ValidateCaseCorrect(self):
        valid = validateMeshAndCaseJson(self.meshFile, self.caseJson)
        self.assertTrue(valid)
    
    def test_VlidateCaseWrongBCs(self):
        del self.caseJson['boundaries']['INNER_VOL/INNER_TOP']
        self.caseJson['boundaries']['fakePatch']={'type':'SlipWall'}
        self.caseJson['slidingInterfaces'][0]['rotatingPatches'].append('fakeRotatingPatch')
        with self.assertRaises(ValueError) as context:
            valid = validateMeshAndCaseJson(self.meshFile, self.caseJson)
        self.assertTrue('not found in mesh: fakePatch, fakeRotatingPatch' in str(context.exception))
        self.assertTrue('not found in case json: INNER_VOL/INNER_TOP')

if __name__ == '__main__':
    unittest.main()
