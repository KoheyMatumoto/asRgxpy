
import shutil
import re
import sys
import os
from time import sleep
import pandas as pd
import numpy as np
import html
import datetime


from adv_class_scripts import UI_ins
from adv_class_scripts import SELENIUM_ins
from adv_class_scripts import functions
from adv_class_scripts import GSPREAD_ins
from adv_class_scripts import AUTOGUI_ins
from adv_class_scripts import DATAFRAME_PD_ins

from adv_class_scripts import MULTI_REPLACE_ins

#from adv_class_scripts import SEARCH_CONSOLE_ins


class SET_UI(MULTI_REPLACE_ins.MULTI_REPLACE):
    def __init__(self):
        super().__init__()

        print("i can put all ui.")
        self.infomation_string = "initialized_info"
        self.start_btn_flag = False
        #ウインドウ定義
        self.main_window = UI_ins.UI_WINDOW("asRgx-py assist-search-regex REPLACER",800,600,"img/backimg1.png")

        #左上UI
        wp_list = [
            "Mizu",
            "Mizu1",
            "Convini"
        ]
        self.wp_dict ={
            "Mizu":"adv_class_scripts/wp_detaill_config/Mizucool_wp config.csv",
            "Mizu1":"https://mizu-cool.jp/wp-admin/",
            "Convini":"adv_class_scripts/wp_detaill_config/コンビニ_wp config.csv",        
        }
        
        self.set_easy_searchword_dim2 =[
            ["@@なんでも100@@","[\r\n\s\S]{0,100}?"],
            ["@@なんでも300@@","[\r\n\s\S]{0,300}?"],
            ["@@なんでも500@@","[\r\n\s\S]{0,500}?"],
        ]
        
        
        self.wp_choice = UI_ins.SET_UI_COMBO(65,125,"",wp_list,40)
        self.urlfield = UI_ins.SET_UI_TEXTAREA(65,175,"",37,14)


        self.targetstr_entry = UI_ins.SET_UI_ENTRY(70,450,"",40,True)
        self.replacestr_entry = UI_ins.SET_UI_ENTRY(70,500,"",40,True)

        self.dict_chk = UI_ins.SET_UI_CHKBOX(70,530,"この入力欄を使用せずに置き換え定義辞書を使う",False)


        #右UI

        self.time_entry = UI_ins.SET_UI_ENTRY(410,125,"",40,True)

        self.infotext = UI_ins.SET_UI_TEXTAREA(410,190,"",40,15)
        self.infotext.change_value(self.infomation_string)

        self.start_btn = UI_ins.SET_UI_BTN(410,480,"",lambda: self.start_btn_act(True),"*Start Action*","limegreen","14")
        self.chk = UI_ins.SET_UI_CHKBOX(410,520,"安全装置を無視して\n緑ボタンを押す",False)

        self.pre_start_btn = UI_ins.SET_UI_BTN(550,480,"",lambda: self.start_btn_act(False),"*Preview Action*","pink","14")
        self.preurl_entry = UI_ins.SET_UI_ENTRY(550,520,"test viewに利用するURL番号",10,True)
        self.preurl_entry.change_value("0")


        self.hiddensys_btn = UI_ins.SET_UI_BTN(680,5,"",lambda: self.hiddensys_act(),"*hidden*","purple","6")


