from .field import Field
import json

class ReportField:
    def __init__(self, containerItem, dataset):
        self.containerJs = json.loads(containerItem["config"])
        self.name = self.containerJs["name"]
        self.fields = []
        if not "singleVisual" in self.containerJs:
            #raise Exception("Missing single Visual")
            print ("Missing single Visual in {}".format(self.name))
            return
        self.visualType = self.containerJs["singleVisual"]["visualType"]
        
        if not "projections" in self.containerJs["singleVisual"] or not self.containerJs["singleVisual"]["projections"]:
            if "objects" in self.containerJs["singleVisual"] and ("values" not in self.containerJs["singleVisual"]["objects"]or len(self.containerJs["singleVisual"]["objects"]["values"]) > 10):
                return
            raise Exception("Missing projection")
        
        for proj in self.containerJs["singleVisual"]["projections"]:
            for val in self.containerJs["singleVisual"]["projections"][proj]:
                queryRef = val["queryRef"]
                splt = queryRef.split(".")
                tableStr = splt[0]
                del splt[0]
                fieldStr = ".".join(splt)
                targetField = None
                for table in dataset.tables:
                    if table.name.lower() == tableStr.lower():
                        for field in table.fields:
                            if field.name.lower() == fieldStr.lower():
                                targetField = field
                if targetField is None:
                    #raise Exception("{} is missing in dataset {}".format(queryRef, dataset.name))
                    print ("{} is missing in dataset {}".format(queryRef, dataset.name))
                    return
                self.fields.append(targetField)

class Section:
    def __init__(self, sectionItem, dataset):
        self.raw = sectionItem
        self.name = sectionItem["name"]
        self.displayName = sectionItem["displayName"]
        self.containers = []
        for container in sectionItem["visualContainers"]:
            self.containers.append(ReportField(container, dataset))
        
    def toJSON(self):
        tmpRaw = self.raw
        del self.raw
        output = json.dumps(self, default=lambda o: 
                          o.__dict__ if Section == type(o) or not hasattr(o, "toJSON")else o.toJSON(), indent=4)
        self.raw = tmpRaw
        return json.loads(output)
    def __repr__(self):
        return type(self).__name__+" = "+self.displayName