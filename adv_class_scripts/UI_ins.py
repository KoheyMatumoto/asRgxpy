import tkinter
from tkinter.constants import W
import tkinter.ttk as ttk
import tkinter.scrolledtext


from tkinter import messagebox

class UI_WINDOW:
    def __init__(self,title,width,height,imgpath=""):
        self.root = tkinter.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(0,0)

        if(imgpath ==""):
            pass
        else:
            self.window_bg_img = tkinter.PhotoImage(file =imgpath)
            self.bgLabel = tkinter.Label(self.root,image=self.window_bg_img)
            self.bgLabel.place(x=0,y=0,relwidth=1,relheight=1)


class _LABEL:
    def __init__(self,x,y,txt, charcolor="black",bgcolor =None):
        self.posx = x
        self.posy = y

        self.label = tkinter.Label(
            text = txt,
            fg=charcolor,
            bg=bgcolor           
            )

class UI_CANVAS:
    def __init__(self,window,txt,w=200,h=25):
        self.canvas = tkinter.Canvas(
            window,
            width = w,
            height = h,
            bg = "cyan"
        )
        self.canvas.pack()
        self.canvas.create_text(100,10,text=txt)



class SET_UI_LABEL(_LABEL):
    def __init__(self,x,y,txt, charcolor="black",bgcolor =None):
        super().__init__(x,y,txt, charcolor,bgcolor)
        self.label.place(x=self.posx, y=self.posy)

class SET_UI_ENTRY(_LABEL):
    def __init__(self,x,y,txt,length=20, visible=True, charcolor="black",bgcolor =None):
        super().__init__(x,y,txt, charcolor,bgcolor)

        #とりあえず動作スタートのUIを考える
        if(visible == True):
            self.entry = tkinter.Entry(width = length)
        else:
            self.entry = tkinter.Entry(width = length, show="*")

        #ラベルなしのパターンもあってもいい
        if(txt==""):
            pass
            self.entry.place(x=self.posx, y=self.posy)

        else:
            self.entry.place(x=self.posx, y=self.posy+20)
            self.label.place(x=self.posx, y=self.posy)
            

    def change_value(self,add):
        self.entry.delete(0,tkinter.END)
        self.entry.insert('end',add)
        self.entry.update()




class SET_UI_COMBO(_LABEL):
    def __init__(self,x,y,txt,chooselist, length=40, charcolor="black",bgcolor =None):
        super().__init__(x,y,txt, charcolor,bgcolor)
        self.combo = ttk.Combobox(state="readonly",width=length)
        self.combo["values"] = chooselist

        #ラベルなしのパターンもあってもいい
        if(txt==""):
            pass
            self.combo.place(x=self.posx, y=self.posy)

        else:
            self.button.place(x=self.posx, y=self.posy+20)
            self.label.place(x=self.posx, y=self.posy)


class SET_UI_BTN(_LABEL):
    def __init__(self,x,y,txt,function,btntxt,iro,btnfontsize, charcolor="black",bgcolor =None):
        super().__init__(x,y,txt, charcolor,bgcolor)
        self.button =tkinter.Button(text=btntxt,font =("Times New Roman",btnfontsize),bg=iro ,command=function)

        #ラベルなしのパターンもあってもいい
        if(txt==""):
            pass
            self.button.place(x=self.posx, y=self.posy)

        else:
            self.button.place(x=self.posx, y=self.posy+20)
            self.label.place(x=self.posx, y=self.posy)
            


#マジでこれ注意！スクロールテキストエリアの値は1文字目から最後の1文字まで　を取得するように指定しないとエラー
#nowtext = self.schedule_area.textarea.get("1.0","end-1c")
class SET_UI_TEXTAREA(_LABEL):
    def __init__(self,x,y,txt,width_charnum,height_charnum, charcolor="black",bgcolor =None):
        super().__init__(x,y,txt, charcolor,bgcolor)
        self.textarea = tkinter.scrolledtext.ScrolledText(width = width_charnum, height = height_charnum ,fg=charcolor, bg=bgcolor)

        #ラベルなしのパターンもあってもいい
        if(txt==""):
            pass
            self.textarea.place(x=self.posx, y=self.posy)

        else:
            self.textarea.place(x=self.posx, y=self.posy+20)
            self.label.place(x=self.posx, y=self.posy)

    #動くかどうか未デバッグ。Entryのコピーしただけ
    def change_value(self,add):
        self.textarea.delete("1.0",tkinter.END)
        self.textarea.insert('end',add)
        self.textarea.update()

    def make_array_from_input_bylines(self):
        nowarray = ""
        splitstr = self.textarea.get("1.0","end-1c")
        nowarray = splitstr.splitlines()
        return nowarray



#ここも注意点。チェックの状況を取得するときは.checkbox.getではなく、instance.bln.get()とする
class SET_UI_CHKBOX(_LABEL):
    def __init__(self,x,y,txt,bool, charcolor="black",bgcolor =None):
        super().__init__(x,y,txt, charcolor,bgcolor)
        self.bln = tkinter.BooleanVar()
        self.bln.set(bool)
        self.checkbox = tkinter.Checkbutton(text=txt,variable=self.bln)
        self.checkbox.place(x=self.posx, y=self.posy)



#ホップアップウインドウなどにプログレスを出すにはwindowrootがどうしても必要となるため、呼び出し側でuiwindowname.rootを引数に持たせる必要がある点に注意
class SET_UI_PROGRESSBAR():
    def __init__(self,windowroot,x,y,barlength=300,volume=100):
        self.maxvolume=volume
        self.progressbar = ttk.Progressbar(windowroot,orient="horizontal",length=barlength,mode="determinate")
        self.progressbar.place(x=x,y=y)
        self.bar_value = 0
        self.progressbar.configure(maximum=volume,value=self.bar_value)

    def plus_value(self,plusvolume):
        self.bar_value = self.bar_value + plusvolume 
        if(self.bar_value > self.maxvolume):
            print("progress bar is max.")
            self.bar_value = self.maxvolume
            self.progressbar.configure(value=self.bar_value)
            self.progressbar.update()
        else:
            self.progressbar.configure(value=self.bar_value)
            self.progressbar.update()

    def change_value(self,newvalue):
        self.bar_value = newvalue
        if(self.bar_value > self.maxvolume):
            print("progress bar is max.")
            self.bar_value = self.maxvolume
            self.progressbar.configure(value=self.bar_value)
            self.progressbar.update()
        else:
            self.progressbar.configure(value=self.bar_value)
            self.progressbar.update()


        

class SET_UI_messagebox():
    def __init__(self,boxtitle,messtext,type="showinfo"):
        if(type=="showinfo"):
            messagebox.showinfo(boxtitle,messtext)
