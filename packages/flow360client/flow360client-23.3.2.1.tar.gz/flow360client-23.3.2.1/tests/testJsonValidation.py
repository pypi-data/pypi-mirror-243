import json
import os
import unittest
import sys

here = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.dirname(here))
import flow360client
from flow360client.surfaceMesh import validateSurfaceMeshJSON
from flow360client.mesh import validateVolumeMeshJSON
from flow360client.case import validateCaseJSON

testVersions = [
    {
        "name": None, 
        "failOnIncorrect": True,
        "passOnCorrect": True,
        "successMessage": True
    }, {
        "name": 'release-21.4.1.0', 
        "failOnIncorrect": False,
        "passOnCorrect": True,
        "successMessage": False
    }, {
        "name": 'release-22.2.3.0', 
        "failOnIncorrect": True,
        "passOnCorrect": True,
        "successMessage": True
    }, {
        "name": 'release-22.3.3.0', 
        "failOnIncorrect": True,
        "passOnCorrect": True,
        "successMessage": True
    }, {
        "name": 'notExistingRelease-0.0.0.0', 
        "failOnIncorrect": False,
        "passOnCorrect": True,
        "successMessage": False
    }]


class TestValidation(unittest.TestCase):

    meshIds = {}
    @classmethod
    def uploadMesh(cls, version):
        if version not in cls.meshIds:
            meshFile = os.path.join(here, 'data/wing_tetra.1.lb8.ugrid.gz')
            meshJson =  os.path.join(here, 'data/wing_tetra_mesh.json')
            meshId = flow360client.NewMesh(fname=meshFile, meshJson=meshJson, solverVersion=version)
            cls.meshIds[version] = meshId
        else:
            meshId = cls.meshIds[version]
        return meshId    

    @classmethod
    def tearDownClass(cls):
        print('removing meshes after tests')
        for version, meshId in cls.meshIds.items():
            print(f'removing {meshId} of version {version}')
            flow360client.mesh.DeleteMesh(meshId)

    def getSurfaceMeshConfig(self, correct=True):
        jsonFile = os.path.join(here, 'data/geoToSurface/test_surface.json')
        with open(jsonFile) as fh:
            config = json.load(fh)

        if correct==False:    
            config['nonExistingField'] = None
        return config    

    def getVolumeMeshConfig(self, correct=True):
        jsonFile = os.path.join(here, 'data/surfaceToVolume/meshVolume.airplane.json')
        with open(jsonFile) as fh:
            config = json.load(fh)

        if correct==False:    
            config['nonExistingField'] = None
        return config    

    def getCaseConfig(self, correct=True):
        jsonFile = os.path.join(here, 'data/wing_tetra.1.json')
        with open(jsonFile) as fh:
            config = json.load(fh)

        if correct==False:    
            config['nonExistingField'] = None
        return config    

    def test_validateSurfaceMeshCorrectJson(self):
        config = self.getSurfaceMeshConfig(correct=True)
        for version in testVersions:
            print('testing:', version)
            res = validateSurfaceMeshJSON(json.dumps(config), version['name'])
            if version['passOnCorrect'] and version['successMessage']:
                self.assertTrue(res['success'])
            else:
                self.assertIsNone(res)    

    def test_validateSurfaceMeshIncorrectJson(self):
        config = self.getSurfaceMeshConfig(correct=False)
        for version in testVersions:
            print('testing:', version)
            if version["failOnIncorrect"]:
                self.assertRaises(ValueError, validateSurfaceMeshJSON, json.dumps(config), version['name'])
            else:
                res = validateSurfaceMeshJSON(json.dumps(config), version['name'])
                self.assertIsNone(res)    

    def test_validateVolumeMeshCorrectJson(self):
        config = self.getVolumeMeshConfig(correct=True)
        for version in testVersions:
            print('testing:', version)
            res = validateVolumeMeshJSON(json.dumps(config), version['name'])
            if version['passOnCorrect'] and version['successMessage']:
                self.assertTrue(res['success'])
            else:
                self.assertIsNone(res)    

    def test_validateVolumeMeshIncorrectJson(self):
        config = self.getVolumeMeshConfig(correct=False)
        for version in testVersions:
            print('testing:', version)
            if version["failOnIncorrect"]:
                self.assertRaises(ValueError, validateVolumeMeshJSON, json.dumps(config), version['name'])
            else:
                res = validateVolumeMeshJSON(json.dumps(config), version['name'])
                self.assertIsNone(res)

    def test_validateCaseCorrectJson(self):
        config = self.getCaseConfig(correct=True)
        for version in testVersions:
            print('testing:', version)
            meshId = self.uploadMesh(version['name'])
            res = validateCaseJSON(json.dumps(config), meshId, version['name'])
            if version['passOnCorrect'] and version['successMessage']:
                self.assertTrue(res['success'])
            else:
                self.assertIsNone(res)    

    def test_validateCaseIncorrectJson(self):
        config = self.getCaseConfig(correct=False)
        for version in testVersions:
            print('testing:', version)
            meshId = self.uploadMesh(version['name'])
            if version["failOnIncorrect"]:
                self.assertRaises(ValueError, validateCaseJSON, json.dumps(config), meshId, version['name'])
            else:
                res = validateCaseJSON(json.dumps(config), meshId, version['name'])
                self.assertIsNone(res)


if __name__ == '__main__':
    unittest.main()

