# -*- coding: iso-8859-1 -*-
import requests  # @UnresolvedImport
import os
import logging
import logger
from xml.sax.saxutils import escape
import cgi
import datetime
from HTMLParser import HTMLParser

log = logger.log()
os.environ['no_proxy'] = '127.0.0.1,localhost,148.110.107.37'
debug = False
from xml.dom.minidom import Text, Element
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

from xml.etree import ElementTree as ET

# response = requests.get(url)

# tree = ElementTree.fromstring(response.content)

class otXml():
    
    def __init__(self):
        self.wsUrl = "http://148.110.107.37/otws/v1.asmx"
        self.xml = ""
        self.headers = ""
        self.body = ""
        self.command = ""  # AddObject ModifyObject GetObjectList
        self.operation = ""
        self.startTime = datetime.datetime.now()
        self.endTime = ""
        
        
    
        
                       
    def initQuery(self, command):
        self.headers = {'Content-Type': 'text/xml', 'charset':'iso-8859-1', 'SOAPAction' : '"http://www.omninet.de/OtWebSvc/v1/%s"' % (command)}
        self.xml = r'<?xml version="1.0" encoding="iso-8859-1"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' + \
        r'xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' + \
        r'xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Body>' + \
        r'<%s xmlns="http://www.omninet.de/OtWebSvc/v1">' % (command) + \
        r'%s</%s></soap:Body></soap:Envelope>' % (self.body, command)
        


    def addEvent(self, InternalID):
        
        self.body = r'%s<Object folderPath="01. ITSM - Service Operation\01. Event Management">' % (self.body) + \
        r'<StringVal name="UCID">%s</StringVal></Object>' % (InternalID)
        self.initQuery("AddObject")
        self.operation = "Adding Event with Internal ID : %s" % InternalID
        return self.sendQuery()
    
    def addIncident(self, Title, Description, UserDisplayName,CategoryID, Solution):
        
        self.body = r'%s<Object folderPath="01. ITSM - Service Operation\02. Incident Management">' % (self.body) + \
        r'<StringVal name="Title">%s</StringVal>' % (Title) + \
        r'<StringVal name="Description">%s</StringVal>' % (repr(Description)) + \
        r'<StringVal name="SolutionDescription">%s</StringVal>' % (Solution) + \
        r'<RefToUserVal name="Applicant">%s</RefToUserVal>' % (UserDisplayName) + \
        r'<RefToUserVal name="Responsible">%s</RefToUserVal>' % (UserDisplayName) + \
        r'<ReferenceVal name="AssociatedCategory" objectId ="%s"/></Object>' % (CategoryID)
       
        self.initQuery("AddObject")
        self.operation = "Adding Incident with Internal ID" 
        return self.sendQuery()
		
    def addIncident_rawDesc(self, Title, Description, UserDisplayName,CategoryID, Solution):
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
    
    def modifyTicket(self, type, object, key, value):
        self.body = r'%s<Object objectId="%s">' % (self.body, object) + \
            r'<%s name="%s">%s</%s>' % (type, key, value, type) + \
            r'</Object>'
        self.initQuery("ModifyObject")
        self.operation = "Modifying " + type + " ID: " + object + ", field " + key + " with value :" + value 
        #print self.xml
        return self.sendQuery() 
    
    def modifyRefValTicket(self, object, key, value):
        self.body = r'%s<Object objectId="%s">' % (self.body, object) + \
            r'<ReferenceVal name="%s" objectId="%s" />' % (key, value) + \
            r'</Object>'
        self.initQuery("ModifyObject")
        self.operation = "Modifying ID: " + object + ", field " + key + " with value :" + value 
        #print self.xml
        return self.sendQuery() 
    
    
    def modifyEvent(self, type, object, key, value):
        self.body = r'%s<Object objectId="%s">' % (self.body, object) + \
            r'<%s name="%s">%s</%s>' % (type, key, value, type) + \
            r'</Object>'
        self.initQuery("ModifyObject")
        # print self.xml
        self.operation = "Modifying " + type + " ID: " + object + ", field " + key + " with value :" + value 
        return self.sendQuery() 
    
    def modifyEventString(self, object, key, value):
        self.body = r'%s<Object objectId="%s">' % (self.body, object) + \
            r'<StringVal name="%s">%s</StringVal>' % (key, value) + \
            r'</Object>'
        self.initQuery("ModifyObject")
        self.operation = "Modifying String for Event ID: " + object + ", field " + key + " with value :" + value 
        return self.sendQuery()
    
    
    def modifyTicketRef(self, type, object, key, value):
        
        self.body = r'%s<Object objectId="%s">' % (self.body, object) + \
            r'<ReferenceToUserVal name="%s" type="%s" Value="%s" />' % (key, type, value) + \
            r'</Object>'
        self.initQuery("ModifyObject")
        self.operation = "Modifying Reference for Event ID: " + object + ", field " + key + " with value :" + value + " type :" + type
        
        return self.sendQuery()
    
    def modifyEventRef(self, type, object, key, value):
        
        self.body = r'%s<Object objectId="%s">' % (self.body, object) + \
            r'<ReferenceToUserVal name="%s" type="%s" Value="%s" />' % (key, type, value) + \
            r'</Object>'
        self.initQuery("ModifyObject")
        self.operation = "Modifying Reference for Event ID: " + object + ", field " + key + " with value :" + value + " type :" + type
        
        return self.sendQuery()
    
    def queryObjects(self, folder, requiredFields):
        
        # "00. MasterData\05. People\05.1 Persons\User Accounts"
        self.body = r'%s<Get folderPath="%s" recursive="true">' % (self.body, folder)
        for requiredField in requiredFields:
            r'<RequiredField>%s</RequiredField>' % (requiredField)
        self.body = "%s</Get>" % (self.body)
                   # r'<RequiredField>Number</RequiredField><RequiredField>Phone</RequiredField><RequiredField>Email Address</RequiredField></Get>
        self.initQuery("GetObjectList")
        # print self.xml
        self.operation = "query objects list for folder " + folder + " with fields " + "%s" % requiredFields
        return self.sendQuery()
    
    
    def queryObjectsBuildInFilter(self,filtername, folder, requiredFields, isRecursive):
        self.body = r'%s<Get folderPath="%s" recursive="%s"><Filter>%s</Filter>' % (self.body, folder, isRecursive, filtername)
        for requiredField in requiredFields:
            r'<RequiredField>%s</RequiredField>' % (requiredField)
        self.body = "%s</Get>" % (self.body)
                   # r'<RequiredField>Number</RequiredField><RequiredField>Phone</RequiredField><RequiredField>Email Address</RequiredField></Get>
        self.initQuery("GetObjectList")
        self.operation = "query objects list for folder " + folder + " with fields " + "%s" % requiredFields + "Filter id : " 
        #print self.xml
        return self.sendQuery()
    
    def queryObjectsFilter(self, filtername, varname, folder, requiredFields, isRecursive, value, varType):
        
        # "00. MasterData\05. People\05.1 Persons\User Accounts"
 

 
        self.body = r'%s<Get folderPath="%s" recursive="%s"><Filter>%s<%s name="%s">%s</%s></Filter>' % (self.body, folder, isRecursive, filtername, varType,varname, value, varType)
        for requiredField in requiredFields:
            r'<RequiredField>%s</RequiredField>' % (requiredField)
        self.body = "%s</Get>" % (self.body)
                   # r'<RequiredField>Number</RequiredField><RequiredField>Phone</RequiredField><RequiredField>Email Address</RequiredField></Get>
        self.initQuery("GetObjectList")
        self.operation = "query objects list for folder " + folder + " with fields " + "%s" % requiredFields + "Filter id : " 
        #print self.xml
        return self.sendQuery()
    
    def queryObjectsFilterUCID(self, folder, requiredFields, UCID):
        
        # "00. MasterData\05. People\05.1 Persons\User Accounts"
        self.body = r'%s<Get folderPath="%s" recursive="true"><Filter>EventUCID<StringVal name="UCID">%s</StringVal></Filter>' % (self.body, folder, UCID)
        for requiredField in requiredFields:
            r'<RequiredField>%s</RequiredField>' % (requiredField)
        self.body = "%s</Get>" % (self.body)
                   # r'<RequiredField>Number</RequiredField><RequiredField>Phone</RequiredField><RequiredField>Email Address</RequiredField></Get>
        self.initQuery("GetObjectList")
        self.operation = "query objects list for folder " + folder + " with fields " + "%s" % requiredFields + "Filter UCID : " + UCID  
        # print self.xml
        return self.sendQuery()

    def queryObjectsFilterId(self, folder, requiredFields, id):
        
        # "00. MasterData\05. People\05.1 Persons\User Accounts"
 

 
        self.body = r'%s<Get folderPath="%s" recursive="true"><ObjectIDs objectIDs="%s"/>' % (self.body, folder, id)
        for requiredField in requiredFields:
            r'<RequiredField>%s</RequiredField>' % (requiredField)
        self.body = "%s</Get>" % (self.body)
                   # r'<RequiredField>Number</RequiredField><RequiredField>Phone</RequiredField><RequiredField>Email Address</RequiredField></Get>
        self.initQuery("GetObjectList")
        self.operation = "query objects list for folder " + folder + " with fields " + "%s" % requiredFields + "Filter id : " + id  
        # print self.xml
        return self.sendQuery()
    # <StringVal name="Priority at least">Medium</StringVal><DateTimeVal name="Due before (date)">2007-06-01T12:00:00</DateTimeVal></Filter>
        
    def plainTextQueryTest(self):
        self.headers = {'Content-Type': 'text/xml', 'charset':'UTF-8', 'SOAPAction' : '"http://www.omninet.de/OtWebSvc/v1/GetObjectList"'}  # set what your server accepts
        self.command = r'<?xml version="1.0" encoding="UTF-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Body><GetObjectList xmlns="http://www.omninet.de/OtWebSvc/v1"><Get folderPath="00. MasterData\05. People\05.1 Persons\User Accounts" recursive="true"><RequiredField>Number</RequiredField><RequiredField>Phone</RequiredField><RequiredField>Email Address</RequiredField></Get></GetObjectList></soap:Body></soap:Envelope>'
        # self.buildXmlQuery()
        self.xml = self.command
        
        return self.sendQuery()
	
    def plainTextQueryTestAddTicket(self):
               
        test=u'test avec accents é è'
        
        #test = cgi.escape(test)
        test = test.encode("ascii", "xmlcharrefreplace")
        
		
        self.headers = {'Content-Type': 'text/xml', 'charset':'iso-8859-1', 'SOAPAction' : '"http://www.omninet.de/OtWebSvc/v1/AddObject"'}  # set what your server accepts
        self.command = r'<?xml version="1.0" encoding="iso-8859-1"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Body>' + \
                        r'<AddObject xmlns="http://www.omninet.de/OtWebSvc/v1">' + \
                        r'<Object folderPath="01. ITSM - Service Operation\02. Incident Management">' + \
                        r'<StringVal name="Title">Number</StringVal>' + \
                        r'<StringVal name="Source">Internal Issues</StringVal>' + \
                        r'<StringVal name="Description">%r</StringVal>' % test + \
                        r'<ReferenceVal name="AssociatedCategory" objectId="706057" />' + \
                        r'<ReferenceToUserVal name="Applicant" type="userloginname" Value="lju" />' + \
                        r'</Object></AddObject>' + \
                        r'</soap:Body></soap:Envelope>'
        # self.buildXmlQuery()
        self.xml = self.command
        self.sendQuery()
        
    def plainTextQueryTestAddEvent(self):
        self.headers = {'Content-Type': 'text/xml', 'charset':'UTF-8', 'SOAPAction' : '"http://www.omninet.de/OtWebSvc/v1/AddObject"'}  # set what your server accepts
        self.command = r'<?xml version="1.0" encoding="UTF-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Body>' + \
                        r'<AddObject xmlns="http://www.omninet.de/OtWebSvc/v1">' + \
                        r'<Object folderPath="01. ITSM - Service Operation\01. Event Management">' + \
                        r'<StringVal name="Title">Number</StringVal>' + \
                        r'<StringVal name="Source">Call Incoming</StringVal>' + \
                        r'<ReferenceToUserVal name="Applicant" type="userloginname" Value="Lebourg Julien" />' + \
                        r'</Object></AddObject>' + \
                        r'</soap:Body></soap:Envelope>'
        # self.buildXmlQuery()
        self.xml = self.command
        self.sendQuery()
        
    def plainTextQueryTestAddEventModify(self):
        self.headers = {'Content-Type': 'text/xml', 'charset':'UTF-8', 'SOAPAction' : '"http://www.omninet.de/OtWebSvc/v1/ModifyObject"'}  # set what your server accepts
        self.command = r'<?xml version="1.0" encoding="UTF-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Body>' + \
                        r'<ModifyObject  xmlns="http://www.omninet.de/OtWebSvc/v1">' + \
                        r'<Object objectId="947699">' + \
                        r'<ReferenceToUserVal name="Applicant" type="userloginname" Value="Lebourg Julien" />' + \
                        r'</Object></ModifyObject>' + \
                        r'</soap:Body></soap:Envelope>'
        # self.buildXmlQuery()
        self.xml = self.command
        result = self.sendQuery()
        
        
    def buildXmlQuery(self):
        
        self.headers = {'Content-Type': 'text/xml', 'charset':'UTF-8', 'SOAPAction' : "http://www.omninet.de/OtWebSvc/v1/GetObjectList"}  # set what your server accepts
        
        openEnvelope = """<?xml version='1.0' encoding='UTF-8'?>
                   <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
                   <soap:Body>"""
                       
        closeEnvelope = """</soap:Body> </soap:Envelope>"""        
        
        self.xml = "%s %s %s" % (openEnvelope, self.command, closeEnvelope)
        
    def getAgentByExt(self, ext):
        
        
        
        
        folderPath = "00. MasterData\05. People\05.1 Persons\User Accounts"
        getObjectList = """<GetObjectList xmlns="%s">""" % (self.wsUrl)
        getFolderPath = """<Get folderPath="%s" recursive="true" username="superuser" password="adminctg">""" % (folderPath)
        getFolderPathClose = """ </Get> """ 
        getObjectListClose = """</GetObjectList>"""
        
        self.command = "%s\n%s" % (self.xml, getObjectList, getFolderPath, getFolderPathClose, getObjectListClose)
        
        self.buildXmlQuery()
        # allAgents = parseXMLResponse(self.sendQuery()) 
        
        
        
    
        



        
        
    
