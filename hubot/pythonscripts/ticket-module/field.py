

class Field():
    def __init__(self, attribute):
        if attribute.get("name"):
            self.name = attribute.get("name").replace(" ","").lower()
            self.dbname = attribute.get("name")
            if "}" in attribute.tag:
                self.type= attribute.tag.split("}")[1]
            else:
                self.type = attribute.tag

            if self.type == "ReferenceToUserVal":
                self.value = attribute.get("Value")
                self.name = attribute.get("type")

            if self.type == "ReferenceListVal":
                self.value = attribute.get("objectIds")
            if self.type == "ReferenceVal":
                self.value = attribute.get("objectId")
            else:
                self.value = attribute.text

            self.refType = attribute.get("type")

