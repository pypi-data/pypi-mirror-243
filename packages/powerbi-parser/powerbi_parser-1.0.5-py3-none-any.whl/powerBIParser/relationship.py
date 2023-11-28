from field import Field
import json

class Relationship:
    def __init__(self, relationshipItem, tables):
        self.raw = relationshipItem
        self.id = relationshipItem["name"]
        self.fromColumn = relationshipItem["fromColumn"]
        self.fromTable = relationshipItem["fromTable"]
        self.toColumn = relationshipItem["toColumn"]
        self.toTable = relationshipItem["toTable"]
        self.fromField = None
        self.toField = None
        for table in tables:
            for field in table.fields:
                if self.fromTable.lower() == table.name.lower() and field.name.lower() == self.fromColumn.lower():
                    self.fromField = field
                if self.toTable.lower() == table.name.lower() and field.name.lower() == self.toColumn.lower():
                    self.toField = field
        if self.fromField is None:
            print("{}.{} not found".format(self.fromTable, self.fromColumn))
        if self.toField is None:
            print("{}.{} not found".format(self.toTable, self.toColumn))
    def toJSON(self):
        tmpFrom = self.fromField
        tmpTo = self.toField
        tmpRaw = self.raw
        del self.toField
        del self.fromField
        del self.raw
        output = json.dumps(self, default=lambda o: o.__dict__)
        self.toField = tmpTo
        self.fromField = tmpFrom
        self.raw = tmpRaw
        return json.loads(output)
    def __repr__(self):
        return type(self).__name__+" = "+self.id