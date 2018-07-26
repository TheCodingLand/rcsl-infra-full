# -*- coding: iso-8859-1 -*-
import otxml_simple
import xml.etree.ElementTree as ET
import user
#import build_object


def modifyref(type, IncidentId, key, UserDisplayName):
    ot = otxml_simple.otXml()
    XmlResponse = ot.modifyTicketRef(type, IncidentId, key, UserDisplayName)


def modify(vartype,id,field,value):
    ot = otxml_simple.otXml()
    XmlResponse = ot.modifyTicket(vartype, id, field, value)
    #print XmlResponse.xml_result

def queryObject(id):
    ot = otxml_simple.otXml()
    results = []
    XmlResponse = ot.queryObjectsById(r"01. ITSM - Service Operation\02. Incident Management",["Title", "Description","State", "Number", "SolutionDescription"],id)
    tree = ET.fromstring(XmlResponse.xml_result)
    root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
    #print XmlResponse.xml_result
    for child in root:
        result = {}
        if child.attrib['id']:
            result['id'] = child.attrib['id']
            #setattr(new_object,'id', child.attrib['id'] )
            #print child.attrib['id']
            for attribute in child:
                result[attribute.get("name")] = attribute.text
                #try:
                    #print attribute.get("Value")
                #except:
                    #print "no value"
                #text = "info : %s : %s" % (attribute.get("name"), attribute.text)
                #try:
                    #print text.encode('utf-8')
                #except:
                    #print "couldn't print multiple line value %s" %(attribute.get("name"))

        results.append(result)
    return result


def finduserdisplayname(username):
    users = ListUsers()
    for r_user in users:
        if r_user.lastname.replace(" ", "").lower() in username.replace(" ", "").lower():
            if r_user.firstname.replace(" ", "").lower() in username.replace(" ","").lower():
                return r_user
    return False

def searchTicket(text, username):
    print "searching for %s".encode('utf-8') % text
    r_user = finduserdisplayname(username)
    username = r_user.userdisplayname
    ot = otxml_simple.otXml()
    xml = ot.queryObjectsFilter("internal-issues", "Applicant_name",
                                r"01. ITSM - Service Operation\02. Incident Management",
                                ["Title", "Description", "State", "Number"], "false", username, "StringVal").xml_result
    tree = ET.fromstring(xml)

    result = ""
    root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
    for child in root:
        if child.attrib['id']:
            ticketdid = child.attrib['id']
            for attribute in child:
                if attribute.get("name") == "Title":
                    tickettitle = attribute.text
                if attribute.get("name") == "Number":
                    ticketnumber = attribute.text
                if attribute.get("name") == "Description":
                    ticketdesc = attribute.text
                if attribute.get("name") == "State":
                    ticketstate = attribute.text
            #result = "%s, %s : %s, state : %s" % (result, ticketnumber, tickettitle, ticketstate)
            testresult = "id:%s/i-%s | Title : %s | state : %s | description : %s" % (ticketdid, ticketnumber, tickettitle, ticketstate, ticketdesc)
            if ticketstate != "Solved" and text in tickettitle:
                try:
                    print testresult.encode('utf-8')
                except Exception, e:
                    print e
                    # print result

def closeTicket(id, username, solution):
    r_user = finduserdisplayname(username)
    print "assigning to %s" % (r_user.userdisplayname)
    result = queryObject(id)

    currentsolution = result['SolutionDescription'].encode('utf-8')


    if currentsolution == "None":
        SolutionDescription = "Alfred : %s" % solution.encode('utf-8')
    else:
        SolutionDescription = "%s - Alfred : %s" % (currentsolution,solution)


    key = "Responsible"
    type = "userdisplayname"
    #
    modifyref(type, id, key, r_user.userdisplayname)
    modify('StringVal', id, 'SolutionDescription', SolutionDescription)

    title = result['Title'].encode('utf-8')
    print "Title : %s" % (title)
    #SolutionDescription = SolutionDescription
    print "Solution : %s.Done" % (SolutionDescription)
    modify('StringVal', id, 'State', 'Solved')
    print "State : Solved"



