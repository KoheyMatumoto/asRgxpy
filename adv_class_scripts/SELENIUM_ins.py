from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


from time import sleep
import pyautogui
import pydirectinput as di
import sys
import random

#オートGUIclassを実装したことによってここのベーシックアクションは要らなくなりつつある
#べーじっくアクションではランダム待機やランダム座標の計算とGUI系統についての動作をまとめる(BOTやセレニウムに継承できるようなカタチで定義している)
class BASIC_ACT():
    def __init__(self):
        pass

    def looptab(self,loopcount):
        #0.02sから0.04sのランダム
        for i in range(loopcount):
            sleep(self.randtime(20,40))
            pyautogui.press('tab')

    #何のためのメソッドなのかいまいちわからなくなってる。
    def chkimg_tryloop_twitterspecial_ptn(self,imgpath,trynum,sharpness,x1,y1,width,height):
        errornum = 0
        while(True):
            self.randwait_ms(200,400)
            g_imgx,g_imgy = self.chkimg_areafocus(imgpath,sharpness,x1,y1,width,height)
            if(g_imgx == None or g_imgy == None):
                errornum +=1
                print(f"画像認証結果の座標にNoneが含まれています。エラーカウント{errornum}/{trynum}")
        
            else:
                print("gimg xyにエラーがないので先へ進めます")
                break
            if(errornum >trynum):
                print("画像認証エラー")
                print(f"{imgpath}の画像が{errornum}/{trynum}回見つかりませんでした。座標をNone,Noneとして処理を終えます。")
                return None,None
        #ブレイク出来た場合だけ座標を握ってreturnできる
        return g_imgx,g_imgy



class SELENIUM_ACT(BASIC_ACT):
    def __init__(self):
        super().__init__()
        print("selenium Ready.")

    def start(self,url,origins_diff=0):
        #self.driver.get('https://www.google.com/')
        self.options =Options()
        self.driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe',options=self.options)
        self.driver.implicitly_wait(15)
        self.driver.set_window_size(1400,1080)
        self.driver.set_window_position(240+origins_diff,20+origins_diff)

        sleep(1)
        self.driver.get(url)
        sleep(1)

    def start_by_headless(self,url,origins_diff=0):
        #self.driver.get('https://www.google.com/')
        self.options =Options()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome('../phoenixians_insta/chromedriver_win32/chromedriver.exe',options=self.options)
        self.driver.implicitly_wait(15)
        self.driver.set_window_size(1400,1080)
        self.driver.set_window_position(240+origins_diff,20+origins_diff)

        sleep(1)
        self.driver.get(url)
        sleep(1)

    def jump(self,url):
        sleep(1)
        self.driver.get(url)
        sleep(1)

    def wait_for_full_load(self,timeout):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located)

    def fullscreen(self):
        self.driver.maximize_window()

    def gethtmlBySelector(self,selector,rule = "1st"):
        print(f"★try to get attribute values of the current pages class:{selector} , rule ={rule}")
        
        if(rule =="all"):
            try:
                self.target = self.driver.find_elements_by_css_selector(selector)
                print(f"{len(self.target)}箇所ヒットセレクタを検出しました。")
                #for data in self.target:#オールヒットの時はセレクタが多すぎるとループがやばいので今回はPrintなし
                    #print(data.get_attribute("innerHTML"))
            except Exception as err:
                print(err)
                self.target = "did not match as your selector"
        elif(rule =="1st"):
            try:
                self.target = self.driver.find_element_by_css_selector(selector)
                print(self.target.get_attribute("innerHTML"))
                print("を1番目に検出しました。")
            except Exception as err:
                print(err)
                self.target = "did not match as your selector"

        else:
            print("error gethtmlBySelector!!!")
            sys.exit()

        return self.target

    def enter_element(self,element):
        try:
            element.click()
        except:
            print("faild... click.")

        try:
            element.submit()
        except:
            print("faild... submit.")




    #エレメントの座標を取得し、return pos をAUTOGUIと連携することでWIN32APIによる入力
    #DIRECTINPUTと連携することでDirectXによる入力ができる。BOT対策の対策などに。
    def getElementPoint(self,elem):
        pos = elem.location
        print(f"1番目投稿エレメントの存在する座標：{pos}")
        #カレントウィンドウの座標(左上隅の座標)を取得
        coordinate = self.driver.get_window_position()
        #取得した座標を表示
        print(f"カレントウインドウ座標{coordinate}とブラウザの高さ120pxを加える")
        pos["x"] = pos["x"]+coordinate["x"]
        pos["y"] = pos["y"]+coordinate["y"]+120
        return pos


    #ウインドウハンドルを取得する(ウインドウハンドルは2つ以上のブラウザウインドウが開かれたときに必要になる。複数ウインドウ)
    def windowhandles(self):
        handle_array = self.driver.window_handles
        print(handle_array)
        return handle_array

    #取得したハンドルを使用してセレニウムアクティブウインドウを切り替える
    def change_active_window(self,handle):
        self.driver.switch_to_window(handle)



    #Seleniumには、selenium.webdriver.common.action_chains.ActionChainsクラスが準備されています。
    #ActionChainsクラスは、Shiftを押下しながら入力といった特殊な処理はもちろん、F1やF3など特殊なキー操作を行うことができます。
    #もちろん、通常のクリック処理や値の設定も行うことができます。
    #ActionChainsクラスは、各メソッドを実行するごとにキューに操作を貯めます。そして、perform関数が実行された時点で今まで貯めていたキュー
    #の操作をまとめて実行します。また、ActionChainsインスタンスの関数は、自身を返却するのでメソッドチェーンで記述することができます。
    def scroll_to_element(self,element):
        #スクロール方法1
        print("スクロール先 Y座標",element.location["y"])
        self.driver.execute_script(f'window.scrollTo(0,{element.location["y"]});')


    #javascriptのクエリーセレクターで反応できるcssセレクタを送り、その対象HTMLを破壊する。様々な認証の突破やオーバーレイ、スクロールできないページやモーダルウインドウに使う
    def element_destroyer(self,css_selectorjs):
        nowjscode_target_red = (f"""\
            t = document.querySelector('{css_selectorjs}');\
            t.style.backgroundColor="red";\
            """)
        nowjscode_target_blue = (f"""\
            t = document.querySelector('{css_selectorjs}');\
            t.style.backgroundColor="blue";\
            """)
        nowjscode_target_purple = (f"""\
            t = document.querySelector('{css_selectorjs}');\
            t.style.backgroundColor="purple";\
            """)

        nowjscode_delete= (f"""\
            t = document.querySelector('{css_selectorjs}');\
            t.remove();""")
        
        self.driver.execute_script(nowjscode_target_red)
        sleep(0.1)
        self.driver.execute_script(nowjscode_target_purple)
        sleep(0.1)
        self.driver.execute_script(nowjscode_target_blue)
        sleep(0.1)
        self.driver.execute_script(nowjscode_target_purple)
        sleep(0.1)
        self.driver.execute_script(nowjscode_target_red)
        sleep(0.1)
        self.driver.execute_script(nowjscode_target_purple)
        sleep(0.1)
        self.driver.execute_script(nowjscode_target_blue)
        sleep(0.1)
        self.driver.execute_script(nowjscode_target_purple)
        sleep(0.1)
        self.driver.execute_script(nowjscode_target_red)
        sleep(0.1)

        self.driver.execute_script(nowjscode_delete)
        print("ターゲット破壊完了")
        sleep(1)

    def endselenium(self):
        self.driver.close()
        self.driver.quit()




