import Tkinter as tk
import tkFileDialog
from os import path

class TopWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="TopWindow")
        label.grid(row=0, column=0)

class MiddleWindow(tk.Frame):
    
    def onFrameConfigure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)
    
    def CreateEntry(self):
        for i in range(50):
            self.buttons.append(tk.Label(self.frame, text="Middle"))
            self.buttons[i].pack()
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.scroll = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=tk.YES)
        self.frame.pack(side="left", fill="both", expand=tk.YES)
        self.canvas_frame = self.canvas.create_window((0,0), window=self.frame, anchor="n")
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(self.canvas))
        self.canvas.bind('<Configure>', self.FrameWidth)
        self.buttons = []
        self.CreateEntry()

class BottomWindow(tk.Frame):
    
    def askDirectory(self):
        self.dirname = tkFileDialog.askdirectory(**self.dir_opt)
        if self.dirname:
            self.dirpath.set(self.dirname)
    
    def downloadMp3(self):
        for mp3 in mp3Objects:
            mp3.download(dirpath)

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.exitButton = tk.Button(self, text="Exit", padx=30, command=root.destroy).grid(row=1, column=20, sticky='e', columnspan=5)
        self.downloadButton = tk.Button(self, text="Download", padx=10, command=self.downloadMp3).grid(row=1,column=0, sticky='w', columnspan=5)
        self.text = path.dirname(path.realpath(__file__))
        self.dirpath = tk.StringVar(root)
        self.dirpath.set(self.text)
        self.pathDir = tk.Entry(self, width=200, textvariable=self.dirpath)
        self.pathDir.grid(row=0,column=0,columnspan=24, sticky="w")
        for i in range(24):
            self.columnconfigure(i, weight=1)
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'
        self.dirButton = tk.Button(self, text="...", width=2, command=self.askDirectory).grid(row=0, column=24, sticky='e')

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1000x600+200+100')
    topWindow=TopWindow(root)
    topWindow.pack(side="top", fill="y", expand='no')
    middleWindow = MiddleWindow(root)
    middleWindow.pack(side="top", fill="both", expand='yes')
    bottomWindow = BottomWindow(root)
    bottomWindow.pack(side="top", fill="y", expand='no')
    root.mainloop()
