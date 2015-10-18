import urllib2
import re
import os.path
from Tkinter import *
from sys import argv

bbcMainPage = "http://www.bbc.co.uk/learningenglish/english/features/6-minute-english"
searchedPattern = "/learningenglish/english/features/6-minute-english/ep-\d{6,8}"

bbcMainPageArch = "http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/"
searchedPatternArch = "/worldservice/learningenglish/general/sixminute/.{,50}.shtml"

class mp3file(object):
    row = 0
    def __init__(self, url):
        self.url = url
        self.name = url[url.rfind("/")+1:]
        self.label = Label(frame, text = self.name, background="#ffffff").grid(row=self.row, column = 0, sticky='w')
        self.checkbox = Checkbutton(frame).grid(row=self.row, column=1)
        self.__class__.row += 1
    
    

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
        
root = Tk()
root.geometry('800x600+200+200')
root.resizable(width='false', height='false')

canvas = Canvas(root, borderwidth=0, width=700, height=550)
frame = Frame(canvas, background="#ffffff")
scroll = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll.set)

scroll.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))


archMp3 = bbcSite(bbcMainPageArch, searchedPatternArch)
#currentMp3 = bbcSite(bbcMainPage, searchedPattern)
linksTomp3 = archMp3.createMp3Objects()
mp3Objects = []


for num in range(0,len(linksTomp3)):
    mp3Object = mp3file(linksTomp3[num])
    mp3Objects.append(mp3Object)

for mp3 in mp3Objects:
    print mp3.name

root.mainloop()
