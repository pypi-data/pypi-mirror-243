import sys
import os

import unittest
from time import sleep
import argparse
from testUtils import checkAuthDir, timeNow

testDir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.dirname(testDir))
import flow360client
assert(os.path.dirname(flow360client.__file__) == os.path.abspath(os.path.join(testDir,'..','flow360client')))
from flow360client.mesh import GetMeshInfo, DownloadMeshingLogs
from flow360client.version import __version__
from flow360client import NewMeshFromSurface, NewSurfaceMesh, NewSurfaceMeshFromGeometry
from flow360client.surfaceMesh import *

def abspath(fname):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fname))


version = f'release-{__version__}'
testBatchId = str(int(time.time()))


class TestSurfaceMesh(unittest.TestCase):

    def waitForStatus(self, resourceId, allowedStatus, finalStatus, checkFunc, statusTrigger=None):
        print('wait for status...')
        while (True):
            meshInfo = checkFunc()
            print(f'{timeNow()}: the current status {resourceId} is {meshInfo["status"]}')
            meshStatus = meshInfo['status']
            if type(finalStatus) == str and meshStatus == finalStatus:
                break
            if type(finalStatus) == list and meshStatus in finalStatus:
                break

            if statusTrigger is not None and meshStatus in statusTrigger:
                statusTrigger[meshStatus]()
            self.assertIn(meshStatus, allowedStatus)
            sleep(5)

    def waitForSurfaceMeshStatusAndAssert(self, meshId, allowedStatus, finalStatus, statusTrigger=None):
        self.waitForStatus(meshId, allowedStatus, finalStatus, lambda: GetSurfaceMeshInfo(meshId), statusTrigger)

    def waitForVolumeMeshStatusAndAssert(self, meshId, allowedStatus, finalStatus, statusTrigger=None):
        self.waitForStatus(meshId, allowedStatus, finalStatus, lambda: GetMeshInfo(meshId), statusTrigger)

    def test_GetMeshInfo(self):
        meshName = f'{version}_test_{testBatchId}'
        tags = ['lei', 'test']
        resp = AddSurfaceMesh(meshName, tags, version, format='pw')
        meshInfo = GetSurfaceMeshInfo(resp['id'])
        print(meshInfo)
        self.assertEqual(meshName, meshInfo['name'])
        self.assertEqual('pw', meshInfo['format'])
        self.assertListEqual(tags, meshInfo['tags'], 'the tags should be matched.')

    def test_ListMeshes_And_Delete(self):
        meshName = f'{version}_test_listMeshes_{testBatchId}'
        tags = ['lei', 'test']
        mesh = AddSurfaceMesh(meshName, tags, version, format='pw')
        meshes = ListSurfaceMeshes()
        self.assertIn(meshName, [meshInfo['name'] for meshInfo in meshes],
                      'the list surface meshes should contain the new created one.')
        DeleteSurfaceMesh(mesh['id'])
        meshes = ListSurfaceMeshes()
        self.assertNotIn(meshName, [meshInfo['name'] for meshInfo in meshes],
                         'the list surface meshes should not contain the deleted created one.')

    def test_DeleteMesh(self):
        meshName = f'{version}_test_DeleteMesh_{testBatchId}'
        tags = ['lei', 'test']
        mesh = AddSurfaceMesh(meshName, tags, version, format='pw')
        DeleteSurfaceMesh(mesh['id'])
        meshInfo = GetSurfaceMeshInfo(mesh['id'])
        self.assertEqual(meshInfo['deleted'], True)
        self.assertEqual(meshInfo['status'], 'deleted')
        DeleteSurfaceMesh(meshInfo['id'])

    def test_NewSurfaceMesh(self):
        fname = abspath('data/surfaceToVolume/airplane.pw')
        meshId = NewSurfaceMesh(fname, surfaceMeshName=None, tags=[], solverVersion=version)
        meshInfo = GetSurfaceMeshInfo(meshId)
        self.assertEqual(meshInfo['status'], 'processed')

    def test_NewSurfaceMeshFromGeometry(self):
        meshName = f'{version}test_NewSurfaceMeshFromGeometry_{testBatchId}'

        fname = abspath('data/geoToSurface/airplane.csm')
        config = abspath('data/geoToSurface/test_surface.json')
        meshId = NewSurfaceMeshFromGeometry(fname, config, tags=[], surfaceMeshName=meshName, solverVersion=version, validate=True)
        self.waitForSurfaceMeshStatusAndAssert(meshId, ['processed', 'generating', 'uploaded'], 'processed')
        DownloadLogs(meshId)
        logFilePath = os.path.join(meshId, 'logs/flow360_surface_mesh.user.log')
        self.assertTrue(os.path.isfile(logFilePath) and os.access(logFilePath, os.R_OK))

    def test_NewSurfaceMeshFromGeometryWithDict(self):
        meshName = f'{version}_test_NewSurfaceMeshFromGeometryWithDict_{testBatchId}'
        fname = abspath('data/geoToSurface/airplane.csm')
        with open(abspath('data/geoToSurface/test_surface.json')) as fh:
            config = json.load(fh)
        meshId = NewSurfaceMeshFromGeometry(fname, config, tags=[], surfaceMeshName=meshName, solverVersion=version, validate=True)
        print(meshId)
        self.waitForSurfaceMeshStatusAndAssert(meshId, ['processed', 'generating', 'uploaded'], 'processed')

    def test_NewVolumeMeshFromSurface(self):
        meshName = f'{version}_test_NewVolumeMeshFromSurface_{testBatchId}'
        fname = abspath('data/surfaceToVolume/airplane.pw')
        config = abspath('data/surfaceToVolume/meshVolume.airplane.json')
        surfaceMeshId = NewSurfaceMesh(fname, tags=[], surfaceMeshName=meshName, solverVersion=version)
        self.waitForSurfaceMeshStatusAndAssert(surfaceMeshId, ['processed', 'generating', 'uploaded'], 'processed')
        meshId = NewMeshFromSurface(surfaceMeshId, config, meshName=meshName, solverVersion=version, validate=True)
        self.waitForVolumeMeshStatusAndAssert(meshId, ['uploading', 'generating', 'uploaded', 'pending'], 'uploaded')
        print(meshId)

    def test_NewVolumeMeshFromGeometry(self):
        meshName = f'{version}_test_NewVolumeMeshFromGeometry_{testBatchId}'
        fname = abspath('data/geoToSurface/airplane.csm')
        config = abspath('data/geoToSurface/test_surface.json')
        surfaceMeshId = NewSurfaceMeshFromGeometry(fname, geometryToSurfaceMeshJson=config, tags=[], surfaceMeshName=meshName,
                                                   solverVersion=version, validate=True)
        self.waitForSurfaceMeshStatusAndAssert(surfaceMeshId, ['processed', 'generating', 'uploaded'], 'processed')
        print(surfaceMeshId)
        config = abspath('data/surfaceToVolume/meshVolume.airplane.json')
        meshId = NewMeshFromSurface(surfaceMeshId, meshName=meshName, config=config, solverVersion=version, validate=True)
        self.waitForVolumeMeshStatusAndAssert(meshId, ['pending', 'processed', 'generating', 'uploaded', 'processing'], ['processing', 'processed', 'uploaded'])
        print(meshId)
        logFilePath = 'flow360_volume_mesh.user_NewVolumeMeshFromGeometry.log'
        DownloadMeshingLogs(meshId, fileName=logFilePath)
        self.assertTrue(os.path.isfile(logFilePath) and os.access(logFilePath, os.R_OK))

    def test_NewVolumeMeshFromSurfaceWithDeleteSurfaceMeshBeforeVolumeStart(self):
        meshName = f'{version}_test_NewVolumeMeshFromSurfaceResultError_{testBatchId}'
        fname = abspath('data/geoToSurface/airplane.csm')
        config = abspath('data/geoToSurface/test_surface.json')
        surfaceMeshId = NewSurfaceMeshFromGeometry(fname, geometryToSurfaceMeshJson=config, tags=[], surfaceMeshName=meshName,
                                                   solverVersion=version, validate=True)
        print(surfaceMeshId)

        config = abspath('data/surfaceToVolume/meshVolume.airplane.json')
        meshId = NewMeshFromSurface(surfaceMeshId, meshName=meshName, config=config, solverVersion=version, validate=True)
        DeleteSurfaceMesh(surfaceMeshId)
        self.waitForVolumeMeshStatusAndAssert(meshId, ['pending', 'generating', 'uploading', 'error'], 'error')
        print(meshId)

    def test_NewVolumeMeshFromSurfaceWithDeleteSurfaceMeshWhenVolumeGenerating(self):
        meshName = f'{version}_test_NewVolumeMeshFromSurfaceResultError_{testBatchId}'
        fname = abspath('data/geoToSurface/airplane.csm')
        config = abspath('data/geoToSurface/test_surface.json')
        surfaceMeshId = NewSurfaceMeshFromGeometry(fname, geometryToSurfaceMeshJson=config, tags=[], surfaceMeshName=meshName,
                                                   solverVersion=version, validate=True)
        print(surfaceMeshId)

        config = abspath('data/surfaceToVolume/meshVolume.airplane.json')
        meshId = NewMeshFromSurface(surfaceMeshId, meshName=meshName, config=config, solverVersion=version, validate=True)
        self.waitForSurfaceMeshStatusAndAssert(surfaceMeshId, ['generating', 'uploaded', 'processed'], 'processed')

        def trigger():
            sleep(20)
            print(f'delete the surface mesh {meshId}')
            DeleteSurfaceMesh(surfaceMeshId)

        self.waitForVolumeMeshStatusAndAssert(meshId, ['generating', 'uploading', 'processing', 'processed'], ['processing', 'processed', 'uploaded'], {'generating': trigger})
        print(meshId)

def suiteCheckNewSubmission():
    suite = unittest.TestSuite()
    suite.addTest(TestSurfaceMesh('test_GetMeshInfo'))
    suite.addTest(TestSurfaceMesh('test_ListMeshes_And_Delete'))
    suite.addTest(TestSurfaceMesh('test_DeleteMesh'))
    suite.addTest(TestSurfaceMesh('test_NewSurfaceMesh'))
    suite.addTest(TestSurfaceMesh('test_NewSurfaceMeshFromGeometry'))
    suite.addTest(TestSurfaceMesh('test_NewSurfaceMeshFromGeometryWithDict'))
    suite.addTest(TestSurfaceMesh('test_NewVolumeMeshFromSurface'))
    suite.addTest(TestSurfaceMesh('test_NewVolumeMeshFromGeometry'))
    suite.addTest(TestSurfaceMesh('test_NewVolumeMeshFromSurfaceWithDeleteSurfaceMeshBeforeVolumeStart'))
    suite.addTest(TestSurfaceMesh('test_NewVolumeMeshFromSurfaceWithDeleteSurfaceMeshWhenVolumeGenerating'))

    return suite

def suiteCheckPreviousSubmission():
    suite = unittest.TestSuite()
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
