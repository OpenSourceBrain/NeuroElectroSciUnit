'''
API to OSB tests using restkit...
'''

from restkit import Resource
res = Resource('http://www.opensourcebrain.org')

import json

projects = res.get('/projects.json', limit=1000)


jp = json.loads(projects.body_string())

neurolex_id_field = 'NeuroLex Ids: Cells'

def printCustomField(project, cfName, info):
    for cf in project["custom_fields"]:
        if cf['name'] == cfName and cf.has_key('value'):  
            if cfName == neurolex_id_field:
                info += cf['value']+"  "
            else:
                info += ""
    return info

info = ""

for project in jp["projects"]:

    isProj = False
    hasids = False
    for cf in project["custom_fields"]:
        if cf['name'] == 'Category' and cf.has_key('value') and cf['value']=='Project':
            isProj = True
        if cf['name'] == neurolex_id_field and cf.has_key('value') and len(cf['value'])>0:
            hasids = True
    
    if isProj:

        url = "http://opensourcebrain.org/projects/%s"%project["identifier"]
        info += "\n%s: "%url
        for i in range(100-len(url)):
            info += " "
        
        if hasids:
            info = printCustomField(project, neurolex_id_field, info)
        else:
            info += ""

print info

