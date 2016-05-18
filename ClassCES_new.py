#!/usr/bin/python3

import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageFilter
import CryptoLibraries
import time

class TkWindow(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.key = os.urandom(32)

        self.initializeVariables()
        self.initializeTkElements()

    def initializeVariables(self):
        self.directoryOriginal = "./original/"
        self.directoryEncrypted = "./encrypted/"
        self.directoryDecrypted = "./decrypted/"
        os.makedirs(self.directoryOriginal, exist_ok = True)
        os.makedirs(self.directoryEncrypted, exist_ok = True)
        os.makedirs(self.directoryDecrypted, exist_ok = True)
        self.imageTkResizedOriginal = None
        self.imageTkResizedEncrypted = None
        self.imageTkResizedDecrypted = None
        self.imageOriginal = None
        self.imageEncrypted = None
        self.imageDecrypted = None
        self.bodyOriginal = None
        self.bodyEncrypted = None
        self.bodyDecrypted = None
        self.tagCounter = 0
        self.tagStop = "1.0"
        self.tagColorWarning = "#FF0000"
        self.tagColorOk = "#00FF00"

        self.encryptionOptions = [
            ("Crypto_AES_CBC", "lib: Crypto, enc: AES, mode: CBC"),
            ("Another", "Another option")
            ]
        self.encryptionChosen = tk.StringVar()

    def initializeTkElements(self):
        # main frames
        frameMain = tk.Frame(self,bg="#FFFFFF")
        frameMain.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.YES)
        frameLogs = tk.Frame(frameMain, relief = tk.GROOVE, borderwidth = 2)
        frameLogs.pack(side = tk.BOTTOM, fill = tk.X, expand = tk.NO, anchor = "n")
        frameControls = tk.Frame(frameMain, relief = tk.GROOVE, borderwidth = 2)
        frameControls.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.NO, anchor = "nw")
        frameOriginal = tk.Frame(frameMain, relief = tk.GROOVE, borderwidth = 2)
        frameOriginal.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.YES, anchor = "nw")
        frameEncrypted = tk.Frame(frameMain, relief = tk.GROOVE, borderwidth = 2)
        frameEncrypted.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.YES, anchor = "nw")
        frameDecrypted = tk.Frame(frameMain, relief = tk.GROOVE, borderwidth = 2)
        frameDecrypted.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.YES, anchor = "nw")

        # logs
        vscrollbarFrameLogs = tk.Scrollbar(frameLogs, orient = tk.VERTICAL)
        vscrollbarFrameLogs.pack(fill = tk.Y, side = tk.RIGHT, expand = tk.FALSE)

        self.textLogs = tk.Text(frameLogs, relief = tk.GROOVE, borderwidth = 2, state = "disabled", wrap = tk.WORD, height = 10, yscrollcommand = vscrollbarFrameLogs.set)
        self.textLogs.pack(side = tk.TOP, padx = 5, pady = 5, expand = tk.YES, fill = tk.X)
        vscrollbarFrameLogs.config(command = self.textLogs.yview)

        # canvas
        labelOriginal = tk.Label(frameOriginal, text = "Original picture:")
        labelOriginal.pack(side = tk.TOP, fill = tk.X, expand = tk.NO)
        labelEncrypted = tk.Label(frameEncrypted, text = "Encrypted picture:")
        labelEncrypted.pack(side = tk.TOP, fill = tk.X, expand = tk.NO)
        labelDecrypted = tk.Label(frameDecrypted, text = "Decrypted picture:")
        labelDecrypted.pack(side = tk.TOP, fill = tk.X, expand = tk.NO)

        self.canvasOriginal = tk.Canvas(frameOriginal, bd = 0)
        self.canvasOriginal.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.YES)
        self.canvasEncrypted = tk.Canvas(frameEncrypted, bd = 0)
        self.canvasEncrypted.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.YES)
        self.canvasDecrypted = tk.Canvas(frameDecrypted, bd = 0)
        self.canvasDecrypted.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.YES)

        self.canvasOriginal.bind("<Configure>", self.imageResizeOriginal)
        self.canvasEncrypted.bind("<Configure>", self.imageResizeEncrypted)
        self.canvasDecrypted.bind("<Configure>", self.imageResizeDecrypted)

        # button - image
        buttonImageOriginal = tk.Button(frameControls, text = "Get image file", command = self.getFile)
        buttonImageOriginal.pack(side = tk.TOP, fill = tk.X, expand = tk.NO, anchor = "n")

        # crypto
        buttonEncrypt = tk.Button(frameControls, text = "Encrypt", command = self.encrypt)
        buttonEncrypt.pack(side = tk.TOP, fill = tk.X, expand = tk.NO, anchor = "n")

        buttonDecrypt = tk.Button(frameControls, text = "Decrypt", command = self.decrypt)
        buttonDecrypt.pack(side = tk.TOP, fill = tk.X, expand = tk.NO, anchor = "n")

        # radiobuttons - options
        radiobuttonDict = {}
        self.radiobuttonDictVal = {}
        for (key, value) in self.encryptionOptions:
            self.radiobuttonDictVal[key] = tk.StringVar()
            self.radiobuttonDictVal[key].set(value)
            radiobuttonDict[key] = tk.Radiobutton(frameControls, textvariable = self.radiobuttonDictVal[key], variable = self.encryptionChosen, value = key, command = self.radiobuttonChoose)
            radiobuttonDict[key].pack(side = tk.TOP, fill = tk.Y, expand = tk.NO, anchor = "nw")

    def radiobuttonChoose(self):
        self.textLogsInsert("Option chosen: %s" % self.radiobuttonDictVal[self.encryptionChosen.get()].get())

    def textLogsInsert(self, text, color = "#000000"):
        self.textLogs.configure(state = "normal")

        self.tagStart = self.tagStop
        self.textLogs.insert("end", "%s\n" % text)
        self.tagStop = self.textLogs.index("end-1c")

        self.textLogs.configure(state = "disabled")
        self.textLogs.see("end")

        self.textLogs.tag_add(str(self.tagCounter), self.tagStart, self.tagStop)
        self.textLogs.tag_config(str(self.tagCounter), foreground = color)
        self.tagCounter = self.tagCounter + 1

    def pathLeaf(self,path):
        leaves = path.strip("/").strip("\\").split("/")[-1].split("\\")[-1].split(".")
        return (leaves[0], leaves[-1])

    def getFile(self):
        self.fileNameOriginal = filedialog.askopenfilename(initialdir = "/home/paulina/obrazki",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if bool(self.fileNameOriginal):
            self.textLogsInsert("Opened: %s" % self.fileNameOriginal)
            self.displayImageOriginal()

    def displayImageOriginal(self):
        imageOriginal = Image.open(self.fileNameOriginal)
        (self.imageName, extension) = self.pathLeaf(self.fileNameOriginal)
        self.imageName = self.returnName(self.directoryOriginal, self.imageName)
        imageOriginal.save("%s%s.ppm" % (self.directoryOriginal, self.imageName))
        self.textLogsInsert("Converted and saved as: %s%s.ppm" % (self.directoryOriginal, self.imageName))
        self.imageOriginal = Image.open("%s%s.ppm" % (self.directoryOriginal, self.imageName))
        self.imageTkResizedOriginal = self.imageResize(self.imageOriginal, self.canvasOriginal)

        (self.header, self.bodyOriginal) = self.splitImageFile("%s%s.ppm" % (self.directoryOriginal, self.imageName))

        self.textLogsInsert("Image ready for encryption.", self.tagColorOk)

    def returnName(self, dir, nameRef):
        name = nameRef
        k = 0
        while(os.path.isfile("%s%s.ppm" % (dir, name))):
            name = "%s(%d)" % (nameRef , k)
            k = k + 1
        return name


    def imageResizeOriginal(self, event):
        if bool(self.imageOriginal):
            self.imageTkResizedOriginal = self.imageResize(self.imageOriginal, self.canvasOriginal)
    def imageResizeEncrypted(self, event):
        if bool(self.imageEncrypted):
            self.imageTkResizedEncrypted = self.imageResize(self.imageEncrypted, self.canvasEncrypted)
    def imageResizeDecrypted(self, event):
        if bool(self.imageDecrypted):
            self.imageTkResizedDecrypted = self.imageResize(self.imageDecrypted, self.canvasDecrypted)

    def imageResize(self, image, canvas):
        (imageSizeWidth, imageSizeHeight) = image.size
        canvasSizeWidth = canvas.winfo_width()
        canvasSizeHeight = canvas.winfo_height()

        newImageSizeHeight = canvasSizeHeight
        n = imageSizeHeight/newImageSizeHeight
        newImageSizeWidth = int(imageSizeWidth/n)

        if ((canvasSizeWidth - newImageSizeWidth) < 0):
            newImageSizeWidth = canvasSizeWidth
            n = imageSizeWidth/newImageSizeWidth
            newImageSizeHeight = int(imageSizeHeight/n)

        #self.canvasOriginal.config(width=newImageSizeWidth,height=newImageSizeHeight)
        imageResized = image.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        imageTkResized = ImageTk.PhotoImage(imageResized)
        canvas.create_image(int(canvasSizeWidth/2), int(canvasSizeHeight/2), image = imageTkResized)
        return imageTkResized

    def splitImageFile(self, image):
        with open(image,"rb") as fp:
            header = b""
            body = b""
            k = 0
            for line in fp:
                if k < 3:
                    header = header + line
                else:
                    body = body + line
                k=k+1
            return (header, body)


    def encrypt(self):
        if bool(self.bodyOriginal):
            if bool(self.encryptionChosen.get()):
                self.textLogsInsert("Starting encryption...")
                if self.encryptionChosen.get() == "Crypto_AES_CBC":
                    start = time.time()
                    self.bodyEncrypted = CryptoLibraries.crypto_AES_CBC_Encrypt(self.bodyOriginal, self.key)
                    stop = time.time()

                self.imageNameEncrypted = self.returnName(self.directoryEncrypted , "%s_enc_%s" % (self.imageName, self.encryptionChosen.get()))
                self.saveImage(self.bodyEncrypted, "%s%s.ppm" % (self.directoryEncrypted, self.imageNameEncrypted))

                self.imageEncrypted = Image.open("%s%s.ppm" % (self.directoryEncrypted, self.imageNameEncrypted))
                self.imageTkResizedEncrypted = self.imageResize(self.imageEncrypted, self.canvasEncrypted)

                self.textLogsInsert("Encryption finished :)", self.tagColorOk)
                self.textLogsInsert("Lasted %s sec" % (stop - start))
                self.textLogsInsert("Output saved as: %s%s.ppm" % (self.directoryEncrypted, self.imageNameEncrypted))
            else:
                self.textLogsInsert("Choose option", self.tagColorWarning)
        else:
            self.textLogsInsert("Got nothing to encrypt :(", self.tagColorWarning)

    def decrypt(self):
        if bool(self.bodyEncrypted):
            if bool(self.encryptionChosen.get()):
                self.textLogsInsert("Starting decryption...")
                if self.encryptionChosen.get() == "Crypto_AES_CBC":
                    start = time.time()
                    bodyDecrypted = CryptoLibraries.crypto_AES_CBC_Decrypt(self.bodyEncrypted, self.key)
                    stop = time.time()

                imageNameDecrypted = self.returnName(self.directoryDecrypted, "%s_dec_%s" % (self.imageNameEncrypted, self.encryptionChosen.get()))
                self.saveImage(bodyDecrypted, "%s%s.ppm" % (self.directoryDecrypted, imageNameDecrypted))

                self.imageDecrypted = Image.open("%s%s.ppm" % (self.directoryDecrypted, imageNameDecrypted))
                self.imageTkResizedDecrypted = self.imageResize(self.imageDecrypted, self.canvasDecrypted)

                self.textLogsInsert("Decryption finished :)", self.tagColorOk)
                self.textLogsInsert("Lasted %s sec" % (stop - start))
                self.textLogsInsert("Output saved as: %s%s.ppm" % (self.directoryDecrypted, imageNameDecrypted))
            else:
                self.textLogsInsert("Choose option", self.tagColorWarning)
        else:
            self.textLogsInsert("Got nothing to decrypt :(", self.tagColorWarning)

    def saveImage(self, body, name):
        with open(name, 'wb') as fo:
            fo.write(self.header + body)

if __name__ == '__main__':
    pass
