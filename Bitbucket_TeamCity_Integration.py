
#######################################################
'''
Auto Trigger TeamCity testcases based on micro-services
This will read the pull requests in bitbucket , trigger the buids in teamcity and then will comment in the Bbucket PR.
This code needs Regression.json file to work.

-----------------
ksahil1993@gmail.com
'''
#######################################################
import json
import requests
import re

user = 'add here'
pwd = 'add here'
auth=(user, pwd)

log = 'FALSE'


# pr = sys.argv[1].split('/')[0]
pr = '17096'
print('PR is -> ',pr)


target_branch_master = 'master'
target_branch_release_52 = 'release/15.2'

OnGoing_Rel = [target_branch_master, target_branch_release_52]

upgrades = {target_branch_master: {'UpgradeTests_UpgradeFr_16', 'UpgradeTests_UFr_17'},
            target_branch_release_52:{'UpgradeTests_Upgrade','UpgradeTests_Upgradr_16'}
            }

upgrade_eligible = ["/az-tron:","/submarine:","/commis:","/prting:","/geored:","/divery:","/prfg:"]


components = ['list of microservices']

Reg_suitey = '52Regressionsuite'

url_b = 'https://bitbucket.abc.com/rest/api/1.0/projects/BP_az_SERVICES/repos/az-solution/pull-requests/'
url = 'https://teamcity.abc.com/blueplanet/app/rest/'
target_b_url = url_b+pr
diff_url_b = url_b+pr+"/diff"
headers = {'Content-Type': 'application/json'}
queued = []
running = []
images_changed = []




rel_branch = requests.get(diff_url_b, auth=auth)
diff = str(rel_branch.json()['diffs'])

temp_target_branch = requests.get(target_b_url, auth=auth)
target_branch = str(temp_target_branch.json()['toRef']['id'])
target_branch = target_branch.replace("refs/heads/","")
print(target_branch)

for component in components:
    if re.search(component + '*', diff, re.IGNORECASE):
        images_changed.append(component)


if log == 'TRUE':
    print('log : images_changed',images_changed,'\n','\n','\n')


data_ = ['buildQueue','builds?locator=running:true']
for item in data_:
    data = item
    url_new = url + data
    r = requests.get(url_new, auth=auth)
    process = r.text
    process = process.split('"/>')

    for elem in process:
        if re.search(pr, elem):
            #print(elem)
            if item in ("buildQueue"):
                queued.append(elem)
            else:
                running.append(elem)

if log == 'TRUE':
    print('queue->',queued,'\n''running-->',running,'\n','\n')

reg_out = []

Regression = ['51Regressionsuite','ZExperiments_AtT_3','RegressionBackupRe','L0FixedServices',
              'L0mrSnc','L0pSnc','L1Provision','L1Provision','L1otnServices','L1Services','ZExperiments_L154x',
              'ZExperiments_L1o_2','RegressionL2Bharti','NsiL2Regression','Regression8700','L2tdmServices',
              'ZExperiments_L2Tun','L3vpnServices','Regression6500neBa','RegressionPacketFa','RegressionOther',
              'Verizon','50RegressionSumm_2','UpgradeNoDevicesFrom5','UpgradeNoDevicesFr_16']


for component in Regression:
    run = str(running+queued)
    if re.search(component + '*', run, re.IGNORECASE):
        reg_out.append(component)

print('component (images_changed) -',  images_changed , 'with PR number -', pr)
print('Running/queued regressions -',reg_out)


with open('Regressions.json') as file:
    data = json.load(file)
to_run = []

if len(images_changed) > 1:
    for component in images_changed:
        for reg in data['images']:
            if reg['name'] in component:
                to_run.extend(reg['run'])

else:
    for reg in data['images']:
        if reg['name'] in images_changed:
            to_run.extend(reg['run'])

if re.search(Reg_suitey,str(to_run)):
    to_run.clear()
    to_run.append(Reg_suitey)

for index in range (0,len(images_changed)):
    component = images_changed[index]
    if component in upgrade_eligible:
        if target_branch_release_52 in target_branch:
            to_run.extend(upgrades[target_branch_release_52])
        else:
            to_run.extend(upgrades[target_branch_master])
        break


for running_regressions in reg_out:
    for regression in to_run:
        if running_regressions in regression:
            to_run.remove(regression)

to_run = list(set(to_run))  
print('to run-->',to_run)


def trigger (reg_new):
    url = 'https://teamcity.abc.com/blueplanet/app/rest/buildQueue'
    template = '<build branchName="'+pr+'/from"><buildType id="BluePlanet_azServices_azSolutionazSolution_'+reg_new+'"/></build>'
    headers = {'Content-Type': 'application/xml'}
    data = template
    r = requests.post(url, headers=headers, data=data, auth=(user, pwd), timeout=10)
    print(reg_new,r.status_code)

if target_branch in OnGoing_Rel:
  for regression in to_run:
    trigger(regression)
else:
  print('Target branch is :', target_branch,' skipping regression.')
 

def comment (message):
    # data =  '{"text":"part of Automation "}'
    dataC =  "'"+'{"text"'+':'+'"'+message+'"'+"}'"
    headers = {'Content-Type': 'application/json'}
    url = url_b+pr+'/comments'
    r = requests.post(url, headers=headers, data=dataC, auth=(user, pwd), timeout=10)
