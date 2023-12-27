import gspread
import json
from datetime import datetime, timedelta
import time

class GSheet:
    def __init__(self):
        config_file = json.load(open("config.json", 'r'))
        cred_file = config_file["cred_file"]
        sheet_url = config_file["sheet_url"]
        gc = gspread.service_account(cred_file)
        self.sheet = gc.open_by_url(sheet_url)
        worksheet_list = self.sheet.worksheets()
        worksheet_list = [worksheet.title for worksheet in worksheet_list]
        if "scraped_data" in worksheet_list:
            self.worksheet = self.sheet.worksheet("scraped_data")
        else:
            self.worksheet = self.sheet.add_worksheet(title="scraped_data", rows=100, cols=20)
            self.worksheet.clear()
        
        my_columns = ["Collection_name", "Account_name", "Account_address"]
        cell_list = self.worksheet.range('A1:C1')
        for i, val in enumerate(my_columns):
            cell_list[i].value = val
        self.worksheet.update_cells(cell_list)
        self.addresses = []
        records = self.worksheet.get_all_records()
        for record in records:
            self.addresses.append(record["Account_address"])
        self.new_rows = []
    def insert_batch(self):
        requests = {
        "requests": [
            {
            "insertDimension": {
                "range": {
                    "sheetId": self.worksheet._properties['sheetId'],
                    "startIndex": 1,
                    "dimension": "ROWS",
                    "endIndex": len(self.new_rows) + 1
                }
            }
            }
        ]

        }
        self.sheet.batch_update(requests)
        self.worksheet.batch_update([{
            "range": "A2:C{}".format(len(self.new_rows) + 1),
            "values": self.new_rows
        }])
    def add_to_sheet(self, collection_name, account_name, account_address):
        self.add_address(account_address)
        self.new_rows.append([collection_name, account_name, account_address])
        if len(self.new_rows) > 0:
            while True:
                try:
                    self.insert_batch()
                    self.new_rows = []  
                except:
                    time.sleep(5)
                    continue
                break
    
    def add_address(self, address):
        self.addresses.append(address)