from Tkinter import *
from os import path
import tkFileDialog

class mp3file(object):
    row = 0
    def __init__(self, url):
        self.url = url
        self.name = url
        self.label = Label(frame, text = self.name, background="#ffffff").grid(row=self.row, column = 0, sticky='w')
        self.checkbox = Checkbutton(frame).grid(row=self.row, column=1)
        self.__class__.row += 1

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))
    
def FrameWidth(event):
	canvas_width = event.width
	canvas.itemconfig(canvas_frame, width = canvas_width)

def askDirectory():
	dirname = tkFileDialog.askdirectory(**dir_opt)
	if dirname:
		var.set(dirname)


root = Tk()
root.geometry('650x600+200+100')

mainFrame = Frame(root,bd=5, background="#ffffff")
mainFrame.pack(side="top", fill="both", expand=YES)

canvas = Canvas(mainFrame,borderwidth=0, background="#ffffff")
frame = Frame(canvas, background="#ffffff")
scroll = Scrollbar(mainFrame, orient="vertical", command=canvas.yview) #
canvas.configure(yscrollcommand=scroll.set)

scroll.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=YES)
frame.pack(side="left", fill="both", expand=YES)
canvas_frame = canvas.create_window((0,0), window=frame, anchor="n")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
canvas.bind('<Configure>', FrameWidth)
frame.columnconfigure(0, weight=10)

frame2 = Frame(root, bd=5)
frame2.pack(side="bottom", fill="x", expand=NO, anchor="s")
exitButton = Button(frame2, text="Exit", padx=30, command=root.destroy).grid(row=1, column=20, sticky='e', columnspan=5)
downloadButton = Button(frame2, text="Download", padx=10).grid(row=1,column=0, sticky='w', columnspan=5)

for i in range(24):
	frame2.columnconfigure(i, weight=1)

text = path.dirname(path.realpath(__file__))
var = StringVar(root)
var.set(text)

pathDir = Entry(frame2, width=200, textvariable=var)
pathDir.grid(row=0,column=0,columnspan=24, sticky="w")

dir_opt = options = {}
options['initialdir'] = 'C:\\'
options['mustexist'] = False
options['parent'] = root
options['title'] = 'This is a title'
dirButton = Button(frame2, text="...", width=2, command=askDirectory).grid(row=0, column=24, sticky='e')

mp3Objects = []
for num in range(0,100):
    mp3Object = mp3file(num)
    mp3Objects.append(mp3Object)

root.mainloop()
