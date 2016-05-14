#!/usr/bin/python3

import os
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image, ImageFilter
import CryptoLibraries
import temp2
import numpy

class TkWindow(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.testOpen()

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

        # images
        buttonImageOriginal = tkinter.Button(frameTop, text=u"Get image", command=self.getFile)
        buttonImageOriginal.pack(side=tkinter.LEFT, anchor="nw")

        self.labelVariable = tkinter.StringVar()
        labelFileName = tkinter.Label(frameTop, textvariable=self.labelVariable, anchor="w", fg="black", bg="white")
        labelFileName.pack(side=tkinter.LEFT, anchor="nw")

        self.canvasOriginal = tkinter.Canvas(frameLeft,width=400, height=400,bd=0,bg="blue")
        self.canvasOriginal.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=tkinter.YES)

        self.canvasEncrypted = tkinter.Canvas(frameMiddle,width=400, height=400,bd=0,bg="blue")
        self.canvasEncrypted.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=tkinter.YES)

        # crypto
        buttonImageOriginal = tkinter.Button(frameTop, text=u"Use Crypto", command=self.useCrypto)
        buttonImageOriginal.pack(side=tkinter.LEFT, anchor="nw")

    def getFile(self):
        self.fileName = filedialog.askopenfilename(initialdir = "/home/paulina/obrazki",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.labelVariable.set(self.fileName)
        self.getImage()

    def getImage(self):
        self.imageOriginal = Image.open(self.fileName)
        (imageSizeWidth, imageSizeHeight) = self.imageOriginal.size
        print(imageSizeWidth, imageSizeHeight)

        newImageSizeHeight = 400
        n = imageSizeHeight/newImageSizeHeight
        print(n)
        newImageSizeWidth = int(imageSizeWidth/n)
        print(newImageSizeWidth, newImageSizeHeight)

        self.canvasOriginal.config(width=newImageSizeWidth,height=newImageSizeHeight)
        self.photo = self.imageOriginal.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        self.photo2 = ImageTk.PhotoImage(self.photo)
        self.canvasOriginal.create_image(int(newImageSizeWidth/2), int(newImageSizeHeight/2), image = self.photo2)

        self.photo.save("out.jpg", "JPEG", quality=80, optimize=True, progressive=True)


    def textLogsInsert(self,text):
        self.textLogs.configure(state="normal")
        self.textLogs.insert("end","%s\n"%text)
        print(text)
        self.textLogs.configure(state="disabled")
        self.textLogs.see("end")

    def useCrypto(self):
        #self.photo.save("out.ppm")
        imageRead = Image.open("out.ppm")
        key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

        temp2.encrypt_file("out.ppm", "out_encrypted.ppm", key)
        temp2.decrypt_file("out_encrypted.ppm", "out_decrypted.ppm", key)

        a = numpy.asarray(imageRead)
        print(a[0])

    def testOpen2(self):

        with open("out.jpg","rb") as fp:
            lines = []
            hexline = []
            str = b""
            header = b""
            body = b""
            k = 0
            print(type(fp))
            for line in fp:
                print("----------------------------------------------\n")
                print(line[0])

    def testOpen(self):

        with open("out.ppm","rb") as fp:
            lines = []
            hexline = []
            str = b""
            header = b""
            body = b""
            k = 0
            print(type(fp))
            for line in fp:
                #print("----------------------------------------------\n")
                hl = ':'.join(['%02x' % b for b in line])
                hexline.append(hl)
                lines.append(line)
                #print(hexline)
                if k < 3:
                    header = header + line
                else:
                    body = body + line
                k=k+1
            for k in range(0, 10):
                print("----------------------------------------------\n")
                print(hexline[k])
                print("----------------------------------------------\n")
                print(lines[k])
            print("***********")
            str = str + lines[1]
            str = str + lines[1]
            print(str)
            for line in str:
                print("#############")
                print(line)
            print("***********")
            print(header)

            key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

            bodyEnc = temp2.encrypt(body,key)

            fileEnc = header + bodyEnc
            with open("out0505.ppm", 'wb') as fo:
                fo.write(fileEnc)
            print(type(fo))

        self.removeFile("to_remove.txt")
        print("Done")

    def removeFile(self,fname):
        try:
            os.remove(fname)
        except Exception as message:
            self.textLogsInsert(message)
        else:
            self.textLogsInsert("File \"%s\" removed" % (fname))


if __name__ == '__main__':
    app = TkWindow(None)
    app.title('Crypto')
    app.minsize(800,600)
    app.mainloop()
