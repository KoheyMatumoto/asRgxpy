
import shutil
import re
import os
from time import sleep
import pandas as pd
import numpy as np



from adv_class_scripts import UI_ins
from adv_class_scripts import SELENIUM_ins
from adv_class_scripts import functions
from adv_class_scripts import GSPREAD_ins
from adv_class_scripts import AUTOGUI_ins
from adv_class_scripts import DATAFRAME_PD_ins

#from adv_class_scripts import SEARCH_CONSOLE_ins


class SET_UI(SELENIUM_ins.SELENIUM_ACT, 
                AUTOGUI_ins.AUTOGUI,
                GSPREAD_ins.GSPREAD):
    def __init__(self):
        super().__init__()

        print("i can put all ui.")
        self.infomation_string = "initialized_info"

        #ウインドウ定義
        self.main_window = UI_ins.UI_WINDOW("RR-Ranking wRighter",800,600,"img/backimg1.png")

        #左上UI
        #self.ranking_title_entry = UI_ins.SET_UI_ENTRY(65,125,"",42,True)

        self.start_btn = UI_ins.SET_UI_BTN(65,200,"",lambda: self.start_btn_act(),"*Start Action*","limegreen","14")

        self.order_column_entry = UI_ins.SET_UI_ENTRY(235,175,"解析対象csv index",10,True)
        self.order_column_entry.change_value(0)

        #右UI
        self.time_entry = UI_ins.SET_UI_ENTRY(410,125,"",40,True)

        self.infotext = UI_ins.SET_UI_TEXTAREA(410,190,"",40,15)
        self.infotext.change_value(self.infomation_string)




class Galaxy(SET_UI):
    def __init__(self):
        super().__init__()
        print("galaxy instance OK")
        self.csvpath = "csv_rank_data/*.csv"
        self.startbtn_flag = False


    def start_btn_act(self):
        if(self.startbtn_flag==False):
            print("スタート準備ができていません。フラグの確認。")
            return        
        print("start pushed")


        print("動作完了")





def main():
    print("メイン関数の展開実験")

    ins = Galaxy()


    ins.main_window.root.mainloop()


main()