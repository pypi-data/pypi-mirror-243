import json
import os
from os.path import exists
import unittest
import sys
import argparse, tempfile
from testUtils import deleteDir, checkAuthDir

testDir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.dirname(testDir))
import flow360client
assert(os.path.dirname(flow360client.__file__) == os.path.abspath(os.path.join(testDir,'..','flow360client')))

from flow360client import mesh, NewMeshWithTransform, NewMesh
from flow360client.mesh import ListMeshes, GetMeshInfo, getFileCompression, DeleteMesh, DownloadVolumeMesh, \
    GetMeshFileName

oldMeshIds = [
        '201eda54-3e0e-4281-be12-4e6733347c44'
        ]

def abspath(fname):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fname))

class TestMesh(unittest.TestCase):
    def setUp(self):
        global oldMeshIds
        self.meshIdsToTest = oldMeshIds

    def test_ListMeshes(self):
        meshes = ListMeshes()
        self.assertTrue(len(meshes) > 0)
    
    def test_getFileCompression(self):
        compression = getFileCompression("abc.gz")
        self.assertTrue(compression == 'gz')
   
    def test_getMeshInfo(self):
        for meshId in self.meshIdsToTest:
            meshInfo = mesh.GetMeshInfo(meshId)
            self.assertTrue(len(meshInfo) > 0)
    
    def test_downloadMeshProcCustomTarget(self):
        with tempfile.TemporaryDirectory() as tempdir:
            for meshId in self.meshIdsToTest:
                targetFilePath = os.path.join(tempdir, meshId+'.log')
                mesh.DownloadMeshProc(meshId, fileName=targetFilePath)
                self.assertTrue(os.path.exists(targetFilePath))
                self.assertTrue(os.path.getsize(targetFilePath)>0)

    def test_downloadMeshProcDefaultTarget(self):
        for meshId in self.meshIdsToTest:
            with tempfile.TemporaryDirectory() as tempdir:
                currCwd = os.getcwd()
                os.chdir(tempdir)
                mesh.DownloadMeshProc(meshId)
                self.assertTrue(os.path.exists('flow360_volume_mesh.user.log'))
                self.assertTrue(os.path.getsize('flow360_volume_mesh.user.log')>0)
                os.chdir(currCwd)

    def test_downloadVolumeMeshCustomTarget(self):
        with tempfile.TemporaryDirectory() as tempdir:
            for meshId in self.meshIdsToTest:
                targetFilePath = os.path.join(tempdir, meshId+'.meshfile')
                mesh.DownloadVolumeMesh(meshId, target=targetFilePath)
                self.assertTrue(os.path.exists(targetFilePath))
                self.assertTrue(os.path.getsize(targetFilePath))

    def test_DeleteMesh(self):
        resp = mesh.AddMesh('OM6_Wing_Tetra', 'mesh.lb8.ugrid', [1], ['OM6'], 'aflr3', 'little')
        meshId = resp['meshId']
        DeleteMesh(meshId)

    def test_AddMeshWithJsonCGNS(self):
        with open('data/volumeMesh/cylinder_mesh.json') as json_file:
            resp = mesh.AddMeshWithJson('Cylinder_cgns', 'volumeMesh.cgns', json.load(json_file), ['cylinder'], 'cgns', '')
            print(resp)
            meshId = resp['meshId']
            print(meshId)

    def test_AddMeshWithJsonUgrid(self):
        with open('data/volumeMesh/wing_tetra_mesh.json') as json_file:
            resp = mesh.AddMeshWithJson('OM6_Wing_Tetra', 'mesh.lb8.ugrid', json.load(json_file), ['OM6'], 'aflr3', 'little')
            print(resp)
            meshId = resp['meshId']
            print(meshId)

    def test_NewMeshWithNoSlipWalls(self):
        meshId = NewMesh(fname='./data/cylinder.cgns', noSlipWalls=['fluid/wall'], tags=['tag1'], fmat='cgns', endianness='')
        print(meshId)

    def test_AddMeshUploadMesh(self):
        resp = mesh.AddMesh('cylinderMesh', 'volumeMesh.cgns', ['fluid/wall'], ['tag1'], 'cgns', '')
        print(resp)
        meshId = resp['meshId']
        print(meshId)
        mesh.UploadMesh(meshId, './data/cylinder.cgns')

    def test_DownloadVolumeMeshWithZip(self):
        meshInfo = mesh.AddMesh('OM6_Wing_Tetra', 'mesh.lb8.ugrid', [1], ['OM6'], 'aflr3', 'little')
        meshId = meshInfo['meshId']
        mesh.UploadMesh(meshId, abspath('./data/wing_tetra.1.lb8.ugrid.gz'))
        meshInfo = GetMeshInfo(meshId)
        fileName = GetMeshFileName(meshInfo['meshFormat'],
                                   meshInfo['meshEndianness'], meshInfo['meshCompression'])
        DownloadVolumeMesh(meshId, targetDir=meshId)
        self.assertTrue(exists(os.path.join(meshId, fileName)))
        DeleteMesh(meshId)
        deleteDir(meshId)

    def test_DownloadVolumeMeshWithUgrid(self):
        meshInfo = mesh.AddMesh('cylinder', 'volumeMesh.cgns', [1], ['OM6'], 'aflr3', 'little')
        meshId = meshInfo['meshId']
        # once we define ugrld format, the original file has no impact any more. here is just for test purpose.
        # or we should provide the correct ugrid file in test code.
        mesh.UploadMesh(meshId, abspath('./data/cylinder.cgns'))
        meshInfo = GetMeshInfo(meshId)
        fileName = GetMeshFileName(meshInfo['meshFormat'],
                                   meshInfo['meshEndianness'], meshInfo['meshCompression'])
        DownloadVolumeMesh(meshId, targetDir=meshId)
        self.assertTrue(exists(os.path.join(meshId, fileName)))
        DeleteMesh(meshId)
        deleteDir(meshId)

    def test_DownloadVolumeMeshWithCGNS(self):
        meshInfo = mesh.AddMesh('cylinder.cgns', 'volumeMesh.cgns', ["fluid/wall"], ['tag1'], 'cgns', '')
        meshId = meshInfo['meshId']
        mesh.UploadMesh(meshId, abspath('../tests/data/cylinder.cgns'))
        meshInfo = GetMeshInfo(meshId)
        fileName = GetMeshFileName(meshInfo['meshFormat'],
                                   meshInfo['meshEndianness'], meshInfo['meshCompression'])
        DownloadVolumeMesh(meshId, targetDir=meshId)
        self.assertTrue(exists(os.path.join(meshId, fileName)))
        DeleteMesh(meshId)
        deleteDir(meshId)

