import sys
import os
import json
import unittest

testDir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.dirname(testDir))
import flow360client
assert(os.path.dirname(flow360client.__file__) == os.path.abspath(os.path.join(testDir,'..','flow360client')))

from flow360client.meshUtils import validateMeshAndMeshJson, validateMeshAndCaseJson
from flow360client import NewMesh
from flow360client.mesh import DeleteMesh

def abspath(fname):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fname))

class TestValidateCGNSmesh(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestValidateCGNSmesh, self).__init__(*args, **kwargs)
        self.meshFile = abspath('data/cylinder_combinedBnd.cgns')

    def test_meshMeshJsonWrong(self):
        meshJson = {'boundaries': {'noSlipWalls' : ['fluid/wall']}}
        with self.assertRaises(ValueError) as context:
            valid = validateMeshAndMeshJson(self.meshFile, meshJson, solverVersion='release-22.1.3.0')
        self.assertTrue('not found in mesh: fluid/wall' in str(context.exception))

    def test_SubmitWrongWalls(self):
        with self.assertRaises(ValueError) as context:
            meshId = NewMesh(self.meshFile, noSlipWalls=['fluid/wall'], solverVersion='release-22.1.3.0')
        self.assertTrue('not found in mesh: fluid/wall' in str(context.exception))

    def test_meshMeshJsonCorrect(self):
        meshJson = {'boundaries': {'noSlipWalls' : ['fluid/mergedBoundaryPatches']}}
        valid = validateMeshAndMeshJson(self.meshFile, meshJson, solverVersion='dummy-22.1.3.999')
        self.assertTrue(valid)

    def test_SubmitWrongWalls(self):
        meshId = NewMesh(self.meshFile, noSlipWalls=['fluid/mergedBoundaryPatches'], solverVersion='release-22.1.3.0')
        self.assertTrue(isinstance(meshId, str))

if __name__ == '__main__':
    unittest.main()
