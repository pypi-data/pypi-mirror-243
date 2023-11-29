import json

class FieldInterface:
    def __init__(self, fieldItem, table):
        self.raw = fieldItem
        self.name = fieldItem["name"]
        self.tableName = table.name
        self.table = table
        self.itemType = "field"
        self.lineageTag = fieldItem["lineageTag"]
        self.annotations = fieldItem["annotations"] if "annotations" in fieldItem else None
        self.formatString = fieldItem["formatString"] if "formatString" in fieldItem else None
    def toJSON(self):
        tmptbl = self.table
        del self.table
        tmpRaw = self.raw
        del self.raw
        tmpField = None
        if hasattr(self, "field"):
            tmpField = self.field
            if self.field:
                self.field = self.tableName+"."+tmpField.name
        output = json.dumps(self, default=lambda o: o.__dict__)
        self.table = tmptbl
        self.raw = tmpRaw
        self.field = tmpField
        return json.loads(output)
    def __repr__(self):
        return type(self).__name__+" = "+self.name
    def __str__(self):
        return "{}.{}".format(self.table, self.name)