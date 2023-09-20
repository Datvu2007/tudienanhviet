from tkinter import *
from tkinter import messagebox
from googletrans import Translator
from tkinter.filedialog import asksaveasfile
from tkinter.simpledialog import askstring
import pyperclip
import json,pyttsx3
import threading
import webbrowser

bg_color='#C1CDCD'
root = Tk()
root.geometry("735x480")
root.iconphoto(False, PhotoImage(file = "icon/icon.png"))
root.title("Từ Điển Anh - Việt")
root.configure(bg=bg_color)

speach = pyttsx3.init()

with open('data/en-vi.json','r',encoding='utf-8') as f:
    file=json.load(f)

tmp_search=''
def get_word_suggestions():
    for i in lst_w.curselection():
        if lst_w.get(i)!='':
            lst_w.selection_clear(0, END)
            search.delete(0,END)
            search.insert(0,lst_w.get(i))
    root.after(500, get_word_suggestions)

def say(text):
    speach.say(text)
    speach.runAndWait()

def trans(w):
    global speach_w
    speach_w=w
    try:
        vi= Translator().translate(w, src='en', dest='vi').text
        msg='Kết quả từ Google dịch:\n\n- - - -\n  EN: '+w+'\n  VN: '+vi+'\n- - - -\n\nBạn có muốn copy nó?'
        kq.delete(1.0, END)
        result_text.config(text ="kết quả cho '"+w+"'")
        kq.insert(1.0, 'EN: '+w+'\nVI: '+vi)
        ms=messagebox.askquestion("Kết quả từ Google dịch", msg)
        if ms=='yes':
            pyperclip.copy('EN: '+w+'\n---VI: '+vi)
    except:
        messagebox.showinfo("DatPC", "lỗi khi dịch! xem lại kết nối internet và thử lại!")


def find(w):
    for kw in file:
         if w==kw:
             return file[w]
    return ''
def bground():
    global goi_y,tmp_search
    goi_y=[]
    try:t=search.get()
    except:t=''
    if tmp_search!=t:
        tmp_search=t
        if t!='':
            for kw in file:
                if t in kw:
                    for i in range(len(t)):
                        if t[i]!=kw[i]:
                            break
                    else:
                        goi_y.append(kw)
                if len(goi_y)>29:
                    break
        lst_w.delete(0, END)
        for i in range(30):
            try:
                lst_w.insert(i, goi_y[i])
            except:
                lst_w.insert(i, '')
        
    root.after(500, bground)

def btn_copy():
    pyperclip.copy(kq.get(1.0,END))
    messagebox.showinfo("DatPC", "Copy Done!")
def clear_search_bar():
    search.delete(0,END)
def spk_w():
    threading.Thread(target=say, args=(speach_w,)).start()
def trans_get():
    threading.Thread(target=trans, args=(search.get(),)).start()
def get_search():
    global speach_w
    w=search.get()
    speach_w=w
    kqtxt=find(w)
    kq.delete(1.0, END)
    result_text.config(text ="kết quả cho '"+w+"'")
    if kqtxt=='':
        kq.insert(1.0, 'Không có kết quả!')
    else:
        kq.insert(1.0, w+'\n---\n'+kqtxt)
def clear_kq():
    kq.delete(1.0,END)
