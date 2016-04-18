#!/usr/bin/python3

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
        # main frames
        frameMain = tkinter.Frame(self,bg="#FFFFFF")
        frameMain.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=tkinter.YES)
        frameTop = tkinter.Frame(frameMain,relief=tkinter.GROOVE, borderwidth=2)
        frameTop.pack(side=tkinter.TOP,fill=tkinter.X,expand=tkinter.NO,anchor="nw")
        frameLeft = tkinter.Frame(frameMain,relief=tkinter.GROOVE, borderwidth=2)
        frameLeft.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=tkinter.YES,anchor="nw")
        frameMiddle = tkinter.Frame(frameMain,relief=tkinter.GROOVE, borderwidth=2)
        frameMiddle.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=tkinter.YES,anchor="nw")
        frameRight = tkinter.Frame(frameMain,relief=tkinter.GROOVE, borderwidth=2)
        frameRight.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=tkinter.YES,anchor="nw")

        labelTest= tkinter.Label(frameTop,text="TEST LABEL",anchor="nw")
        labelTest.grid(column=0,row=0,padx=10,pady=10,sticky="EW")


if __name__ == '__main__':
    app = TkWindow(None)
    app.title('Crypto')
    app.minsize(800,600)
    app.mainloop()
