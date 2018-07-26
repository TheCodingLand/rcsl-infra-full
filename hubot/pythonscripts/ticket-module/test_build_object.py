import otxml_simple
import xml.etree.ElementTree as ET
import build_object



users = []
ot = otxml_simple.otXml()
id= "1256840"
xml = ot.queryObjectsById(r"01. ITSM - Service Operation\02. Incident Management",["Title", "Description","State", "Number", "SolutionDescription", "AssociatedCategory"],id).xml_result
#xml = ot.queryObjects(r"00. MasterData\05. People\05.1 Persons\User Accounts", []).xml_result
tree = ET.fromstring(xml)
root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
for child in root:
    user = build_object.buildobject(child)
    users.append(user)
    print user.result.title
    print user.result.associatedcategory



