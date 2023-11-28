import unittest
import sys
import os
import time
import argparse
import tempfile
from testUtils import checkAuthDir, timeNow

testDir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.dirname(testDir))
import flow360client
assert(os.path.dirname(flow360client.__file__) == os.path.abspath(os.path.join(testDir,'..','flow360client')))
from flow360client import case, mesh, NewMesh, NewCase

meshJsonFile = './data/volumeMesh/cylinder_mesh.json'
caseJsonFile = './data/volumeMesh/cylinder_case.json'
meshFile = './data/cylinder.cgns'

caseIdsToTest = [
        'df00915a-4db2-4e7b-92ab-f78df0b7e6f0',
    ]

class TestFlow360Case(unittest.TestCase):
    def setUp(self):
        global caseIdsToTest
        self.caseIdsToTest = caseIdsToTest

    def test_GetCaseInfo(self):
        for caseId in self.caseIdsToTest:
            caseInfo = case.GetCaseInfo(caseId)
            self.assertTrue(len(caseInfo) > 0)

    def test_ListCases(self):
        cases = case.ListCases(include_deleted=False)
        self.assertTrue(len(cases) > 0)

    def test_GetCaseResidual(self):
        for caseId in self.caseIdsToTest:
            res = case.GetCaseResidual(caseId)
            self.assertTrue(len(res) > 0)

    def test_GetCaseTotalForces(self):
        for caseId in self.caseIdsToTest:
            tf = case.GetCaseTotalForces(caseId)
            self.assertTrue(len(tf) > 0)

    def test_DownloadSurfaceVisualizationCustomTarget(self):
        with tempfile.TemporaryDirectory() as tempdir:
            for caseId in self.caseIdsToTest:
                targetFilePath = os.path.join(tempdir, caseId+'.surfViz.tar.gz')
                case.DownloadSurfaceResults(caseId, fileName=targetFilePath)
                self.assertTrue(os.path.exists(targetFilePath))
                self.assertTrue(os.path.getsize(targetFilePath) > 0)

    def test_DownloadSurfaceVisualizationDefaultTarget(self):
        for caseId in self.caseIdsToTest:
            with tempfile.TemporaryDirectory() as tempdir:
                currCwd = os.getcwd()
                os.chdir(tempdir)
                case.DownloadSurfaceResults(caseId)
                self.assertTrue(os.path.exists('surfaces.tar.gz'))
                self.assertTrue(os.path.getsize('surfaces.tar.gz') > 0)
                os.chdir(currCwd)

    def test_DownloadVolumetricResults(self):
        with tempfile.TemporaryDirectory() as tempdir:
            for caseId in self.caseIdsToTest:
                targetFilePath = os.path.join(tempdir, caseId+'.volumeViz.tar.gz')
                case.DownloadVolumetricResults(caseId, fileName=targetFilePath)
                self.assertTrue(os.path.exists(targetFilePath))
                self.assertTrue(os.path.getsize(targetFilePath) > 0)

    def test_DownloadSolver(self):
        with tempfile.TemporaryDirectory() as tempdir:
            for caseId in self.caseIdsToTest:
                targetFilePath = os.path.join(tempdir, caseId+'.log')
                case.DownloadSolverOut(caseId, fileName = targetFilePath)
                self.assertTrue(os.path.exists(targetFilePath))
                self.assertTrue(os.path.getsize(targetFilePath) > 0)

    def test_DownloadCSV(self):
        with tempfile.TemporaryDirectory() as tempdir:
            for caseId in self.caseIdsToTest:
                for csvType in ['nonlinear_residual_v2','total_forces_v2']:
                    targetFilePath = os.path.join(tempdir, caseId+csvType+'.csv')
                    case.DownloadResultsFile(caseId, src=csvType+'.csv',\
                        target=targetFilePath)
                    self.assertTrue(os.path.exists(targetFilePath))
                    self.assertTrue(os.path.getsize(targetFilePath) > 0)

    def test_GetCaseSurfaceForcesByNames(self):
        for caseId in self.caseIdsToTest:
            surfaces = case.GetCaseSurfaceForcesByNames(caseId)
            self.assertTrue(len(surfaces.keys())>0)

def suiteCheck():
    suite = unittest.TestSuite()
    suite.addTest(TestFlow360Case('test_GetCaseInfo'))
    suite.addTest(TestFlow360Case('test_ListCases'))
    suite.addTest(TestFlow360Case('test_GetCaseResidual'))
    suite.addTest(TestFlow360Case('test_GetCaseTotalForces'))
    suite.addTest(TestFlow360Case('test_DownloadSurfaceVisualizationCustomTarget'))
    suite.addTest(TestFlow360Case('test_DownloadSurfaceVisualizationDefaultTarget'))
    suite.addTest(TestFlow360Case('test_DownloadVolumetricResults'))
    suite.addTest(TestFlow360Case('test_DownloadSolver'))
    suite.addTest(TestFlow360Case('test_DownloadCSV'))
    suite.addTest(TestFlow360Case('test_GetCaseSurfaceForcesByNames'))
    return suite

if __name__ =='__main__':
    checkAuthDir()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--testClientSubmission', default=False, action='store_true')
    args = parser.parse_args()
    
    caseIdNew = None
    if args.testClientSubmission:
        meshIdNew = NewMesh(fname=meshFile, meshJson=meshJsonFile, tags=['integration_test_case'])
        caseIdNew = NewCase(meshId=meshIdNew, config=caseJsonFile, caseName='cylinder_case', priority='high')
        print('caseIdNew = {}'.format(caseIdNew))
        caseIdsToTest += [caseIdNew]

    completed = [False]*len(caseIdsToTest)
    while not all(completed):
        for index, caseId in enumerate(caseIdsToTest):
            caseInfo = case.GetCaseInfo(caseId)
            caseStatus = caseInfo['caseStatus']
            if caseStatus == 'completed':
                completed[index] = True
            else:
                print(f'{timeNow()}: The case {caseId} status is {caseStatus}')
        time.sleep(10)
    runner = unittest.TextTestRunner()
    runner.run(suiteCheck())
    if caseIdNew is not None:
        case.DeleteCase(caseIdNew)
