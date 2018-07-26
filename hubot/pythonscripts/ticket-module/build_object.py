from field import Field
from collections import namedtuple


class buildobject(object):
    def __init__(self, name, data):
        self.fieldnames=[]
        self.values = []
        if data.attrib['id'] != None:
            self.fieldnames.append("id")
            self.values.append(data.attrib['id'])
            for attribute in data:
                field = Field(attribute)
                self.fieldnames.append(field.name)
                self.values.append(field.value)
        newtuple = namedtuple(name, self.fieldnames, rename=True, verbose=False)
        self.result = newtuple(*self.values)



