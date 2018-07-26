import otxml_simple
import xml.etree.ElementTree as ET
import build_object
class query():

    def ListUsers(self):
        users = []
        ot = otxml_simple.otXml()
        xml = ot.queryObjects(r"00. MasterData\05. People\05.1 Persons\User Accounts", []).xml_result
        tree = ET.fromstring(xml)
        root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
        for child in root:
            user = build_object.buildobject(child)
            users.append(user)
            print user.result.number
            print user.result.firstname
            #print user.result.displayname
        return users


    def ListTickets(self):
        users = []
        ot = otxml_simple.otXml()
        xml = ot.queryObjects(r"00. MasterData\05. People\05.1 Persons\User Accounts", []).xml_result
        tree = ET.fromstring(xml)
        root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
        for child in root:
            user = build_object.buildobject(child)
            users.append(user)
            print user.result.number
            print user.result.firstname
        return users






