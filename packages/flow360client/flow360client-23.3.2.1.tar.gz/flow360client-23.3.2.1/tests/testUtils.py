import sys
import os
import shutil, subprocess, importlib
import importlib.util, datetime

def deleteFile(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)

def deleteDir(dirPath):
    if os.path.exists(dirPath):
        shutil.rmtree(dirPath)

def checkRequiredModules(packages):
    for pkg in packages:
        ret = importlib.util.find_spec(pkg)
        if ret == None:
            raise RuntimeError(f'{pkg} is required for running unit test, but it is not installed.')

def checkAuthDir():
    if os.getenv('FLOW360CLIENT_AUTHDIR') == None:
        raise RuntimeError('Please set FlOW360CLIENT_AUTHDIR to the testing account.')

def timeNow():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d-%H:%M:%S')


