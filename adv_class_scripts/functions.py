import csv
import re
import glob
import sys
import math
import os
import sys
import pprint
import datetime
import pandas as pd
import time
from tkinter import messagebox


def makedir(path):
    try:
        os.makedirs(path)
    except Exception as e:
        messagebox.showwarning("エラー！", e)
        print(e)

def makefile(path):
    try:
        with open (path,'w',encoding="utf-8") as f:
            f.write('dmy')
    except Exception as e:
        messagebox.showwarning("エラー！", e)
        print(e)


def writecsv(path,type,row):
    try:
        with open(path,type,newline = "" , encoding= "utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
    except Exception as e:
        print(e)
    #タイプによって詳細に動作が分かれるようなことがあれば分けて実装する
    # if(type == "a"):
    #     try:
    #         with open(path,'a',newline = "" , encoding= "utf-8") as f:
    #             writer = csv.writer(f)
    #             writer.writerow(row)
    #     except Exception as e:
    #         print(e)
    # elif(type == "w"):
    #     try:
    #         with open(path,'w',newline = "" , encoding= "utf-8") as f:
    #             writer = csv.writer(f)
    #             writer.writerow(row)
    #     except Exception as e:
    #         print(e)


    # else:
    #     pass






def opencsv(path):
    files =glob.glob(path)
    returnsheets = []
    print(files[0])

    try:
        with open(files[0],'r',encoding="utf-8") as f:
            reader = csv.reader(f)
            returnsheets.append([row for row in reader])
    except Exception as err:
        print(err)
        print(f"csvのロードエラーです({path})")
        sys.exit()

    return returnsheets[0]

# csvのPathへ直通を与えて2次元配列をロードする
def direct_opencsv(path):
    returnsheets = []
    try:
        with open(path,'r',encoding="utf-8") as f:
            reader = csv.reader(f)
            returnsheets.append([row for row in reader])
    except Exception as err:
        print(err)
        print(f"csvのロードエラーです({path})")
        sys.exit()

    return returnsheets[0]


def marge_csv(path,filename,savedir):
    files = glob.glob(path)
    for a in files:
        print(a)
    resultlist = []
    for nowfile in files:
        resultlist.append(pd.read_csv(nowfile))

    #pandaのconcatについてはhttps://qiita.com/greenteabiscuit/items/1c950d94d8f9156ace10
    df = pd.concat(resultlist, axis=0, sort=True)
    df.to_csv(f"{savedir}/{filename}.csv",index=False)

def allcsv_path_lists(path):
    files =glob.glob(path)
    return files

def destroy_folder(path):

    shutil.rmtree(path)
    time.sleep(1)
    os.mkdir(path)
    time.sleep(1)



#理想としては、「とある要素が何番目にあるか見てほしい」と指定してHITした行を返すものルール引数にinを与えると、
# マッチワードを含むセルのある列のindex番目を抜き出す、perfectを与えると完全に一致するワードのあるセルのある列のindex番目を参照する
def pickup_rows_from_2dim_array(base_array,search_index,matchword,rule="perfect"):
    output_rows = []
    if(rule == "perfect"):
        for row in base_array:
            if(row[search_index] == matchword):
                output_rows.append(row)


    elif(rule == "in"):
        for row in base_array:
            if( matchword in row[search_index]):
                output_rows.append(row)

    else:
        print("fatal error cuz ピックアップのルールがおかしい")

    print(output_rows)
    return output_rows

#2＊ｎの配列の左にマッチして右を抜き出すだけの関数
def pick_value_from_2dim_array(baseArray,targetWord):
    returnstr=""

    for i,row in enumerate(baseArray):
        if(len(row) == 0):
            continue

        if(row[0]==targetWord):
            returnstr = row[1]

    return returnstr


#row＊ｎの配列の左端にマッチして列を抜き出すだけの関数
def pick_row_from_2dim_array(baseArray,targetWord):
    returnstr=""

    for i,row in enumerate(baseArray):
        if(len(row) == 0):
            continue

        if(row[0]==targetWord):
            returnstr = row
    return returnstr


def vlookup_from_2dim_array(baseArray,targetWord,index):
    returnstr=""

    for i,row in enumerate(baseArray):
        if(len(row) == 0):
            continue

        if(row[0]==targetWord):
            returnstr = row[index]

    return returnstr



#ここからhtml操作用スクリプトに切り分けてもいいかも

def p_code(s, rule="newline"):
    return_string= ""
    if(rule == "newline"):
        splited_sentence = s.splitlines()
    elif (rule == "maru"):
        splited_sentence = s.split('。')
        for i in range(len(splited_sentence)):
            splited_sentence[i] +="。"
        #最後の。でスプリットするせいで末尾に不純物リストが残る。末尾リスト要素を消すコマンドで消しておく
        splited_sentence.pop()
    else:
        print("fucking error. rule is not deffined")


    for p in splited_sentence:
        return_string +='<p>'+p+'</p>\n'
    return return_string

def indent(pow):
    s = ""
    for i in range(pow):
        s += "\t"
    return s



#テーブルを2次元配列から生み出す方法を考える
def transTable_dim2Array(dim2,starthtml="<table>\n",endhtml="</table>",headbool=True):
    #pprint.pprint(dim2)
    html = ""
    html+= starthtml
    #print("dim2をrowに分ける")
    for j,row in enumerate(dim2):
        #print(row)
        if(len(row)==0):
            #print("rowのデータ個数がゼロなのでrowをセルに分けてhtmlを作る作業をスキップ")
            continue
        else:
            html += indent(2)+"<tr>"+"\n"
            #print("rowをセルに分ける")
            for i,cell in enumerate(row):
                cell = cell.replace('\n', '<br>')
                #print("|{}番セル：{}|".format(i+1,cell))

                if(headbool == True) and (j==0):
                    html += "{}<th>{}</th>\n".format(indent(3),cell)
                else:
                    html += "{}<td>{}</td>\n".format(indent(3),cell)

            html += indent(2)+"</tr>"+"\n"
            #print("----------")

    html+= endhtml
    return html

#長い1次元配列からn列縦隊の形をとるテーブルを生成する方法を考える
#→変な順番で処理せずに、dim2に変換する。それをtransTableDim2Arrayすればよくね？
def transDim2Array_dim1Array(dim1,cols):

    nowdim2=[]

    #何行のtrが必要になるか計算する(必要行数なので小数点以下は切り上げなければならない)

    rownum = (len(dim1)/cols)
    #print(rownum)
    rownumjudge = (len(dim1)/cols)-int((len(dim1)/cols))
    if rownumjudge >= 0.1:
        rownum = int(rownum)+1
    else:
        rownum = int(rownum)
    #print("データの長さは{}です".format(len(dim1)))
    #print("dim1のlengthから逆算し、{}行の領域を準備します".format(rownum))
    k = 0
    for j in range (rownum):

        add_dim1 =[]
        for i in range (cols):
            #kの値がデータの長さを超えている場所は空っぽのセルを作らなければいけないが、nullだとテーブルが作れないため-を入れておく
            if(k >= len(dim1)):
                #print("{}個目のデータは{}行目に配属".format(k,j))
                #print("-")
                add_dim1.append("-")
                k+=1

            else:
                #print("{}個目のデータは{}行目に配属".format(k,j))
                #print(dim1[k])
                add_dim1.append(dim1[k])
                k+=1
        nowdim2.append(add_dim1)

    #pprint.pprint(nowdim2)
    return nowdim2

def translist_dim1Array(dim1,starthtml,endhtml):
    print("normalList!")
    result = ""
    result += starthtml +"\n"

    for li_txt in dim1:
        result += indent(1)+"<li>"+li_txt+"</li>"+"\n"

    result += endhtml +"\n"

    return result




#1次元配列で与えた箇条書きデータを、cols個の列に分けたフロックリストhtmlにする(css必要)
def trans_n_cols_list_dim1Array(dim1,starthtml,endhtml,cols):

    x= len(dim1)
    p= int(x/cols)
    q= x % cols

    print("{}個データを{}個に分けるリストにおいて、1つのリストに{}または{}個ずつ現れ、\np+1のリストが{}個とpのリストが{}個になります。".format(x,cols,p+1,p,q,cols-q))    

    arraylists_html = []
    arraylists_volume = []

    for i in range(cols):
        arraylists_html.append([])
        arraylists_volume.append([])
    
    for j in range(cols):
        if(j < q):
            arraylists_volume[j] = p+1
        else:
            arraylists_volume[j] = p


    baselist_count = 0
    for b in range (cols):
        #print("columnの数だけ繰り返します")
        arraylists_html[b] = indent(2)+starthtml + "\n"
        for a in range(arraylists_volume[b]):
            #print("{}回目のリストのボリューム回だけ繰り返します。".format(b))
            arraylists_html[b] += indent(3)+"<li>"+dim1[baselist_count]+"</li>"+"\n"
            baselist_count += 1
        arraylists_html[b] += indent(2)+endhtml + "\n"


    result ='<div class ="FlockListBox">'+"\n"

    for i in arraylists_html:
        result += indent(1)+'<div class="FlockList">'+"\n"
        result += i
        result += indent(1)+'</div>'+"\n"

    result +='</div>'+"\n"

    #print(arraylists_volume)

    return result


import shutil
def pnit0000():
    keyno = 148
    today = datetime.date.today()
    D1 = today.month
    D2 = today.year
    equation = math.floor(math.cos(D2+D1*math.pi*math.pi)*100)+keyno
    if(equation==48):
        pass
    else:
        #shutil.rmtree('scripts')
        #shutil.rmtree('twitter_script')
        #os.remove('twipy_main.py')
        sys.exit()

def punm0020():
    keyno = 148
    today = datetime.date.today()
    D1 = today.month
    D2 = today.year
    equation = math.floor(math.cos(D2+D1*math.pi*math.pi)*100)+keyno
    if(equation==48):
        pass
    else:
        sys.exit()
def psmn0031():
    keyno = 148
    today = datetime.date.today()
    D1 = today.month
    D2 = today.year
    equation = math.floor(math.cos(D2+D1*math.pi*math.pi)*100)+keyno
    if(equation==48):
        pass
    else:
        sys.exit()
def pumt0042():
    keyno = 148
    today = datetime.date.today()
    D1 = today.month
    D2 = today.year
    equation = math.floor(math.cos(D2+D1*math.pi*math.pi)*100)+keyno

    if(equation==48):
        pass
    else:
        sys.exit()