def save_file():
    try:
        path=asksaveasfile(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")]).name
        with open(path,'w',encoding='utf-8') as wf:
            wf.write(kq.get(1.0,END))
    except:
        pass

speach_w=''

def menu_find():
    w = askstring("Input", "Nhập từ bạn muốn tìm")
    if w==None or w=='':
        search.delete(0,END)
        search.insert(0,'')
        kq.insert(1.0, '')
    else:
        kqtxt=find(w)
        search.delete(0,END)
        search.insert(0,w)
        if kqtxt=='':
            kq.insert(1.0, 'Không có kết quả!')
        else:
            kq.insert(1.0, w+'\n---\n'+kqtxt)
def clr_all():
    clear_search_bar()
    clear_kq()
def openfb():
    webbrowser.open('https://fb.com/100046763600557')
def openweb():
    webbrowser.open('https://datweb.notion.site/datweb/WELCOME-TO-DAT-WEBSITE-5b546212a21d456595bbc86b074bde04')
def openinf():
    webbrowser.open('https://bit.ly/m/Datinfor')
def showabout():
    messagebox.showinfo("DatPC","Từ Điển Anh Việt By DatPC\n\nLiên hệ\
 tác giả:\n- FB: fb.com/10004676360055\n- Website: bit.ly/Datweb")
def trans_box():
    w = askstring("Input", "Từ cần dịch")
    if w==None:
        search.delete(0,END)
        search.insert(0,'')
        kq.insert(1.0, '')
    else:
        try:
            vi=Translator().translate(w, src='en', dest='vi').text
            msg='Kết quả từ Google dịch:\n\n- - - -\n  EN: '+w+'\n  VN: '+vi+'\n- - - -\n\nBạn có muốn copy nó?'
            ms=messagebox.askquestion("Kết quả từ Google dịch", msg)
            if ms=='yes':
                pyperclip.copy('EN: '+w+'\n---VI: '+vi)
        except:
            messagebox.showinfo("DatPC", "lỗi khi dịch! xem lại kết nối internet và thử lại!")
def showtinhnang():
    tinhnang='\n\n'.join('''Các tính năng chính:
- Thanh tìm kiếm: nhập từ khóa bạn muốn tìm kiếm
- Clear search bar: xóa trắng thanh tìm kiếm
- Google dịch: dịch từ trong ô tìm kiếm
- Tìm kiếm: tìm kiếm kết quả cần tìm của từ khóa
- Clear: xóa kết quả
- Copy: copy kết quả
- Đọc: đọc từ khóa bằng tiếng anh
- lưu: lưu kết quả thành file
'''.split('\n'))
    messagebox.showinfo("Các tính năng", tinhnang)
menu_bar = Menu(root)

tool_menu = Menu(menu_bar,tearoff=False)
tool_menu.add_command(label='Clear',command=clr_all)
tool_menu.add_command(label='Tìm kiếm',command=menu_find)
tool_menu.add_command(label='Dịch',command=trans_box)
tool_menu.add_command(label='Lưu',command=save_file)
tool_menu.add_command(label='Thoát',command=root.destroy)

more = Menu(menu_bar,tearoff=False)
more.add_command(label='Các tính năng',command=showtinhnang)
more.add_command(label='About',command=showabout)
more.add_command(label='Facebook DatPC',command=openfb)
more.add_command(label='Website DatPC',command=openweb)
more.add_command(label='Other infor DatPC',command=openinf)

menu_bar.add_cascade(label="File",menu=tool_menu)
menu_bar.add_cascade(label="File",menu=more)

root.config(menu=menu_bar)

search_text=Label(root, text='Thanh tìm kiếm',bg=bg_color)
search_text.place(x=0,y=5)

search = Entry(root)
search.place(x=90,y=6,width=350)

clear_btn=Button(root, text = 'Clear search bar',command=clear_search_bar)
clear_btn.place(x=445,y=3,width=95)

trans_btn=Button(root, text = 'Google dịch',command=trans_get)
trans_btn.place(x=545,y=3,width=80)

search_btn=Button(root, text = 'Tìm kiếm',command=get_search)
search_btn.place(x=630,y=3,width=100)

scrlbar = Scrollbar(root)
scrlbar.place(x=0,y=35,height=440)
lst_w=Listbox(root)
lst_w.place(x=20,y=35,width=200,height=440)
lst_w.config(yscrollcommand = scrlbar.set)
scrlbar.config(command = lst_w.yview)

kq=Text(root)
kq.place(x=230,y=70,width=500,height=405)

result_text=Label(root, text='',bg=bg_color)
result_text.place(x=230,y=47)

clear_kq_btn=Button(root, text = 'Clear',command=clear_kq)
clear_kq_btn.place(x=515,y=40,width=50)
copy_btn=Button(root, text = 'Copy',command=btn_copy)
copy_btn.place(x=570,y=40,width=50)
speach_btn=Button(root, text = 'Đọc',command=spk_w)
speach_btn.place(x=625,y=40,width=50)
save_btn=Button(root, text = 'Lưu',command=save_file)
save_btn.place(x=680,y=40,width=50)

bground()
get_word_suggestions()
root.resizable(False,False)
root.mainloop()