def suiteCheckNewSubmission():
    suite = unittest.TestSuite()
    suite.addTest(TestMesh('test_DeleteMesh'))
    suite.addTest(TestMesh('test_AddMeshWithJsonCGNS'))
    suite.addTest(TestMesh('test_AddMeshWithJsonUgrid'))
    suite.addTest(TestMesh('test_NewMeshWithNoSlipWalls'))
    suite.addTest(TestMesh('test_AddMeshUploadMesh'))
    suite.addTest(TestMesh('test_DownloadVolumeMeshWithZip'))
    suite.addTest(TestMesh('test_DownloadVolumeMeshWithUgrid'))
    suite.addTest(TestMesh('test_DownloadVolumeMeshWithCGNS'))
    return suite

def suiteCheckPreviousSubmission():
    suite = unittest.TestSuite()
    suite.addTest(TestMesh('test_ListMeshes'))
    suite.addTest(TestMesh('test_getFileCompression'))
    suite.addTest(TestMesh('test_getMeshInfo'))
    suite.addTest(TestMesh('test_downloadMeshProcCustomTarget'))
    suite.addTest(TestMesh('test_downloadMeshProcDefaultTarget'))
    suite.addTest(TestMesh('test_downloadVolumeMeshCustomTarget'))
    return suite

if __name__ == '__main__':
    checkAuthDir()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--testClientSubmission', default=False, action='store_true')
    args = parser.parse_args()

    runner = unittest.TextTestRunner()
    runner.run(suiteCheckPreviousSubmission())

    if args.testClientSubmission:
        runner.run(suiteCheckNewSubmission())
