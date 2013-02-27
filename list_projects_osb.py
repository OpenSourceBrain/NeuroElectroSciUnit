'''
Some quality assurance tests on OSB/GitHub repos

'''

from restkit import Resource
import urllib
import os
import sys

import json

from lxml import etree
from urllib import urlopen



def get_custom_fields(project):

    cfs = {}
    for cf in project["custom_fields"]:
        if cf.has_key('value'):
            cfs[cf['name']] = cf['value']
    return cfs

if __name__ == "__main__":

    res = Resource('http://www.opensourcebrain.org')

    p = res.get('/projects.json', limit=1000)

    jp = json.loads(p.body_string())

    versionFolder = "NeuroML2"
    nml_schema_file = urlopen("http://neuroml.svn.sourceforge.net/viewvc/neuroml/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd")
    suffix = ".nml"


    xmlschema_doc = etree.parse(nml_schema_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    for project in jp["projects"]:
       

        status_found = 0
        github_repo = None
        category = ""
        spine_check = 0
        neurolexidscells = ""
        
        cfs = get_custom_fields(project)

        if cfs.has_key('GitHub repository'):
            github_repo = cfs['GitHub repository']
        if cfs.has_key('Status info') and len(cfs['Status info']) > 0:
            status_found = 1
        if cfs.has_key('NeuroLex Ids: Cells') and len(cfs['NeuroLex Ids: Cells']) > 0:
            neurolexidscells = cfs['NeuroLex Ids: Cells']

        category = cfs['Category'] if cfs.has_key('Category') else "???"

        if category == "Project" or category == "Showcase":

            print "\n--------   Project: %s (%s)\n"%(project["name"], github_repo)
            #if status_found:
                #print "Status: %s"%cfs['Status info']

            #print "Project hierarchy:"
            print "    %s / %s / %s / %s / %s"%(cfs['Spine classification'], cfs['Family'], cfs['Specie'], cfs['Brain region'], cfs['Cell type'])
            if len(neurolexidscells) > 0:
                print "    NeuroLex id(s) of cells: "+neurolexidscells
            
    
    print
