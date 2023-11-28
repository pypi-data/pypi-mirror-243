import os
import json
from table import Table
from relationship import Relationship

class PBIItemParser:
    def __init__(self, filepath, itemType):
        self.filepath = filepath
        self.itemType = itemType
    def _parseGeneral(self):
        if not os.path.isdir(self.filepath) or not self.filepath.lower().endswith("."+self.itemType.lower()):
            raise Exception("file path is not a folder or not a {} folder".format(self.itemType))
        f = open(self.filepath + "/item.metadata.json")
        meta = json.load(f)
        f.close()
        if "type" not in meta or meta["type"] != self.itemType.lower() or "displayName" not in meta:
            raise Exception("item.metadata.json file is not consistent")
        self.name = meta["displayName"]
        
        f = open(self.filepath + "/item.config.json")
        meta = json.load(f)
        f.close()
        if "logicalId" not in meta:
            raise Exception("item.config.json file is not consistent")
        self.logicalId = meta["logicalId"]
    def toJSON(self):
        return json.dumps(self, default=lambda o: 
                          o.__dict__ if PBIItemParser in type(o).__bases__ or not hasattr(o, "toJSON")else o.toJSON(), indent=4)
    def parse(self):
        self._parseGeneral()
        self._parseDetail()
    def __str__(self):
        return self.toJSON()