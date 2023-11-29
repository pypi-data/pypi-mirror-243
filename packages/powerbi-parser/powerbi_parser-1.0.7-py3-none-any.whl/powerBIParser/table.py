from .field import Field
from .measure import Measure
import json

class Table:
    def __init__(self, tableItem):
        self.raw = tableItem
        self.name = tableItem["name"]
        self.lineageTag = tableItem["lineageTag"]
        self.annotations = tableItem["annotations"]
        self.fields = []
        self.sources = []
        if "columns" in tableItem:
            for col in tableItem["columns"]:
                self.fields.append(Field(col, self))
        if "measures" in tableItem:
            for col in tableItem["measures"]:
                self.fields.append(Measure(col, self))

    def toJSON(self):
        tmpRaw = None
        if hasattr(self, "raw"):
            tmpRaw = self.raw
            del self.raw
        output = json.dumps(self, default=lambda o: 
                          o.__dict__ if Table == type(o) or not hasattr(o, "toJSON")else o.toJSON(), indent=4)
        self.raw = tmpRaw
        return json.loads(output)
    def __repr__(self):
        return type(self).__name__+" = "+self.name
    def __str__(self):
        return self.name