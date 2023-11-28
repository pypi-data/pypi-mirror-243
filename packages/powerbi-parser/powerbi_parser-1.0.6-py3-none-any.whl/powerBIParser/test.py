from . import PowerBIParser

if __name__ == "__main__":
    parser = PowerBIParser("/Users/rapha/Documents/DIOR/AzureDevOps/PBI-EDV-My-KPIs")
    parser.parse()
    print(parser)
