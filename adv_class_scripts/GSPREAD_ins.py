import enum
from cv2 import solveP3P
import pyautogui
from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv


class GSPREAD():
    def __init__():
        super().__init__()
        print("Gspread initialize")


    def gspread_start(self,jsonpath,drive_filename,sheet_name):
        self.json_file_path = jsonpath
        self.spread_file_name = drive_filename
        self.sheet_name1 = sheet_name
        #sheet_name2 = 'csv_sheet'
        #csv_file_name = 'Davis.csv'
        self.scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
        
    # スプレッドシートにアクセス(jsonと2つのURLを使用(scopeとして定義))
    def access_spreadsheet(self):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.json_file_path, self.scope)
        self.gc = gspread.authorize(self.credentials)
        self.sh = self.gc.open(self.spread_file_name)
        self.wks = self.sh.worksheet(self.sheet_name1)
        self.sheet_list = [ws.title for ws in self.sh.worksheets()]
        coldata1_l = len(self.wks.col_values(1))
        coldata2_l = len(self.wks.col_values(2))
        coldata3_l = len(self.wks.col_values(3))
        coldata4_l = len(self.wks.col_values(4))


        if((coldata1_l == coldata2_l)and(coldata1_l== coldata3_l)and(coldata1_l== coldata4_l)):
            print(self.sheet_name1,"は",coldata1_l,coldata2_l,coldata3_l,coldata4_l,"で平らなシートです")
        else:
            print(self.sheet_name1,"は",coldata1_l,coldata2_l,coldata3_l,coldata4_l,"でダメシートです")
            return "error"

        print(f"{coldata1_l}番目が最終行です。appendを行う場合、対象行は{coldata1_l+1}です。")
        return "ok"

    #access_spreadsheetメソッドを使用後に使用可能、シート名を頼りに取得したワークシートの最下段に1行(1次元配列)丸ごと追記書き込みを行う
    def append_row_to_sheet(self,add_dim1):
        self.wks.append_row(add_dim1)
        print(f"{self.sheet_name1}に{add_dim1}を書き込み完了しました。")

    #access_spreadsheetを使用後に使用可能
    def reset_nowaccess_sheet(self):
        try:
            self.sh.del_worksheet(self.wks)
            self.sh.add_worksheet(title=self.sheet_name1,rows=1000,cols=20)
        except Exception as e:
            print(e)
            return    

    #access_spreadsheetを使用後に使用可能
    def append_dim2_to_sheet(self,csvpath,sheet_name2):
        print("append dim2")
        # 書き込むシート作成。すでにあれば読み込む
        if sheet_name2 in self.sheet_list:
            wks = self.sh.worksheet(sheet_name2)
        else:
            wks = self.sh.add_worksheet(title=sheet_name2, rows='300', cols='20')
        # CSVを書き込み
        wks.update(list(csv.reader(open(csvpath, encoding='utf-8'))))    

#初期設定とmethodに割り振って汎用性を持たせる
# 設定

#json_file = 'python-instchecker-8ad30eebc6d2.json'
#spread_file_name = 'py access sheet'
#sheet_name1 = 'send_from_py'
#sheet_name2 = 'csv_sheet'
#csv_file_name = 'Davis.csv'

#scope = ['https://spreadsheets.google.com/feeds',
#        'https://www.googleapis.com/auth/drive']

# スプレッドシートにアクセス
#credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
#gc = gspread.authorize(credentials)
#sh = gc.open(spread_file_name)

#新規作成ならこのように書く
#wks = sh.add_worksheet(title="pythonによって生成された新規シート", rows='100', cols='30')

#取得して書き込むならシートの名前を書く
#wks = sh.worksheet(sheet_name1)