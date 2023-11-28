import json
import os
import time

from .authentication import refreshToken
from .config import Config
from .httputils import flow360ApiPost, flow360ApiGet, flow360ApiDelete
from .s3utils import S3TransferType
from .errorHandling import deprecated 
from .validation import validateJSON

auth = Config.auth
keys = Config.user

@refreshToken
def AddMeshWithJson(name, remoteFileName, mesh_json, tags, fmat, endianness, compression=None, solver_version=None):
    return AddMeshBase(name, remoteFileName, mesh_json, tags, fmat, endianness, compression, solver_version)


@refreshToken
def AddMesh(name, remoteFileName, noSlipWalls, tags, fmat, endianness, compression=None, solver_version=None):
    return AddMeshBase(name, remoteFileName, {
        "boundaries":
            {
                "noSlipWalls": noSlipWalls
            }
    }, tags, fmat, endianness, compression, solver_version)

def AddMeshBase(name, remoteFileName, meshParams, tags, fmat, endianness, compression, solver_version):
    '''
       AddMesh(name, noSlipWalls, tags, fmat, endianness, version)
       returns the raw HTTP response
       {
           'meshId' : 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
           'addTime' : '2019:01:01:01:01:01.000000'
       }
       The returned meshId is need to subsequently call UploadMesh
       Example:
           resp = AddMesh('foo', [1], [], 'aflr3', 'big')
           UploadMesh(resp['meshId'], 'mesh.lb8.ugrid')
       '''

    body = {
        "fileName": remoteFileName,
        "meshName": name,
        "meshTags": tags,
        "meshFormat": fmat,
        "meshEndianness": endianness,
        "meshCompression": compression,
        "meshParams": json.dumps(meshParams)
    }

    if solver_version:
        body['solverVersion'] = solver_version

    resp = flow360ApiPost("volumemeshes", data=body)
    return resp

def validateVolumeMeshJSON(config, solverVersion=None):
        return validateJSON('volumemesh', config, solverVersion=solverVersion)

@refreshToken
def GenerateMeshFromSurface(name, config, surfaceMeshId, tags, solver_version,
        validate):
    if validate:
        validateVolumeMeshJSON(json.dumps(config), solver_version)
    body = {
        "name": name,
        "tags": tags,
        "surfaceMeshId": surfaceMeshId,
        "config": json.dumps(config),
        "format": 'cgns'
    }

    if solver_version:
        body['solverVersion'] = solver_version

    resp = flow360ApiPost("volumemeshes", data=body)
    return resp


@refreshToken
def DeleteMesh(meshId):
    resp = flow360ApiDelete(f"volumemeshes/{meshId}")
    return resp


@refreshToken
def GetMeshInfo(meshId):
    url = f"volumemeshes/{meshId}"
    resp = flow360ApiGet(url)
    meshParams = None 
    try:
        meshParams = json.loads(resp['meshParams'])
    except Exception as e:
        pass
    resp['meshParams'] = meshParams
    return resp

@refreshToken
def CompleteVolumeMeshUpload(meshId, fileName):
    url = f"volumemeshes/{meshId}/completeUpload?fileName={fileName}"
    resp = flow360ApiPost(url)
    return resp


@refreshToken
def ListMeshes(include_deleted=False):
    resp = flow360ApiGet("volumemeshes", params={"includeDeleted": include_deleted})
    return resp


def MeshFileNameBreakdown(fileName, fmat=None, endianness=None):
    if fmat is None:
        if fileName.endswith('.ugrid') or fileName.endswith('.ugrid.gz') or \
                fileName.endswith('.ugrid.bz2'):
            fmat = 'aflr3'
        elif fileName.endswith('.cgns') or fileName.endswith('.cgns.gz') or \
                fileName.endswith('.cgns.bz2'):
            fmat = 'cgns'
        else:
            raise RuntimeError('Unknown format for file {}'.format(fileName))

    if fmat == 'aflr3' and endianness is None:
        if fileName.find('.b8.') != -1:
            endianness = 'big'
        elif fileName.find('.lb8.') != -1:
            endianness = 'little'
        else:
            raise RuntimeError('Unknown endianness for file {}'.format(fileName))
    else:
        endianness = ''

    compression = ''
    if fileName.endswith('.gz'):
        compression += 'gz'
    elif fileName.endswith('.bz2'):
        compression += 'bz2'

    return fmat, endianness, compression

