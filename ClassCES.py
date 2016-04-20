#!/usr/bin/python3

import os
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image

class TkWindow(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # main frames
        frameMain = tkinter.Frame(self,bg="#FFFFFF")
        frameMain.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)
        frameTop = tkinter.Frame(frameMain, relief=tkinter.GROOVE, borderwidth=2)
        frameTop.pack(side=tkinter.TOP, fill=tkinter.X, expand=tkinter.NO, anchor="nw")
        frameBottom = tkinter.Frame(frameMain, relief=tkinter.GROOVE, borderwidth=2)
        frameBottom.pack(side=tkinter.BOTTOM, fill=tkinter.X, expand=tkinter.NO, anchor="n")
        frameLeft = tkinter.Frame(frameMain,relief=tkinter.GROOVE, borderwidth=2)
        frameLeft.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, anchor="nw")
        frameMiddle = tkinter.Frame(frameMain,relief=tkinter.GROOVE, borderwidth=2)
        frameMiddle.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, anchor="nw")
        frameRight = tkinter.Frame(frameMain,relief=tkinter.GROOVE, borderwidth=2)
        frameRight.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, anchor="nw")

        # logs
        vscrollbarFrameBottom = tkinter.Scrollbar(frameBottom, orient=tkinter.VERTICAL)
        vscrollbarFrameBottom.pack(fill=tkinter.Y, side=tkinter.RIGHT, expand=tkinter.FALSE)

        self.textLogs = tkinter.Text(frameBottom, relief=tkinter.GROOVE, borderwidth=2,state="disabled", wrap=tkinter.WORD, height=10, yscrollcommand=vscrollbarFrameBottom.set)
        self.textLogs.pack(side=tkinter.TOP, padx=5, pady=5, expand=tkinter.YES, fill=tkinter.X)
        vscrollbarFrameBottom.config(command=self.textLogs.yview)

        #
        buttonImageOriginal = tkinter.Button(frameTop, text=u"Get image", command=self.getFile)
        buttonImageOriginal.pack(side=tkinter.LEFT, anchor="nw")

        self.labelVariable = tkinter.StringVar()
        labelFileName = tkinter.Label(frameTop, textvariable=self.labelVariable, anchor="w", fg="black", bg="white")
        labelFileName.pack(side=tkinter.LEFT, anchor="nw")

        self.canvas = tkinter.Canvas(frameLeft,width=400, height=400,bd=0,bg="blue")
        self.canvas.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=tkinter.YES)

    def getFile(self):
        self.fileName = filedialog.askopenfilename(initialdir = "/home/paulina/obrazki",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.labelVariable.set(self.fileName)

        self.photo = Image.open(self.fileName)
        (imageSizeWidth, imageSizeHeight) = self.photo.size
        print(imageSizeWidth, imageSizeHeight)

        newImageSizeHeight = 400
        n = imageSizeHeight/newImageSizeHeight
        print(n)
        newImageSizeWidth = int(imageSizeWidth/n)
        print(newImageSizeWidth, newImageSizeHeight)

        self.canvas.config(width=newImageSizeWidth,height=newImageSizeHeight)
        self.photo = self.photo.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.photo)
        self.canvas.create_image(int(newImageSizeWidth/2), int(newImageSizeHeight/2), image = self.photo)



    def textLogsInsert(self,text):
        self.textLogs.configure(state="normal")
        self.textLogs.insert("end","%s\n"%text)
        print(text)
        self.textLogs.configure(state="disabled")
        self.textLogs.see("end")


if __name__ == '__main__':
    app = TkWindow(None)
    app.title('Crypto')
    app.minsize(800,600)
    app.mainloop()
