import Tkinter as tk
import ttk as ttk
import tkFileDialog
from os import path
import urllib2
import re
import threading
import shelve

#from  swampy import Lumpy
#lumpy = Lumpy.Lumpy()
#lumpy.make_reference()

class NotificationWindow(tk.Frame):
    def __init__(self, parent):
        pass
        
class TopWindow(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=10)


class MiddleWindow(ttk.Frame):
    
    def onFrameConfigure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

    def CreateEntry(self, db):
        separatorDrawed = None
        self.label = ttk.Label(self.frame, text="New mp3 files")
        self.label.grid(row=0, column=0, columnspan=2, sticky='we')
        for mp3 in range(len(db.readDB()[0])):
            self.variables.append(tk.IntVar())
            self.buttons.append(ttk.Label(self.frame, text=db.readDB()[2][mp3]))
            self.checkboxes.append(ttk.Checkbutton(self.frame, variable=self.variables[mp3]))

            if db.readDB()[1][mp3] == 'no':
                self.buttons[mp3].grid(row=mp3+1, column=0, sticky='w')
                self.checkboxes[mp3].grid(row=mp3+1, column=1, sticky='e')
            if db.readDB()[1][mp3] == 'yes':
                if separatorDrawed == None:
                    self.label = ttk.Label(self.frame, text="Mp3 downloaded before")
                    self.label.grid(row=mp3+1, column=0, columnspan=2, sticky='we')
                    separatorDrawed = 'yes'
                self.buttons[mp3].grid(row=mp3+2, column=0, sticky='w')
                self.checkboxes[mp3].grid(row=mp3+2, column=1, sticky='e')

    def DestroyEntries(self):
        for entry in range(len(self.buttons)):
            self.buttons[entry].grid_forget()
            self.checkboxes[entry].grid_forget()
        self.buttons = []
        self.checkboxes = []
        self.variables = []
        try: 
            self.label.grid_forget()
        except:
            pass

    def getMp3toDownload(self):
        mp3toDownload = []
        for mp3 in range(len(self.variables)):
            if self.variables[mp3].get() == 1:
                mp3toDownload.append(mp3)
        return mp3toDownload
    
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.frame = ttk.Frame(self.canvas)
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=tk.YES)
        self.frame.pack(side="left", fill="both", expand=tk.YES)
        self.frame.columnconfigure(0, weight=10)
        self.canvas_frame = self.canvas.create_window((0,0), window=self.frame, anchor="n")
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(self.canvas))
        self.canvas.bind('<Configure>', self.FrameWidth)
        self.buttons = []
        self.checkboxes = []
        self.variables = []
        

class BottomWindow(tk.Frame):
    
    def askDirectory(self):
        self.dirname = tkFileDialog.askdirectory(**self.dir_opt)
        if self.dirname:
            self.dirpath.set(self.dirname)
    
    def Download(self):
        mp3toDownload = middleWindow.getMp3toDownload()
        for mp3 in mp3toDownload:
            mp3file = urllib2.urlopen(db.readDB()[0][mp3])
            total_size = mp3file.info().getheader('Content-Length').strip()
            total_size = int(total_size)
            bytes_so_far = 0
            output = open(self.dirpath.get()+ "\\" + db.readDB()[2][mp3] + ".mp3",'wb')
            self.progress["value"] = 0
            self.progress["maximum"] = total_size
            while True:
                dfile = mp3file.read(self.chunk_size)
                bytes_so_far += len(dfile)
                output.write(dfile)
                self.progress["value"] = bytes_so_far
                root.update_idletasks()
                if not dfile:
                    break
            output.close()
            db.markAsDownloaded(mp3)
        db.sort()
        middleWindow.DestroyEntries()
        middleWindow.CreateEntry(db)
            
    def closeApp(self):
        db.closeDB()
        root.destroy()

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.exitButton = ttk.Button(self, text="Exit", command=self.closeApp).grid(row=2, column=20, sticky='e', columnspan=5)
        self.downloadButton = ttk.Button(self, text="Download", command=self.Download).grid(row=2,column=0, sticky='w', columnspan=5)
        self.dirpath = tk.StringVar(root)
        self.dirpath.set(path.dirname(path.realpath(__file__)))
        self.pathEntry = ttk.Entry(self, width=200, textvariable=self.dirpath)
        self.pathEntry.grid(row=1,column=0,columnspan=24, sticky="w")
        for i in range(24):
            self.columnconfigure(i, weight=1)
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'
        self.var = tk.IntVar(self)
        self.dirButton = ttk.Button(self, text="...", width=2, command=self.askDirectory).grid(row=1, column=24, sticky='e')
        self.progress = ttk.Progressbar(self, orient="horizontal", 
                                        length=200, mode="determinate")
        self.progress.grid(row=0,column=0,columnspan=25, sticky="we")
        self.chunk_size=512

