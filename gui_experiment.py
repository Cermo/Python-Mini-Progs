from Tkinter import *

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

root = Tk()
root.geometry('650x800+200+200')

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

frame2 = Frame(root, bd=5, background="#ffffff")
frame2.pack(side="bottom", fill="x")
exitButton = Button(frame2, text="Exit", width=10).grid(row=1, column=104)
downloadButton = Button(frame2, text="Download", width=10).grid(row=1,column=0)

pathDir = Entry(frame2, width=105)
pathDir.insert(0, "C:\BBC 6 Minute English")
pathDir.grid(columnspan=105, row=0, column=0)

mp3Objects = []
for num in range(0,100):
    mp3Object = mp3file(num)
    mp3Objects.append(mp3Object)

root.mainloop()
