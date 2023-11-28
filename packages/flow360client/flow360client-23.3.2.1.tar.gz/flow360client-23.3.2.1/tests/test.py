#!/usr/bin/env python3
import subprocess
import sys
import os
import argparse, platform

from testUtils import checkRequiredModules, checkAuthDir

testTargetsOnAllOS = [
        'test_case.py',
        'test_mesh.py',
        'test_getAPIAuthentication.py',
        'testReadJson.py',
        'test_surface_mesh.py',
        'testVersionCompare.py',
        ]

testTargetsUsingH5py = [
        'testValidateSingleBlockCgns.py',
        'testValidateTwoBlockCgns.py',
        'testValidateSingleBlockCgns_v1.py',
        ]

targetsContainSubmission = [
        'test_case.py',
        'test_mesh.py',
        'test_surface_mesh.py',
        ]

testDir = os.path.dirname(os.path.abspath(__file__))

def monitorPopenObject(popenObj):
    while True:
        output = popenObj.stdout.readline().decode()
        if output == '' and popenObj.poll() != None:
            break
        if output:
            print(output.strip())
    retcode = popenObj.poll()
    if retcode != 0:
        print(popenObj.stderr.readlines())
    return retcode

if __name__ == '__main__':
    print(sys.executable)
    print(*sys.path, sep='\n')
    checkAuthDir()
    testTargetsToRun = list()
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        checkRequiredModules(['h5py'])
        testTargetsToRun = testTargetsOnAllOS + testTargetsUsingH5py
    elif platform.system() == 'Windows':
        testTargetsToRun = testTargetsOnAllOS
    else:
        raise RuntimeError('Unrecognized platform.')

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--testClientSubmission', default=False, action='store_true')
    args = parser.parse_args()
    processes = dict()

    for target in testTargetsToRun:
        print('testing {}'.format(target))
        cmd = [sys.executable, '-u', os.path.join(testDir, target)]

        if args.testClientSubmission and target in targetsContainSubmission:
            cmd += ['--testClientSubmission']

        proc = subprocess.Popen(
            cmd,
            env={**os.environ},
            cwd=testDir,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
            )
        processes[target]=proc

    for target in processes:
        print('checking test: {}'.format(target))
        returncode = monitorPopenObject(processes[target])
        assert returncode == 0
        print('{} passes.'.format(target))

