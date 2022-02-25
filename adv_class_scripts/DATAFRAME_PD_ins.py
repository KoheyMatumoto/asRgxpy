import pandas as pd
import numpy as np

from time import sleep
import datetime



#read_csvなら、ヘッダの有無で一発でデータフレームに変換することもできる。
#面倒な2次元リスト状態からデータフレームを作成しなければいけない場合の処理をこのインスタンスでは行う。

class DATAFRAME_PD():
    def __init__(self):
        print("df instance OK")

        #to csvは、ファイル名を与えてそのファイル名でデータフレームをcsv保存する。
        #df.to_csv(f"{savedir}/{start_date}-{end_date}({start_row}~{start_row+limit}).csv", index=False)
        #print(df)


    def dim2_to_df(self,dim2,headflag):
        print("open dataframe")

        #フラグがTrueなら配列の頭[0]を落とし、それをヘッダに利用する
        if(headflag):
            headlist = dim2.pop(0)
        df = pd.DataFrame(dim2,columns=headlist)
        return df

    
    #ruleにはasc か descの文字列が入る
    def sorting_df(self,fromdf,ordercolumn,rule="asc"):
        #headerの[1]にランキング根拠変数となるカラムが入ってる
        headlist = list(fromdf.head(0))
        sort_by = headlist[1]
        print(f"ルール：{rule}で、列名：{sort_by}に対して数字として扱ってソートします")

        #fromdf[sort_by] = fromdf[sort_by].astype('int')
        #数字として扱う際にコンマ区切りが邪魔をするので置換してintに変換
        fromdf[sort_by] = fromdf[sort_by].str.replace(',','').astype('int')

        #※テーブル上での表記をカンマ区切りに戻すならここで再度フォーマットしなおす手順を挟む
        #現状は省略中
        
        res_df = fromdf.sort_values(sort_by,ascending=False)

        return res_df



