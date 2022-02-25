import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account


from time import sleep
import pyautogui
import pydirectinput as di
import sys
import random
import datetime
import glob

#オートGUIclassを実装したことによってここのベーシックアクションは要らなくなりつつある
#べーじっくアクションではランダム待機やランダム座標の計算とGUI系統についての動作をまとめる(BOTやセレニウムに継承できるようなカタチで定義している)
class SEARCH_CONSOLE_ACT():
    def __init__(self,url,d_list,searchdays):
        #開始日を稼働日をもとに計算によって求める
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        aweekago = yesterday - datetime.timedelta(days=searchdays)

        self.d_list= d_list
        self.start_date = str(aweekago)
        self.end_date = str(yesterday)


        print([self.start_date,self.end_date],"の期間で計測")
        self.url = url


    def action(self,start_row,limit,savedir):

        #ドメイン毎に異なるサーチコンソールの認証情報を定義する
        if("supari" in savedir):
            path = f"domains/supari/"
            credentials = service_account.Credentials.from_service_account_file(path+'exid-tesuto_jsons/mexspreadsheet-python-8940f4090502.json')
            webmasters = build('webmasters', 'v3', credentials=credentials)
            print(webmasters.sites().list().execute())
        elif("iqos919" in savedir):
            path = f"domains/iqos919/"
            credentials = service_account.Credentials.from_service_account_file(path+'exid-tesuto_jsons/search-console-python-919-fad3f7814b61.json')
            webmasters = build('webmasters', 'v3', credentials=credentials)
            print(webmasters.sites().list().execute())

        url = self.url
        d_list = self.d_list
        start_date = self.start_date
        end_date = self.end_date
        row_limit = limit
        body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': d_list,
            'rowLimit': row_limit,
            'startRow':start_row
        }
        response = webmasters.searchanalytics().query(siteUrl=url, body=body).execute()
        df = pd.io.json.json_normalize(response['rows'])
        for i, d in enumerate(d_list):
            df[d] = df['keys'].apply(lambda x: x[i])
        df.drop(columns='keys', inplace=True)

        df.to_csv(f"{savedir}/{start_date}-{end_date}({start_row}~{start_row+limit}).csv", index=False)
        print(df)

        return f"{start_date}-{end_date}(full)"