def addincident_query(title,description,username): #returns incident ID
    ot=otxml_simple.otXml()
    r_user = finduserdisplayname(username)
    IncidentId = ot.addIncident(Title=title,Description=description,UserDisplayName=r_user.userdisplayname,CategoryID="706057",Solution=" ").result
    key = "Applicant"
    type = "userdisplayname"
    modifyref(type, IncidentId, key, r_user.userdisplayname)
    modify('StringVal', IncidentId, 'Source', 'Internal Issues')
    key = "Responsible"
    type = "groupname"
    modifyref(type, IncidentId, key, "IT Admins")
    return IncidentId






def ListUsers():
    ot = otxml_simple.otXml()
    xml = ot.queryObjects(r"00. MasterData\05. People\05.1 Persons\User Accounts",[]).xml_result
    #print xml
    users = []
    tree = ET.fromstring(xml)
    root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
    for child in root:
        if child.attrib['id']:
            #print child.attrib['id']
            newuser = user.user()
            newuser.id = child.attrib['id']
            for attribute in child:
                if attribute.get("name") == "LoginName":
                    newuser.userloginname = attribute.text
                    #print attribute.text
                if attribute.get("type") == "userdisplayname" and attribute.get("name") == "RefOTUser":
                    newuser.userdisplayname = attribute.get("Value")
                    #print attribute.get("Value")
                if attribute.get("name") == "FirstName":
                    newuser.firstname = attribute.text
                    #print attribute.text
                if attribute.get("name") == "LastName":
                    newuser.lastname = attribute.text
                    #print attribute.text
            users.append(newuser)
    return users


def findMytickets(username):
    username = finduserdisplayname(username).userdisplayname
    #print "tickets for %s:" % (username)
    ot = otxml_simple.otXml()
    xml = ot.queryObjectsFilter("internal-issues","Applicant_name",r"01. ITSM - Service Operation\02. Incident Management",["Title", "Description","State", "Number"],"false",username,"StringVal").xml_result
    tree = ET.fromstring(xml)
    result = ""
    root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
    for child in root:
        if child.attrib['id']:
            ticketdid = child.attrib['id']
            for attribute in child:
                if attribute.get("name") == "Title":
                    tickettitle = attribute.text
                if attribute.get("name") == "Number":
                    ticketnumber = attribute.text
                if attribute.get("name") == "Description":
                    ticketdesc= attribute.text
                if attribute.get("name") == "State":
                    ticketstate = attribute.text
            result = "%s, %s : %s, state : %s" % (result,ticketnumber, tickettitle, ticketstate)
            testresult = "id:%s / %s : *%s*, state : %s" % (ticketdid, ticketnumber, tickettitle, ticketstate)
            if ticketstate!="Solved":
                try:
                    print testresult.encode('utf-8')
                except Exception, e:
                    print e
    #print result




def findAdmintickets(username):
    username = finduserdisplayname(username).userdisplayname
    #print "tickets for %s:" % (username)
    ot = otxml_simple.otXml()
    xml = ot.queryObjectsFilter("internal-issues-group","username",r"01. ITSM - Service Operation\02. Incident Management",["Title", "Description","State", "Number"],"false",username,"StringVal").xml_result
    tree = ET.fromstring(xml)
    #print xml
    result = ""
    root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
    for child in root:
        if child.attrib['id']:
            ticketdid = child.attrib['id']
            for attribute in child:
                if attribute.get("name") == "Title":
                    tickettitle = attribute.text
                if attribute.get("name") == "Number":
                    ticketnumber = attribute.text
                if attribute.get("name") == "Description":
                    ticketdesc= attribute.text
                if attribute.get("name") == "State":
                    ticketstate = attribute.text
            result = "%s, %s : %s, state : %s" % (result,ticketnumber, tickettitle, ticketstate)
            testresult = "id:%s / %s : *%s*, state : %s" % (ticketdid, ticketnumber, tickettitle, ticketstate)
            if ticketstate!="Solved":
                try:
                    print testresult.encode('utf-8')
                except Exception, e:
                    print e