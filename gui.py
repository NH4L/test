from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import os
import fnmatch
from tkinter.scrolledtext import ScrolledText


def search():
    ent_search_value = ent_search.get()
    ent_type_value = ent_type.get()
    if not ent_search_value or not ent_type_value:
        tkinter.messagebox.showerror('警告','请把关键字和类型输入完整再搜索')
        return
    path = tkinter.filedialog.askdirectory()
    fnlist = os.walk(path)              #列出文件夹下的文件和子文件夹
    for root,dirs,files in fnlist:
        for i in fnmatch.filter(files,ent_type_value):
            fn = '%s/%s' %(root,i)
            fn = fn.replace('\\','/')
            f = open(fn,encoding='UTF-8')
            if ent_search_value in f.read(): #if 'a' in 'abc':
                listBox.insert(END,fn)
                f.close()

def edit(e):
    fn  = listBox.get(listBox.curselection())
    fileWindow = Tk()
    fileWindow.geometry('+500+200')
    text = ScrolledText(fileWindow,width = 80,height = 40)
    fileWindow.mainloop()
    text.grid()
    text.insert(INSERT,open(fn,encoding='UTF-8').read())
    fileWindow.mainloop()

root = Tk()
root.title('文件搜索软件')
root.geometry('+500+300')
Label(root,text = '关键字:').grid(row = 0,column = 0)
ent_search = Entry()
ent_search.grid(row = 0,column = 1)
Label(root, text='类型:').grid(row=0, column=2)
ent_type = Entry()
ent_type.grid(row=0, column=3)
btn = Button(root,text = '搜索',command = search)
btn.grid(row=0, column=4)

listBox = Listbox(root,width = 60)
listBox.bind('<Double-Button-1>',edit)
listBox.grid(row = 1,columnspan = 5)

root.mainloop()