class bbcArchSite(object):
    def __init__(self):
        self.url = "http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/"
        self.searchPattern  = "/worldservice/learningenglish/general/sixminute/.{,50}.shtml"

class bbcSite(object):
    def __init__(self):
        self.url = "http://www.bbc.co.uk/learningenglish/english/features/6-minute-english"
        self.searchPattern  = "/learningenglish/english/features/6-minute-english/ep-\d{6,8}"
        self.subpageData = []
        self.linksTomp3 = []
        self.mp3names = []
        self.subPageList = list(set(re.findall(self.searchPattern, (urllib2.urlopen(self.url).read()))))
        for i in range(len(self.subPageList)):
            self.linksTomp3.append(None)
            self.mp3names.append(None)
    
    def extractMp3Link(self, link, index):
        self.linksTomp3[index] = str(re.findall(r'http.{,150}\.mp3', (urllib2.urlopen("http://www.bbc.co.uk"+link).read()))[0])
        self.mp3names[index] = str(re.findall(r'title.{0,250}title', (urllib2.urlopen("http://www.bbc.co.uk"+link).read()))[0][6:-7]).replace("/","-")
        
    def prepareMp3Links(self):
        threads = [threading.Thread(target=self.extractMp3Link, args=(link, self.subPageList.index(link))) for link in self.subPageList]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    
    def getMp3Links(self):
        return self.linksTomp3, self.mp3names

class Database(object):
    def __init__(self):
        newdb = 0
        if not path.isfile('bbc.db'):
            newdb = 1
        self.db = shelve.open('bbc.db', 'c')
        if newdb == 1:
            self.db['db'] = [[],[],[]]
        
    def insert(self, bbcSite):
        entries, names = bbcSite.getMp3Links()
        db = self.db['db']
        for entry, name in zip(entries, names):
            if entry not in db[0]:
                db[0].append(entry) #URL
                db[1].append('no')  #Downloaded ?
                db[2].append(name)
        self.db['db'] = db
    
    def markAsDownloaded(self, entry):
        db = self.db['db']
        db[1][entry] = 'yes'
        self.db['db'] = db
    
    def sort(self):
        db = self.db['db']
        again = 1
        while again == 1:
            again = 0
            for entry in range(len(db[0])-1):
                if db[1][entry] == 'yes' and db[1][entry+1] == 'no':
                    db[0][entry], db[0][entry+1] = db[0][entry+1], db[0][entry]
                    db[1][entry], db[1][entry+1] = db[1][entry+1], db[1][entry]
                    db[2][entry], db[2][entry+1] = db[2][entry+1], db[2][entry]
                    again = 1
        self.db['db'] = db
        
    def readDB(self):
        return self.db['db']
    
    def closeDB(self):
        self.db.close()
    
if __name__ == '__main__':

    #archMp3 = bbcSite()
    currentMp3 = bbcSite()
    #archMp3.prepareMp3Links()
    currentMp3.prepareMp3Links()
    db = Database()
    #db.insert(archMp3)
    db.insert(currentMp3)
    
    root = tk.Tk()
    root.geometry('500x600+200+100')
    topWindow = TopWindow(root)
    topWindow.pack(side="top", fill="both", expand='no')
    middleWindow = MiddleWindow(root)
    middleWindow.CreateEntry(db)
    middleWindow.pack(side="top", fill="both", expand='yes')
    bottomWindow = BottomWindow(root)
    bottomWindow.pack(side="top", fill="both", expand='no')
    root.protocol('WM_DELETE_WINDOW', bottomWindow.closeApp)
    #lumpy.object_diagram()
    root.mainloop()
