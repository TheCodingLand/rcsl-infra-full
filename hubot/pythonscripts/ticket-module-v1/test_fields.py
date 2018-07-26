import otxml_simple
import xml.etree.ElementTree as ET
from field import Field

from collections import namedtuple


def ListUsers():
    ot = otxml_simple.otXml()
    xml = ot.queryObjects(r"00. MasterData\05. People\05.1 Persons\User Accounts",[]).xml_result


    users = []

    tree = ET.fromstring(xml)
    root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
    #print xml
    for child in root:
        if child.attrib['id']:
            userfields = []

            userfields.append('id')
            for attribute in child:
                field = Field(attribute)
                #print attribute
            #print child.attrib['id']
                    #print attribute.text
                userfields.append(field)
            users.append(userfields)
    object_users=[]
    for a_user in users:

        fieldnames= []
        values= []
        for field in a_user:

            fieldnames.append(field.name)
            values.append(field.value)
            #print "##NAME## %s ##VALUE## %s ##TYPE## %s ##REFTYPE## %s" %(field.name, field.value, field.type, field.refType)

        if 'User' not in locals():
            print fieldnames
            User = namedtuple('User', fieldnames, rename = True, verbose=True)

        user = User(*values)


        object_users.append(user)

    for object_user in object_users:
        print object_user.firstname




ListUsers()