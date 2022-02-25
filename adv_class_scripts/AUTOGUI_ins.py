import tkinter
import pyautogui

from time import sleep
import sys
import random



class _MATH_POINT:
    def __init__(self):
        print("座標・時間計算関係")


    def randarea_set(self,set_x,set_y,difference):
        rx = random.randint(0,difference)-(difference/2)
        ry = random.randint(0,difference)-(difference/2)

        resultx = int(set_x) + int(rx)
        resulty = int(set_y) + int(ry)

        return resultx,resulty

    def randtime(self,a,b):
        #a~bの数字の中のランダムから1000分の1
        time= random.randint(a,b)/1000
        return time

    def randwait_ms(self,min,max):
        w=self.randtime(min,max)
        print(f"待機時間:{w}")
        sleep(w)
        return w

    def rand_percent_of_100(self):
        p=random.randint(0,100)
        print(f"{p}％が選ばれました。")
        return p


class _CHECK_IMG_POINT:
    def __init__(self):
        print("画像認証ループ系")
    def chkimg(self,imgpath,sharpness):
        print(f"精度{sharpness}で認証を行います")
        try:
            x,y = pyautogui.locateCenterOnScreen(imgpath,confidence=sharpness)
            print("検出成功")
            print(x,y)
            return x,y
        except Exception as ex:
            print("画像の検出に失敗しました")
            print(ex)
            return None,None

    def chkimg_tryloop(self,imgpath,trynum,sharpness):
        errornum = 0
        while(True):
            self.randwait_ms(200,400)
            g_imgx,g_imgy = self.chkimg(imgpath,sharpness)
            if(g_imgx == None or g_imgy == None):
                errornum +=1
                print(f"画像認証結果の座標にNoneが含まれています。エラーカウント{errornum}/{trynum}")
        
            else:
                print("gimg xyにエラーがないので先へ進めます")
                break
            if(errornum >trynum):
                print("フェイタルエラー")
                print(f"{imgpath}の画像が{errornum}/{trynum}回見つかりませんでした。")
                sys.exit()
        #ブレイク出来た場合だけ座標を握ってreturnできる
        return g_imgx,g_imgy

    #画面全体ではなく、特定のエリア内で画像認証をする場合はここ
    def chkimg_areafocus(self,imgpath,sharpness,x1,y1,width,height):
        print(f"範囲({x1},{y1})~({x1+width},{y1+height})内で、精度{sharpness}で認証を行います")
        try:
            x,y = pyautogui.locateCenterOnScreen(imgpath,region=(x1,y1,width,height),confidence=sharpness)
            print("検出成功")
            print(x,y)
            return x,y
        except Exception as ex:
            print("画像の検出に失敗しました")
            print(ex)
            return None,None


    def chkimg_areafocus_tryloop(self,imgpath,trynum,sharpness,x1,y1,width,height):
        errornum = 0
        while(True):
            self.randwait_ms(200,400)
            g_imgx,g_imgy = self._areafocus(imgpath,sharpness,x1,y1,width,height)
            if(g_imgx == None or g_imgy == None):
                errornum +=1
                print(f"画像認証結果の座標にNoneが含まれています。エラーカウント{errornum}/{trynum}")
        
            else:
                print("gimg xyにエラーがないので先へ進めます")
                break
            if(errornum >trynum):
                print("フェイタルエラー")
                print(f"{imgpath}の画像が{errornum}/{trynum}回見つかりませんでした。")
                sys.exit()
        #ブレイク出来た場合だけ座標を握ってreturnできる
        return g_imgx,g_imgy

    def chkimg_tryloop_noexit(self,imgpath,trynum,sharpness):
        errornum = 0
        while(True):
            self.randwait_ms(200,400)
            g_imgx,g_imgy = self.chkimg(imgpath,sharpness)
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





class AUTOGUI(_MATH_POINT,_CHECK_IMG_POINT):
    def __init__(self):
        super().__init__()
        self.pyautogui.FAILSAFE=False
        print("マウス操作や画像認証・ランダム入りキーボード入力操作などが可能になります。")


    def mmv_random(self,to_x,to_y,second=2,square=5):
        x,y=self.randarea_set(to_x,to_y,square)
        pyautogui.moveTo(x,y,second,pyautogui.easeInQuad)

    #クリックしたい場所をランダム化したいときに必須の動きがワンセット(ベースx、ベースy ずらす正方形幅、,マウス移動時間、クリック後に逃がす向き、逃がす遠さ)で定義され、最後の2引数は0,0なら逃がさず終えることも可能
    #所要時間はmmvtimes x 2秒となる
    def gui_random_corrected_motion_clickmove(self,basex,basey,square=2,mmvtime=2,enddirection="key5",escapescall=1):
        print(f"元座標({basex},{basey})にランダム正方形エリア{square}以内の補正をかけます.({mmvtime}秒かけてマウスムーブ)")
        cl_x,cl_y =self.randarea_set(basex,basey,square)
        print(f"変換後座標({cl_x},{cl_y})となりました。")

        pyautogui.moveTo(cl_x,cl_y,mmvtime,pyautogui.easeInQuad)
        pyautogui.click()

        #テンキーの数字の向きであらわされる引数でディレクションを確定させる.キー以外のものが入ったときはマウス捨てなしでパスする
        scale = 100 * escapescall
        if(enddirection == "key7"):
            print(f"クリックしたらマウスカーソルをランダムに捨てる(フラグ7に沿って捨てます){enddirection}")
            escmouse_x,escmouse_y = self.randarea_set(-1*scale,-1*scale,50)
            pyautogui.moveRel(escmouse_x,escmouse_y, mmvtime)
        elif(enddirection == "key9"):
            print(f"クリックしたらマウスカーソルをランダムに捨てる(フラグ9に沿って捨てます){enddirection}")
            escmouse_x,escmouse_y = self.randarea_set(scale,-1*scale,50)
            pyautogui.moveRel(escmouse_x,escmouse_y, mmvtime)
        elif(enddirection == "key3"):
            print(f"クリックしたらマウスカーソルをランダムに捨てる(フラグ3に沿って捨てます){enddirection}")
            escmouse_x,escmouse_y = self.randarea_set(scale,scale,50)
            pyautogui.moveRel(escmouse_x,escmouse_y, mmvtime)
        elif(enddirection == "key1"):
            print(f"クリックしたらマウスカーソルをランダムに捨てる(フラグ1に沿って捨てます){enddirection}")
            escmouse_x,escmouse_y = self.randarea_set(-1*scale,scale,50)
            pyautogui.moveRel(escmouse_x,escmouse_y, mmvtime)
        elif(enddirection == "key5"):
            print(f"クリックしたらマウスカーソルを移動せずその場に置く(フラグ5に沿って捨てます){enddirection}")
        else:
            print(f"クリック後処理に使うディレクションキーが定義されていません。{enddirection}")
            pass


    def scroll_by_pgdownkey(self,loops,chains,waitmin,waitmax):
        for i in range(loops):
            for k in range(chains):
                print(f"{chains}連打:Pagedown")
                pyautogui.press('pagedown')
                self.randwait_ms(100,600)
            self.randwait_ms(waitmin,waitmax)
            pyautogui.click()

