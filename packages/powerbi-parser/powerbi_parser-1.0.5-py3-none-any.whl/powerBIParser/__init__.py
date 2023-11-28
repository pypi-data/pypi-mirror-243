import re
import sys
import os
from pbiDatasetParser import PBIDatasetParser
from pbiReportParser import PBIReportParser

class PowerBIParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.reports = []
        self.datasets = []
        if not os.path.isdir(self.filepath):
            raise Exception("file path is not a folder")
        for folder in os.scandir(self.filepath):
            if os.path.isdir(folder.path):
                if folder.name.endswith(".Dataset"):
                    self.datasets.append(PBIDatasetParser(folder.path))
                elif folder.name.endswith(".Report"):
                    self.reports.append(PBIReportParser(folder.path))
    def parse(self):
        for dataset in self.datasets:
            dataset.parse()
        for report in self.reports:
            report.parse(self.datasets)
