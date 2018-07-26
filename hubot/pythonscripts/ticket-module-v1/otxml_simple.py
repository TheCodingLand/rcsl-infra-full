# -*- coding: iso-8859-1 -*-
import requests

import platform
if platform.system()=="Windows":
    Encoding = "iso-8859-1"
else:
    Encoding = "utf-8"




#import os
#os.environ['no_proxy'] = '127.0.0.1,localhost,148.110.107.37'
debug = False

import datetime
import xml.etree.ElementTree as ET
from xml.dom.minidom import Text, Element

class otXml():
    
    def __init__(self):
        self.wsUrl = "http://otrcsl01.rcsl.lu/otws/v1.asmx"
        self.xml = "" #XML Being build for this query
        self.headers = ""
        self.body = ""
        self.command = ""  # AddObject ModifyObject GetObjectList
        self.operation = ""
        self.startTime = datetime.datetime.now()
        self.endTime = ""
        self.result = False
        self.xml_result = ""

    def initQuery(self, command):
        self.headers = {'Content-Type': 'text/xml', 'charset':'iso-8859-1', 'SOAPAction' : '"http://www.omninet.de/OtWebSvc/v1/%s"' % (command)}
        self.xml = r'<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' + \
        r'xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' + \
        r'xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Body>' + \
        r'<%s xmlns="http://www.omninet.de/OtWebSvc/v1">' % (command) + \
        r'%s</%s></soap:Body></soap:Envelope>' % (self.body, command)

    def addIncident(self, Title, Description, UserDisplayName, CategoryID, Solution):
        self.body = r'%s<Object folderPath="01. ITSM - Service Operation\02. Incident Management">' % (self.body) + \
                    r'<StringVal name="Title">%s</StringVal>' % (Title) + \
                    r'<StringVal name="Description">%s</StringVal>' % (Description) + \
                    r'<StringVal name="SolutionDescription">%s</StringVal>' % (Solution) + \
                    r'<RefToUserVal name="Applicant">%s</RefToUserVal>' % (UserDisplayName) + \
                    r'<RefToUserVal name="Responsible">%s</RefToUserVal>' % (UserDisplayName) + \
                    r'<ReferenceVal name="AssociatedCategory" objectId ="%s"/></Object>' % (CategoryID)

        self.initQuery("AddObject")
        self.operation = "Adding Incident with Internal ID"
        return self.sendQuery()

    def modifyTicketRef(self, type, object, key, value):
        self.body = r'%s<Object objectId="%s">' % (self.body, object) + \
                    r'<ReferenceToUserVal name="%s" type="%s" Value="%s" />' % (key, type, value) + \
                    r'</Object>'
        self.initQuery("ModifyObject")
        self.operation = "Modifying Reference for Event ID: " + object + ", field " + key + " with value :" + value + " type :" + type
        return self.sendQuery()

    def queryObjectsFilter(self, filtername, varname, folder, requiredFields, isRecursive, value, varType):

        # "00. MasterData\05. People\05.1 Persons\User Accounts"
        self.body = r'%s<Get folderPath="%s" recursive="%s"><Filter>%s<%s name="%s">%s</%s></Filter>' % (
        self.body, folder, isRecursive, filtername, varType, varname, value, varType)
        for requiredField in requiredFields:
            self.body = r'%s<RequiredField>%s</RequiredField>' % (self.body,requiredField)
        self.body = "%s</Get>" % (self.body)
        # r'<RequiredField>Number</RequiredField><RequiredField>Phone</RequiredField><RequiredField>Email Address</RequiredField></Get>
        self.initQuery("GetObjectList")
        self.operation = "query objects list for folder " + folder + " with fields " + "%s" % requiredFields + "Filter id : "
        # print self.xml
        return self.sendQuery()

    def queryObjects(self, folder, requiredFields):
        # "00. MasterData\05. People\05.1 Persons\User Accounts"
        self.body = r'%s<Get folderPath="%s" recursive="true">' % (self.body, folder)
        for requiredField in requiredFields:
            self.body = r'%s<RequiredField>%s</RequiredField>' % (self.body,requiredField)
        self.body = "%s</Get>" % (self.body)
        # r'<RequiredField>Number</RequiredField><RequiredField>Phone</RequiredField><RequiredField>Email Address</RequiredField></Get>
        self.initQuery("GetObjectList")
        # print self.xml
        self.operation = "query objects list for folder " + folder + " with fields " + "%s" % requiredFields
        return self.sendQuery()




    def testsuccess(self, content):
        tree = ET.fromstring(content)
        try:
            root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}ModifyObjectResult')
            #root = tree.find<ModifyObjectResult success="false" errorMsg="User not found by display name 'Julien Le Bourg'" />
            if root.attrib['success'] == "false":
                self.result = False
            else:
                self.result = True
        except:
            nomod = ""
            #print "not a modify query"
        try:
            root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}AddObjectResult')
            # root = tree.find<ModifyObjectResult success="false" errorMsg="User not found by display name 'Julien Le Bourg'" />
            if root.attrib['success'] == "false":
                self.result = False
            else:
                self.result = root.attrib['objectId']
        except:
            nomod = ""
            #print "not an addobject query"

    def modifyTicket(self, type, object, key, value):
        self.body = r'%s<Object objectId="%s">' % (self.body, object) + \
            r'<%s name="%s">%s</%s>' % (type, key, value, type) + \
            r'</Object>'
        self.initQuery("ModifyObject")
        self.operation = "Modifying " + type + " ID: " + object + ", field " + key + " with value :" + value
        #print self.xml
        return self.sendQuery()

    def queryObjectsById(self, folder, requiredFields, id):
        self.body = r'%s<Get folderPath="%s" recursive="true"><ObjectIDs objectIDs="%s"/>' % (self.body, folder, id)
        for requiredField in requiredFields:
            self.body= r'%s<RequiredField>%s</RequiredField>' % (self.body,requiredField)
        self.body = "%s</Get>" % (self.body)
        self.initQuery("GetObjectList")
        self.operation = "query objects list for folder " + folder + " with fields " + "%s" % requiredFields + "Filter id : " + id
        #print self.body
        return self.sendQuery()


    def sendQuery(self):
        #print self.xml
        #

        if debug == True:
            #print self.wsUrl
            content = ""
        else:
            #print self.wsUrl

            #repr(body).replace(r'\r\n', '&#x000d;&#x000a;')[1:-1]
            result = requests.post(self.wsUrl, data=self.xml.decode(Encoding).encode("ascii", "xmlcharrefreplace").replace(r'\r\n', '&#x000d;&#x000a;'), headers=self.headers)

            content = result.content
        # tree = ET.fromstring(result.content)
        # print "%s" % (tree)
        self.xml_result = result.content

        #print result.content
        #self.logresults(content)
        self.testsuccess(content)
        return self