class Galaxy(SET_UI):
    def __init__(self):
        super().__init__()
        print("galaxy instance OK")


    def start_btn_act(self,flag):
        print("start pushed")

        #辞書の受取関数
        #単体置き換えが成功してから実装
        
        #URLのスプリット関数
        self.inputURLs = self.urlfield.make_array_from_input_bylines()
        print(self.inputURLs)

        #wpへログインを1度だけ済ませ、1枚のセレニウムでループアクセスしたい
        nowwp = self.wp_choice.combo.get()
        try:
            wpdata_path = self.wp_dict[nowwp]
            wp_dim2 = functions.opencsv(wpdata_path)
        except Exception as e:
            print(e)
            print("対象ワードプレス情報が正常に定義されませんでした。終了。")
            return

        instance = SELENIUM_ins.WORDPRESS_SELENIUM(wp_config_dim2=wp_dim2)
        instance.try_login_wp()

        if(flag ==True and self.start_btn_flag ==True):
            print("緑ボタンかつプレビューが完了しています。ループ実行へ進みます。")
            pass
        elif(flag ==True and self.chk.bln.get()==True):
            print("フラグはそろっていませんが緑が押されていて、チェックが入っています。安全装置を無視してループへ進みます。")
            pass            
        elif(flag ==False):
            print("プレビューのための1回処理とコード表示まででreturnします")
            #nはクライアントから取得する
            n=int(self.preurl_entry.entry.get())

            instance.jump(self.inputURLs[n])
            print("編集画面に突入(条件クリア後は突入ボタンの定義やhtmlフィールドの定義もcsvに加える必要がある)")
            link = instance.gethtmlBySelector("li[id*='bar-edit'] a")
            instance.enter_element(link)

            print("html情報を取得したい")
            thishtml = instance.gethtmlBySelector("textarea[class*=wp-editor-area]")
            thishtml = thishtml.get_attribute("innerHTML")
            thishtml = html.unescape(thishtml)

            print(thishtml)

            print("htmlstrを単体置換。いずれは辞書データのロードとForループになる")
            replaced_html = self.replace_move(thishtml)

            print(replaced_html)


            self.infotext.change_value(replaced_html)
            UI_ins.SET_UI_messagebox("test preview","プログラムが実行されるとinfoに示すコードで保存されます。\n確認してOKであれば緑のボタンで開始して下さい。")
            self.start_btn_flag = True
            return
        elif(flag ==True, self.start_btn_flag==False):
            print("緑ボタンが押されたもののプレビューをしていません。強制終了")
            instance.endselenium()
            return
        else:
            print("フラグの整合性エラー。強制終了")
            instance.endselenium()
            sys.exit()


        #フラグが揃ってパスされたらここが実行される

        for i,url in enumerate(self.inputURLs):
            instance.jump(url)
            self.time_entry.change_value(f"【{i+1}/{len(self.inputURLs)}】を実行中")
            print("編集画面に突入(条件クリア後は突入ボタンの定義やhtmlフィールドの定義もcsvに加える必要がある)")
            link = instance.gethtmlBySelector("li[id*='bar-edit'] a")
            instance.enter_element(link)

            print("html情報と編集ページのURLを取得したい")
            #編集ページのURLはこのタイミングで初出
            htmlarea = instance.gethtmlBySelector("textarea[class*=wp-editor-area]")
            thishtml = htmlarea.get_attribute("innerHTML")
            thishtml = html.unescape(thishtml)

            print(thishtml)
            print("置換作業。UIから単体。いずれは辞書データをロードしてループにも対応")
            replaced_html = self.replace_move(thishtml)

            print(replaced_html)



            print("html情報を全消しして貼り付け")
            htmlarea.clear()
            instance.pastehtml(replaced_html)

            print("保存ボタンを押す")
            instance.hozon(True)

            print("[編集時間,url]となる1次元配列を作成、csvに追記")

            editurl = instance.getnowurl()

            edittime = datetime.datetime.today()
            
            arr = [editurl,edittime]
            #生成したタイムスタンプをcsvに送る。追記は"a",書き込みは"w"
            functions.writecsv("logfile/log.csv","a",arr)

            #リミッター(解除すると全部の記事にループする)
            #if(i == 0):
            #    print("テスト動作のため最初の0回目で強制終了させる")
            #    return

        print("動作完了")
        self.time_entry.change_value(f"動作完了")


    def replace_move(self,string):
        print("辞書使用☑の状況",self.dict_chk.bln.get())
        
        
        if(self.dict_chk.bln.get() == True):
            print("入力欄ではなく辞書を使用して置換を行います")
            repdim2 = functions.opencsv("csv_replace_dict/*.csv")

            result_html = string
            for row in repdim2:
                print(row)
                print("で置き換えます")
                #辞書の場合はサーチは0、リプレイスは1に入ってるのを1行ずつループする
                search = row[0]
                search = self.replace_by_dim2arr(search,self.set_easy_searchword_dim2)
    
                replace = row[1]

                result_html = re.sub(search,replace,result_html)


        else:
            print("入力欄を使用してRgxPtnを生成します")
            #UIから取得したワードをかんたんrgx変換辞書で成形してptnを生成する
            search = self.targetstr_entry.entry.get()
            search = self.replace_by_dim2arr(search,self.set_easy_searchword_dim2)

            #置き換え側は記憶変数がもしあれば\1で入力するのみなのでいじらない
            replace = self.replacestr_entry.entry.get()

            print(f"【{search}】を置き換えます")

            result_html = re.sub(search,replace,string)

        return result_html


    def hiddensys_act(self):
        print("hidden window OPEN")
        #ここに新規ウインドウを開くmethodと、閉じられたときにインスタンスを破壊するように仕込む
        #ウインドウにはテキストUI2つと開始ボタンをセットし、左に元テキストを入れて辞書データからの置き換えが終わったStringを
        #右側のテキストUIに返す


def main():
    print("メイン関数の展開実験")

    ins = Galaxy()


    ins.main_window.root.mainloop()


main()