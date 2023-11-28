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
        self.meshFile = abspath('data/cylinder.cgns')

    def test_meshMeshJsonCorrect(self):
        meshJson = abspath('data/cylinder_mesh.json')
        with open(meshJson) as meshJsonFh:
            valid = validateMeshAndMeshJson(self.meshFile, json.load(meshJsonFh))
            self.assertTrue(valid)

    def test_meshMeshJsonWrong(self):
        meshJson = {'boundaries': {'noSlipWalls' : ['wall']}}
        with self.assertRaises(ValueError) as context:
            valid = validateMeshAndMeshJson(self.meshFile, meshJson)
        self.assertTrue('not found in mesh: wall' in str(context.exception))

    def test_NewMeshCorrect(self):
        meshJson = abspath('data/cylinder_mesh.json')
        with open(meshJson) as fh:
            meshId = NewMesh(self.meshFile, meshJson=json.load(fh))
            DeleteMesh(meshId)

    def test_NewMeshWrong(self):
        meshJson = {'boundaries': {'noSlipWalls' : ['wall']}}
        meshId = None
        with self.assertRaises(ValueError) as context:
            meshId = NewMesh(self.meshFile, noSlipWalls=meshJson['boundaries']['noSlipWalls'])
        self.assertTrue('not found in mesh: wall' in str(context.exception))

    def test_SubmitWrongFile(self):
        meshJson = {'boundaries': {'noSlipWalls' : ['wall']}}
        with self.assertRaises(ValueError) as context:
            meshId = NewMesh(self.meshFile, meshJson=meshJson)
        self.assertTrue('not found in mesh: wall' in str(context.exception))

    def test_SubmitWrongWalls(self):
        with self.assertRaises(ValueError) as context:
            meshId = NewMesh(self.meshFile, noSlipWalls=['wall'])
        self.assertTrue('not found in mesh: wall' in str(context.exception))

    def test_ValidateCaseCorrect(self):
        caseJsonFile = abspath('data/cylinder_case.json')
        with open(caseJsonFile) as fh:
            valid = validateMeshAndCaseJson(self.meshFile, json.load(fh))
            self.assertTrue(valid)

    def test_ValidateCaseWrong1(self):
        caseJson =  {   "boundaries" : {
                "fluid/farfield" : {
                    "type" : "Freestream"
                },
                "fluid/periodic_0_l" : {
                    "type" : "SlipWall"
                },
                "fluid/periodic_0_r" : {
                    "type" : "SlipWall"
                }
                }}

        with self.assertRaises(ValueError) as context:
            valid = validateMeshAndCaseJson(self.meshFile, caseJson)
        self.assertTrue('missing in case json: fluid/wall' in str(context.exception))

    def test_ValidateCaseWrong2(self):
        caseJson =  {   "boundaries" : {
                "fluid/walls" : {
                    "type" : "NoSlipWall"
                },
                "fluid/farfield" : {
                    "type" : "Freestream"
                },
                "fluid/periodic_0_r" : {
                    "type" : "SlipWall"
                }
                }}

        with self.assertRaises(ValueError) as context:
            valid = validateMeshAndCaseJson(self.meshFile, caseJson)
        self.assertTrue('not found in mesh: fluid/walls' in str(context.exception))
        self.assertTrue('missing in case json: fluid/wall, fluid/periodic_0_l' in str(context.exception))

if __name__ == '__main__':
    unittest.main()

