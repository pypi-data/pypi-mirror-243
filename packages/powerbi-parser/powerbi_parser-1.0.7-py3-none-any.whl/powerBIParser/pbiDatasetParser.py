import os
import json
from .table import Table
from .relationship import Relationship
from .pbiItemParser import PBIItemParser

class PBIDatasetParser(PBIItemParser):
    def __init__(self, filepath):
        super().__init__(filepath, "Dataset")
        self.filepath = filepath
        
    def _parseDetail(self):
        f = open(self.filepath + "/model.bim")
        dataset = json.load(f)
        f.close()
        if "compatibilityLevel" not in dataset or "model" not in dataset or type(dataset["model"]) is not dict:
            raise Exception("model.bim file is not consistent")
        self.compatibilityLevel = dataset["compatibilityLevel"]
        self.culture = dataset["model"]["culture"]
        self.cultures = dataset["model"]["cultures"]
        self.tables = []

        for tab in dataset["model"]["tables"]:
             self.tables.append(Table(tab))
        self.relations = []
        for rel in dataset["model"]["relationships"]:
            self.relations.append(Relationship(rel, self.tables))
    