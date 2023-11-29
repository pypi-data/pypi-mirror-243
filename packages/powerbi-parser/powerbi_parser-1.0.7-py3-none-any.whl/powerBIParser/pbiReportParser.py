import os
import json
from .pbiItemParser import PBIItemParser
from .pbiDatasetParser import PBIDatasetParser
from .section import Section

class PBIReportParser(PBIItemParser):
    def __init__(self, filepath):
        super().__init__(filepath, "Report")
        self.filepath = filepath
    def _parseGeneral(self, datasets):
        super()._parseGeneral()
        f = open(self.filepath + "/definition.pbir")
        meta = json.load(f)
        f.close()
        if "datasetReference" in meta and meta["datasetReference"] and "byPath" in meta["datasetReference"] and meta["datasetReference"]["byPath"] and "path" in meta["datasetReference"]["byPath"]:
            tmpdataset = meta["datasetReference"]["byPath"]["path"]
            idx = tmpdataset[::-1].index("/") if "/" in tmpdataset else len(tmpdataset)
            self.datasetName = tmpdataset[len(tmpdataset) - idx : -8]
            self.dataset = next((ds for ds in datasets if self.datasetName == ds.name), None)
            
    def _parseDetail(self, datasets):
        f = open(self.filepath + "/report.json")
        meta = json.load(f)
        f.close()
        self.sections = []
        for section in meta["sections"]:
            self.sections.append(Section(section, self.dataset))

    def parse(self, datasets):
        self._parseGeneral(datasets)
        self._parseDetail(datasets)
    def toJSON(self):
        tmpdataset = None
        if hasattr(self, 'dataset'):
            tmpdataset = self.dataset
            del self.dataset
        output = super().toJSON()
        self.dataset = tmpdataset
        return output
    