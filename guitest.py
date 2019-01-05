import queue
from mimetypes import guess_type
from tkinter import Frame, Entry, Listbox, Button, StringVar, Scrollbar, Tk
from tkinter.font import families
from threading import Thread
from tkinter.constants import *
from tkinter.filedialog import askdirectory
import os

DEFAULT_FONT = ('微软雅黑', 11, 'normal')


class Searcher(Frame):
    """ Keyword Searcher
    This is a very simple python program, which is designed for finding specified key-word
    in files. Just for fun!
    """

    def __init__(self, master=None, cnf={}, **kwargs):
        super(Searcher, self).__init__(master, cnf, **kwargs)
        self._root_path_var = StringVar()
        self._keyword_var = StringVar(self)
        self._listbox = None
        self._result_queue = None
        self.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        self.make_widgets()
        self._consumer()

        # config for main window
        self.master.title('Keyword Searcher')

    def make_widgets(self):
        frm1 = Frame(self)
        frm1.pack(side=TOP, fill=X)
        Entry(frm1, textvariable=self._root_path_var, font=DEFAULT_FONT).pack(side=LEFT, fill=X, expand=YES)
        Button(frm1, text='Add directory', font=DEFAULT_FONT,
               command=lambda: self._root_path_var.set(askdirectory(title='Add directory'))).pack(side=RIGHT)

        frm2 = Frame(self)
        frm2.pack(side=TOP, fill=X)
        keyword_ent = Entry(frm2, textvariable=self._keyword_var, font=DEFAULT_FONT)
        keyword_ent.pack(side=LEFT, fill=X, expand=YES)
        Button(frm2, text='Find', font=DEFAULT_FONT, command=self.find).pack(side=RIGHT)

        vs = Scrollbar(self)
        hs = Scrollbar(self)
        self._listbox = Listbox(self)
        vs.pack(side=RIGHT, fill=Y)
        vs.config(command=self._listbox.yview)
        hs.pack(side=BOTTOM, fill=X)
        hs.config(command=self._listbox.xview, orient='horizontal')
        self._listbox.config(yscrollcommand=vs.set, xscrollcommand=hs.set,
                             font=DEFAULT_FONT)
        self._listbox.pack(fill=BOTH, expand=YES)
        self._listbox.bind('<Double-1>', self._navigate_to)

    def find(self):
        self._result_queue = queue.Queue()
        self._listbox.delete('0', 'end')
        Thread(target=self._find, args=(self._root_path_var.get(),
                                        self._keyword_var.get()), daemon=True).start()

    def _find(self, path, keyword):
        if not os.path.exists(path):
            return None

        for this_dir, sub_dirs, files in os.walk(path):
            for file in files:
                file_type = guess_type(file)[0]
                if file_type and 'text' in file_type:
                    fp = os.path.join(this_dir, file)
                    self._result_queue.put(fp) if keyword in open(fp).read() else None

    def _consumer(self):
        if self._result_queue:
            try:
                fp = self._result_queue.get(block=False)
            except queue.Empty:
                pass
            else:
                self._listbox.insert('end', fp)
                # auto scroll.
                self._listbox.yview('end')

        self.after(100, self._consumer)

    def _navigate_to(self, event):
        """
        Only works on Ubuntu platform currently.
        Double click to navigate to selected path.
        It's a very convenient function.
        :return: None
        """
        print(event)
        # get active item from listbox
        path = self._listbox.get('active')
        print(path)

        # open nautilus with param path, before that, check your platform.
        if 'ubuntu' in (os.popen('uname -a').read()).lower():
            os.system('/usr/bin/nautilus {}'.format(path))
        else:
            pass


def main():
    root = Tk()
    Searcher(root)
    root.mainloop()


if __name__ == '__main__':
    main()