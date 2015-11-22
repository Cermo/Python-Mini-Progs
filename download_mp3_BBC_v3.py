import Tkinter as tk
import tkFileDialog
from os import path
import urllib2
import re
import threading
import shelve

class TopWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="New mp3 files")
        label.grid(row=0, column=0, sticky='w')

class MiddleWindow(tk.Frame):
    
    def onFrameConfigure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)
    
    def CreateEntry(self, bbcSite):
        for mp3 in range(len(bbcSite.getMp3Links())):
            self.buttons.append(tk.Label(self.frame, text=bbcSite.getMp3Links()[mp3]))
            self.checkbox = tk.Checkbutton(self.frame, variable=self.var).grid(row=mp3, column=1, sticky='e')
            self.buttons[mp3].grid(row=mp3, sticky='w')
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.scroll = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=tk.YES)
        self.frame.pack(side="left", fill="both", expand=tk.YES)
        self.frame.columnconfigure(0, weight=10)
        self.canvas_frame = self.canvas.create_window((0,0), window=self.frame, anchor="n")
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(self.canvas))
        self.canvas.bind('<Configure>', self.FrameWidth)
        self.buttons = []
        self.var = tk.IntVar()

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

bbcMainPage = "http://www.bbc.co.uk/learningenglish/english/features/6-minute-english"
searchedPattern = "/learningenglish/english/features/6-minute-english/ep-\d{6,8}"

bbcMainPageArch = "http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/"
searchedPatternArch = "/worldservice/learningenglish/general/sixminute/.{,50}.shtml"

class bbcSite(object):
    def __init__(self, url, searchPattern):
        self.url = url
        self.searchPattern = searchPattern
        self.subPageList = []
        self.linksTomp3 = []

    def createSubpageList(self):
        self.subPageList = re.findall(self.searchPattern, (urllib2.urlopen(self.url).read()))
    
    def extractMp3Link(self, link):
        self.linksTomp3 += re.findall(r'http.{,150}\.mp3', (urllib2.urlopen("http://www.bbc.co.uk"+link).read()))

    def extractMp3Links(self):
        threads = [threading.Thread(target=self.extractMp3Link, args=(link,)) for link in self.subPageList]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.linksTomp3 = list(set(self.linksTomp3))
    
    def getMp3Links(self):
        return self.linksTomp3

class Database(object):
    def __init__(self):
        self.db = shelve.open('bbc.db', 'c')
        self.db['db']
        
    def insert(self, bbcSite):
        for entry in bbcSite.getMp3Links():
            if entry not in self.db['db'][0]:
                self.db['db'][0].append(entry)
                self.db['db'][1].append('no')
    
    def printDB(self):
        print self.db['db']
        
if __name__ == '__main__':

    archMp3 = bbcSite(bbcMainPageArch, searchedPatternArch)
    #currentMp3 = bbcSite(bbcMainPage, searchedPattern)
    archMp3.createSubpageList()
    archMp3.extractMp3Links()
    
    root = tk.Tk()
    root.geometry('1000x600+200+100')
    topWindow=TopWindow(root)
    topWindow.pack(side="top", fill="y", expand='no')
    middleWindow = MiddleWindow(root)
    #middleWindow.CreateEntry(archMp3)
    db = Database()
    db.insert(archMp3)
    db.printDB()
    middleWindow.pack(side="top", fill="both", expand='yes')
    bottomWindow = BottomWindow(root)
    bottomWindow.pack(side="top", fill="y", expand='no')

    root.mainloop()