@refreshToken
def GetRemoteMeshFileName(localMeshFileName=None, meshId=None):

    if localMeshFileName is not None:
        fmat, endianness, compression = MeshFileNameBreakdown(localMeshFileName)
        remoteFileName = GetMeshFileName(fmat, endianness, compression)

        return remoteFileName, fmat, endianness, compression
    
    if meshId is not None:
        remoteFiles = flow360ApiGet(f"volumemeshes/{meshId}/files")
        remoteFileName = None
        for file in remoteFiles:
            try:
                fmat, endianness, compression = MeshFileNameBreakdown(file['fileName'])
                return file['fileName'], fmat, endianness, compression
            except RuntimeError:
                continue

        if remoteFileName is None:
            raise RuntimeError(f"No volume mesh file found for id={meshId}")
        
    raise ValueError('You need to provide localMeshFileName OR meshId')


@refreshToken
def UploadMesh(meshId, localMeshFileName, remoteMeshFileName):
    '''
    UploadMesh(meshId, meshFile)
    '''

    S3TransferType.VolumeMesh.upload_file(meshId, remoteMeshFileName, localMeshFileName)
    CompleteVolumeMeshUpload(meshId, remoteMeshFileName)

def DownloadVolumeFile(id, src, target):
    S3TransferType.VolumeMesh.download_file(id, src, target)

@refreshToken
@deprecated("DownloadMeshGenerationConfigJson()")
def DownloadMeshConfigJson(id, fileName=None):
    if fileName is None:
        fileName = 'config.json'
    DownloadVolumeFile(id, 'config.json', fileName)

@refreshToken
def DownloadMeshGenerationConfigJson(id, fileName=None):
    if fileName is None:
        fileName = 'volumeMeshGenerationConfig.json'
    DownloadVolumeFile(id, 'config.json', fileName)

def DownloadMeshProc(meshId, fileName=None):
    logFileName = 'logs/flow360_volume_mesh.user.log'
    if fileName is None:
        fileName = os.path.basename(logFileName)
    DownloadVolumeFile(meshId, src=logFileName, target=fileName)

def DownloadMeshingLogs(id, fileName=None):
    DownloadMeshProc(id, fileName)

def GetMeshFileName(meshFormat, endianness, compression):
    if meshFormat == 'aflr3':
        if endianness == 'big':
            name = 'mesh.b8.ugrid'
        elif endianness == 'little':
            name = 'mesh.lb8.ugrid'
        else:
            raise RuntimeError("unknown endianness: {}".format(endianness))
    else:
        name = "volumeMesh" + '.' + meshFormat

    if compression is not None and len(compression) > 0:
        name += '.' + compression
    return name

def DownloadVolumeMesh(id, target=None, targetDir=None):
    remoteFileName, _, _, _ = GetRemoteMeshFileName(meshId=id)

    if target is None:
        meshName = os.path.basename(remoteFileName)
        if targetDir is None:
            target = os.path.join(os.getcwd(), meshName)
        else:
            target = os.path.join(targetDir, meshName)

    DownloadVolumeFile(id, remoteFileName, target)

def WaitOnMesh(meshId, timeout=86400, sleepSeconds=10):
    startTime = time.time()
    while time.time() - startTime < timeout:
        try:
            info = GetMeshInfo(meshId)
            if info['meshStatus'] in ['deleted', 'error', 'preerror', 'unknownError', 'processed']:
                return info['meshStatus']
        except Exception as e:
            print('Warning : {0}'.format(str(e)))

        time.sleep(sleepSeconds)


def getFileCompression(name):
    if name.endswith("tar.gz"):
        return 'tar.gz'
    elif name.endswith(".gz"):
        return 'gz'
    elif name.endswith("bz2"):
        return 'bz2'
    else:
        return None

