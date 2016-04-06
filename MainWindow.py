#!/usr/bin/python

import os
import tkinter
from tkinter import filedialog, Canvas
from PIL import ImageTk, Image


class TkWindow(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        #self.filename = filedialog.askopenfilename(initialdir = "/home/paulina",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.grid()

        buttonFile = tkinter.Button(self,text=u"Get file",command=self.getFile)
        buttonFile.grid(column=0,row=1,padx=10,pady=10)

        #labelHeader = Tkinter.Label(self,text=u"Database file:",anchor="w")
        #labelHeader.grid(column=0,row=0,columnspan=3,padx=10,pady=10,sticky='EW')
        self.labelVariable = tkinter.StringVar()
        labelFileName = tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="black",bg="white")
        labelFileName.grid(column=1,row=1,columnspan=2,sticky='EW',padx=10,pady=10)

        self.canvas = Canvas(self)
        self.canvas.grid(row = 2,column = 0,columnspan=3,sticky='EW',padx=10,pady=10)
        #self.photo = ImageTk.PhotoImage(file = "/home/paulina/obrazki/obrazek.jpg")
        #self.canvas.create_image(0,0, image = self.photo)

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
        #if same:
        #    newImageSizeHeight = int(imageSizeHeight*n)
        #else:
        #    newImageSizeHeight = int(imageSizeHeight/n)


        self.photo = self.photo.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.photo)
        self.canvas.create_image(0,0, image = self.photo)



if __name__ == '__main__':
    print("WERDTGFYHJ")
    app = TkWindow(None)
    app.title('Altium Database Adder')
    app.minsize(600,400)
    app.mainloop()
