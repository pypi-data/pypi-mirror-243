from time import sleep

from flow360client import mesh, NewCase, Config, ChooseAccount, case

ChooseAccount()
resp = mesh.AddMesh('OM6_Wing_Tetra', 'mesh.lb8.ugrid.gz', [1], ['OM6','flow360-no-cleanup'], 'aflr3', 'little', 'gz')
print(resp)
meshId = resp['meshId']
print(meshId)
#
mesh.UploadMesh(meshId, 'data/wing_tetra.1.lb8.ugrid.gz')
resp = mesh.GetMeshInfo(meshId=meshId)
print(resp)

resp = mesh.ListMeshes()
print(resp)


# meshId = 'd67ebdc1-8cd2-444f-8fae-0d4389eccb40'
caseId = NewCase(meshId=meshId, config='data/wing_tetra.1.json', caseName='case2_unittest', tags=['test1'],
            priority='high', parentId=None)

while True:
    caseDetail = case.GetCaseInfo(caseId)
    if caseDetail['caseStatus'] == 'completed':
        break
    else:
        print(f"the current case status is {caseDetail['caseStatus']}, wait for completed...")
        sleep(15)

case.DownloadSolverOut(caseId)
