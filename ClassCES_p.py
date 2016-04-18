#!/usr/bin/python3

import os
import tkinter
from tkinter import filedialog, Canvas
from PIL import ImageTk, Image
import keyczar
from Crypto.Cipher import AES

class TkWindow(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        buttonFile = tkinter.Button(self,text=u"Get file",command=self.getFile)
        buttonFile.grid(column=0,row=1,sticky='EW',padx=10,pady=10)

        buttonCrypto = tkinter.Button(self,text=u"Crypto",command=self.crypto)
        buttonCrypto.grid(column=0,row=3,sticky='EW',padx=10,pady=10)

        #labelHeader = Tkinter.Label(self,text=u"Database file:",anchor="w")
        #labelHeader.grid(column=0,row=0,columnspan=3,padx=10,pady=10,sticky='EW')
        self.labelVariable = tkinter.StringVar()
        labelFileName = tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="black",bg="white")
        labelFileName.grid(column=1,row=1,columnspan=2,sticky='EW',padx=10,pady=10)

        self.canvas = Canvas(self,width=400, height=400,bd=0,bg="blue")
        self.canvas.grid(row = 2,column = 0,columnspan=2,sticky='EW',padx=10,pady=10)
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

        self.canvas.config(width=newImageSizeWidth,height=newImageSizeHeight)
        self.photo = self.photo.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.photo)
        self.canvas.create_image(int(newImageSizeWidth/2), int(newImageSizeHeight/2), image = self.photo)

    def crypto(self):
        obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
        message = "The answer is no"
        ciphertext = obj.encrypt(message)
        print(ciphertext)
        obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
        messagedec = obj2.decrypt(ciphertext)
        print(messagedec)


if __name__ == '__main__':
    app = TkWindow(None)
    app.title('Crypto')
    app.minsize(800,600)
    app.mainloop()