#===============================================================================
#     def addEvent(self, event):
#         
#         strCommand="""<AddObject xmlns="%s">""" % (self.wsUrl)
#         folderPath="01. ITSM - Service Operation\O1. Event Management"
#         #strObjectDef = """<Object folderPath="%s" fieldMapping="%s" saveExFlags="int" username="superuser" password="adminctg" />""" % ()
#         strObjectDef = """<Object folderPath="%s" username="superuser" password="adminctg" />""" % (folderPath)
#         strCloseCommand = """ </AddObject> """
#         
# 
#         
#         self.command = "%s\n%s" % (self.xml,strCommand, strObjectDef, strCloseCommand)
#      
#         
#         self.buildXmlQuery()
#         self.sendQuery()
#     
#===============================================================================
    
        
    def sendQuery(self):
        #print self.xml
        #
        if debug == True:
            print self.wsUrl
            content = ""
        else:
            #print self.wsUrl
            result = requests.post(self.wsUrl, data=self.xml, headers=self.headers)
            content = result.content
        # tree = ET.fromstring(result.content)
        # print "%s" % (tree)    
        #print result.content
        self.logresults(content)
        return content
    
    def logresults(self, content):
        if "success=\"true\"" in content:
            delay = int((datetime.datetime.now() - self.startTime).microseconds / 1000)
            log.info("success :" + self.operation + " in %s ms" % delay)
            with open("E:\\otEventsManagement\\perfdata.txt", "a") as myfile:
                myfile.write("%s;" % delay)
            #log.info(content)
        else:
            log.critical("Error on query :" + self.operation)
            print self.xml
            print content
        
        

   
        
        
        
