import urllib2
import re
from Tkinter import *
from os import path
import tkFileDialog
from sys import argv
import shelve

bbcMainPage = "http://www.bbc.co.uk/learningenglish/english/features/6-minute-english"
searchedPattern = "/learningenglish/english/features/6-minute-english/ep-\d{6,8}"

bbcMainPageArch = "http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/"
searchedPatternArch = "/worldservice/learningenglish/general/sixminute/.{,50}.shtml"

db = shelve.open('bbc.db','c')

class mp3file(object):
	row = 1
	mp3id = 0
	def __init__(self, url):
		self.var = IntVar()
		self.url = url
		self.name = url[url.rfind("/")+1:]
		#self.idlabel = Label(frame, text = self.mp3id, background="#ffffff", relief=RAISED).grid(row=self.row, column = 0, sticky='w')
		self.label = Label(frame, text = self.url, background="#ffffff")
		self.label.grid(row=self.row, column = 0, sticky='w')
		self.checkbox = Checkbutton(frame, variable=self.var).grid(row=self.row, column=1)
		self.__class__.row += 1
		self.__class__.mp3id += 1
	
	def download(self,dirpath):
		if self.var.get() == 1:
			filename = dirpath.get()+ "\\" + self.name
			mp3file = urllib2.urlopen(self.url)
			output = open(filename,'wb')
			output.write(mp3file.read())
			output.close()
		return 0	
	def loadInfoFromDB(self):
		pass
	def saveInfoToDB(self):
		pass

	
	
class bbcSite(object):
    def __init__(self, url, searchPattern):
        self.url = url
        self.searchPattern = searchPattern
    
    def createMp3Objects(self):
        linksTomp3 = []
        links = re.findall(self.searchPattern, (urllib2.urlopen(self.url).read()))
	
        for i in links:
            linksTomp3 += re.findall(r'http.{,150}\.mp3', (urllib2.urlopen("http://www.bbc.co.uk"+i).read()))

        return list(set(linksTomp3))

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))
    
def FrameWidth(event):
	canvas_width = event.width
	canvas.itemconfig(canvas_frame, width = canvas_width)

def askDirectory():
	dirname = tkFileDialog.askdirectory(**dir_opt)
	if dirname:
		dirpath.set(dirname)
def downloadMp3():
	for mp3 in mp3Objects:
		mp3.download(dirpath)

# ----------------------------------------------------------------------
# GUI Interface
#-----------------------------------------------------------------------
root = Tk()
root.geometry('1000x600+200+100')

mainFrame = Frame(root,bd=5, background="#ffffff")
mainFrame.pack(side="top", fill="both", expand=YES)

canvas = Canvas(mainFrame,borderwidth=0, background="#ffffff")
frame = Frame(canvas, background="#ffffff")
scroll = Scrollbar(mainFrame, orient="vertical", command=canvas.yview) #
canvas.configure(yscrollcommand=scroll.set)

LinkLabel = Label(frame, text = "Link location", relief=RAISED).grid(columnspan=2, row=0, column = 0, sticky='w')

scroll.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=YES)
frame.pack(side="left", fill="both", expand=YES)
canvas_frame = canvas.create_window((0,0), window=frame, anchor="n")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
canvas.bind('<Configure>', FrameWidth)
frame.columnconfigure(1, weight=10)

frame2 = Frame(root, bd=5)
frame2.pack(side="bottom", fill="x", expand=NO, anchor="s")
exitButton = Button(frame2, text="Exit", padx=30, command=root.destroy).grid(row=1, column=20, sticky='e', columnspan=5)
downloadButton = Button(frame2, text="Download", padx=10, command=downloadMp3).grid(row=1,column=0, sticky='w', columnspan=5)

for i in range(24):
	frame2.columnconfigure(i, weight=1)

text = path.dirname(path.realpath(__file__))
dirpath = StringVar(root)
dirpath.set(text)

pathDir = Entry(frame2, width=200, textvariable=dirpath)
pathDir.grid(row=0,column=0,columnspan=24, sticky="w")

dir_opt = options = {}
options['initialdir'] = 'C:\\'
options['mustexist'] = False
options['parent'] = root
options['title'] = 'This is a title'
dirButton = Button(frame2, text="...", width=2, command=askDirectory).grid(row=0, column=24, sticky='e')
#-----------------------------------------------------------------------
# Main app
#-----------------------------------------------------------------------
archMp3 = bbcSite(bbcMainPageArch, searchedPatternArch)
#currentMp3 = bbcSite(bbcMainPage, searchedPattern)
linksTomp3 = archMp3.createMp3Objects()
mp3Objects = []

for num in range(0,len(linksTomp3)):
    mp3Object = mp3file(linksTomp3[num])
    mp3Objects.append(mp3Object)

root.mainloop()
