import pandas as pd
import os

class WorkBook:
    def __init__(self):
        self.sheets = {}
        
    def size(self):
        return len(self.sheets)
    
    def append(self,sheet,sheet_name):
        self.sheets[sheet_name] = sheet

    def write_all(self,parent_dir,should_create_dir=True):
        if should_create_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        # TODO raise custom exception if dir does not exist

        for s,df in self.sheets.items():
            df.to_csv(f"{parent_dir}/{s}.csv", encoding='utf-8', index=False, header=True)


    def from_xlsx(filename):
        wb = WorkBook()
        xl = pd.ExcelFile(filename)
    

        for s in xl.sheet_names:
            wb.append(pd.read_excel(xl,sheet_name=s),s)

        return wb