#以降、セレニウムでワードプレスを操作するためだけのclass。
#上記のセレニウムクラスを継承したワードプレスクラスとする。ワードプレス定義には専用のcsvファイルを使用する(フォルダ同梱)



try:
    import functions
except:
    pass
try:
    from adv_class_scripts import functions
except:
    pass

import pyperclip

class WORDPRESS_SELENIUM(SELENIUM_ACT):
    def __init__(self,wp_config_dim2):
        super().__init__()
        print("WordPress datacsv full load")
        self.wpurl = functions.vlookup_from_2dim_array(wp_config_dim2,"wpurl",1)
        self.wpid = functions.vlookup_from_2dim_array(wp_config_dim2,"wpid",1)
        self.wppw = functions.vlookup_from_2dim_array(wp_config_dim2,"wppw",1)

        self.wp_login_id_areas_selector = functions.pick_value_from_2dim_array(wp_config_dim2,"wp_login_id_areas_selector")
        self.login_id_areas_value = functions.pick_value_from_2dim_array(wp_config_dim2,"login_id_areas_value")

        self.wp_login_pw_areas_selector = functions.pick_value_from_2dim_array(wp_config_dim2,"wp_login_pw_areas_selector")
        self.login_pw_areas_value = functions.pick_value_from_2dim_array(wp_config_dim2,"login_pw_areas_value")

        self.wp_title_areas_selector = functions.pick_value_from_2dim_array(wp_config_dim2,"wp_title_areas_selector")
        self.title_areas_value = functions.pick_value_from_2dim_array(wp_config_dim2,"title_areas_value")

        self.wp_slug_areas_selector = functions.pick_value_from_2dim_array(wp_config_dim2,"wp_slug_areas_selector")
        self.slug_areas_value = functions.pick_value_from_2dim_array(wp_config_dim2,"slug_areas_value")

        self.wp_tag_areas_selector = functions.pick_value_from_2dim_array(wp_config_dim2,"wp_tag_areas_selector")
        self.tag_areas_value = functions.pick_value_from_2dim_array(wp_config_dim2,"tag_areas_value")

        self.wp_koukai_areas_selector = functions.pick_value_from_2dim_array(wp_config_dim2,"wp_koukai_areas_selector")
        self.koukai_areas_value = functions.pick_value_from_2dim_array(wp_config_dim2,"koukai_areas_value")

        self.wp_sitagaki_areas_selector = functions.pick_value_from_2dim_array(wp_config_dim2,"wp_sitagaki_areas_selector")
        self.sitagaki_areas_value = functions.pick_value_from_2dim_array(wp_config_dim2,"sitagaki_areas_value")

        self.wp_html_areas_selector = functions.pick_value_from_2dim_array(wp_config_dim2,"wp_html_areas_selector")
        self.html_areas_value = functions.pick_value_from_2dim_array(wp_config_dim2,"html_areas_value")

        self.wp_descri_areas_selector = functions.pick_value_from_2dim_array(wp_config_dim2,"wp_descri_areas_selector")
        self.descri_areas_value = functions.pick_value_from_2dim_array(wp_config_dim2,"descri_areas_value")

        self.wp_bassu_areas_selector = functions.pick_value_from_2dim_array(wp_config_dim2,"wp_bassu_areas_selector")
        self.bassu_areas_value = functions.pick_value_from_2dim_array(wp_config_dim2,"bassu_areas_value")

    #デバッグ用
    def printall(self):
        print([
            self.wpurl,
            self.wpid,
            self.wppw,
            self.wp_login_id_areas_selector,
            self.login_id_areas_value,
            self.wp_login_pw_areas_selector,
            self.login_pw_areas_value,
            self.wp_title_areas_selector,
            self.title_areas_value,
            self.wp_slug_areas_selector,
            self.slug_areas_value,
            self.wp_tag_areas_selector,
            self.tag_areas_value,
            self.wp_koukai_areas_selector,
            self.koukai_areas_value,
            self.wp_sitagaki_areas_selector,
            self.sitagaki_areas_value,
            self.wp_html_areas_selector,
            self.html_areas_value,
            self.wp_descri_areas_selector,
            self.descri_areas_value,
            self.wp_bassu_areas_selector,
            self.bassu_areas_value
        ])

    def try_login_wp(self):
        self.start(self.wpurl)
        print("send method")
        idArea = self.element_send(self.wp_login_id_areas_selector,self.login_id_areas_value,self.wpid)
        print("send method")
        pwArea = self.element_send(self.wp_login_pw_areas_selector,self.login_pw_areas_value,self.wppw)
        pwArea.submit()

    #知らないと解法が見つからないためドハマリするエラー。
    #current_urlのようなmethodではなくpropertyになってるやつらは()を付けるとエラーログからはまず解決できないタイプエラーを吐き出す。
    #sys.exit()などのようにかっこをつけてはいけない！
    def getnowurl(self):
        cur_url = self.driver.current_url
        return cur_url

    #記述を短縮するための関数
    def element_send(self,selector,attrbute_value,send_data):
        if(selector == "id"):
            print("css id check for",attrbute_value)
            try:
                target = self.driver.find_element_by_id(attrbute_value)
                sleep(0.25)
                target.send_keys(send_data)
            except:
                print("fail id send...") 
                print("could not send\n" + send_data + "\n------------------------------------")
                #sys.exit()

        elif(selector == "class"):
            print("css class check for",attrbute_value)

            try:
                target = self.driver.find_element_by_class_name(attrbute_value)
                sleep(0.25)
                target.send_keys(send_data)
            except:
                print("fail class send...") 
                print("could not send\n" + send_data + "\n------------------------------------")
                #sys.exit()
        elif(selector == "css_selector"):
            print("css css_selector check for",attrbute_value)

            try:
                target = self.driver.find_element_by_css_selector(attrbute_value)
                sleep(0.25)
                target.send_keys(send_data)
            except:
                print("fail css send...") 
                print("could not send\n" + send_data + "\n------------------------------------")
                #sys.exit()
        elif(selector == "name"):
            print("css name check for",attrbute_value)

            try:
                target = self.driver.find_element_by_name(attrbute_value)
                sleep(0.25)
                target.send_keys(send_data)
            except:
                print("fail name send...") 
                print("could not send\n" + send_data + "\n------------------------------------")
                #sys.exit()

        else:
            print("Fuck!!!!★Fatal Error! please check wp_login_pw_areas_selector in seleniums config.csv in wp_detaill_config")

        return target


    def element_paste(self,selector,attrbute_value,send_data):
        pyperclip.copy(send_data)

        if(selector == "id"):
            print("css id check for",attrbute_value)
            try:
                target = self.driver.find_element_by_id(attrbute_value)
                sleep(1)
                print("Press ctrl+V")
                target.send_keys(Keys.CONTROL,"v")
            except:
                print("fail id paste...")
                print("could not paste\n" + send_data + "\n------------------------------------")
                #sys.exit()

        elif(selector == "class"):
            print("css class check for",attrbute_value)
            try:
                target = self.driver.find_element_by_class_name(attrbute_value)
                sleep(1)
                print("Press ctrl+V")
                target.send_keys(Keys.CONTROL,"v")
            except:
                print("fail class paste...") 
                print("could not paste\n" + send_data + "\n------------------------------------")
                #sys.exit()

        elif(selector == "css_selector"):
            print("css css_selector check for",attrbute_value)
            try:
                target = self.driver.find_element_by_css_selector(attrbute_value)
                sleep(1)
                print("Press ctrl+V")
                target.send_keys(Keys.CONTROL,"v")
            except:
                print("fail css paste...") 
                print("could not paste\n" + send_data + "\n------------------------------------")
                #sys.exit()

        elif(selector == "name"):
            print("css name check for",attrbute_value)
            try:
                target = self.driver.find_element_by_name(attrbute_value)
                sleep(1)
                print("Press ctrl+V")
                target.send_keys(Keys.CONTROL,"v")
            except:
                print("fail name paste...") 
                print("could not paste\n" + send_data + "\n------------------------------------")
                #sys.exit()

        else:
            print("Fuck!!!!★Fatal Error! please check wp_login_pw_areas_selector in seleniums config.csv in wp_detaill_config")

        return target

    def sendtitle(self,title):
        print("send method")
        titArea = self.element_send(self.wp_title_areas_selector,self.title_areas_value,title)

    def sendslug(self,slug):
        print("send method")
        slugArea = self.element_send(self.wp_slug_areas_selector,self.slug_areas_value,slug)

    def sendtag(self,tag):
        print("send method")
        tagArea = self.element_send(self.wp_tag_areas_selector,self.tag_areas_value,tag)

    def pastehtml(self,html):
        print("paste method")
        pasteArea = self.element_paste(self.wp_html_areas_selector,self.html_areas_value,html)

    def senddescri(self,des):
        print("send method")
        descriptionArea = self.element_send(self.wp_descri_areas_selector,self.descri_areas_value,des)

    def pastedescri_yoast(self,des):
        print("paste maxa & mex special method")
        #現在のドライバでただのアクション(要素無のクリック等)を行う
        pyperclip.copy(des)
        self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight - document.documentElement.clientHeight);")
        print("move Endline")
        target = self.driver.find_element_by_css_selector('.InputContainer__VariableEditorInputContainer-fmvk3g-0.shared__DescriptionInputContainer-sc-4x7tml-1.cjbmvN')
        print("got target 3classArea")
        sleep(1)
        target.click()
        print("click")
        sleep(0.5)
        pyautogui.hotkey('ctrl','v')
        print("paste acted by autogui and wait")
        sleep(1)
        self.driver.execute_script("window.scrollTo(0,0);")

    def pastedescri_yoast_forMengym(self,des):
        print("paste maxa & mex special method")
        #現在のドライバでただのアクション(要素無のクリック等)を行う
        pyperclip.copy(des)
        self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight - document.documentElement.clientHeight);")
        print("move Endline")
        target = self.driver.find_element_by_css_selector('#replacement-variable-editor-field-7')
        print("got target idname7s area")
        sleep(1)
        target.click()
        print("click")
        sleep(0.5)
        pyautogui.hotkey('ctrl','v')
        print("paste acted by autogui and wait")
        sleep(1)
        self.driver.execute_script("window.scrollTo(0,0);")

    def pastedescri_forMengym(self,des):
        print("paste mengymdescri special method")
        #現在のドライバでただのアクション(要素無のクリック等)を行う
        pyperclip.copy(des)
        self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight - document.documentElement.clientHeight);")
        print("move Endline")
        target = self.driver.find_element_by_css_selector('[name="post_desc"]')
        print("got target idname7s area")
        sleep(1)
        target.click()
        print("click")
        sleep(0.5)
        pyautogui.hotkey('ctrl','v')
        print("paste acted by autogui and wait")
        sleep(1)
        self.driver.execute_script("window.scrollTo(0,0);")


    def sendbassu(self,bas):
        print("send method")
        bassuArea = self.element_send(self.wp_bassu_areas_selector,self.bassu_areas_value,bas)


    #publishで公開、save-postで下書き保存となる
    def hozon(self,boolen):
        if(boolen ==True):
            hozonButton = self.driver. find_element_by_id ("publish")
        else:
            hozonButton = self.driver. find_element_by_id ("save-post")

        #何が何でも上にスクロールさせる
        sleep(1.5)
        self.driver.execute_script("window.scrollTo(0,0);")
        hozonButton.click()
        sleep(2)