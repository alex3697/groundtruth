#-------------------------------------------------------------------------------
# Name:        Object bounding box label tool
# Purpose:     Label object bboxes for ImageNet Detection data
# Author:      Qiushi
# Created:     06/06/2014

#
#-------------------------------------------------------------------------------
from __future__ import division
from tkinter import * 
# from tkinter import messagebox as tkMessageBox
from PIL import Image, ImageTk
import os
import glob
import random


# colors for the bboxes
COLORS = ['red', 'blue', 'yellow', 'pink', 'cyan', 'green', 'black']
# image sizes for the examples
SIZE = 256, 256

class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("Autocatalogador :D")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width = FALSE, height = FALSE)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.hl = None
        self.vl = None

        # ----------------- GUI stuff ---------------------
        # dir entry & load
        self.label = Label(self.frame, text = "Image Dir:")
        self.label.grid(row = 0, column = 0, sticky = E)      #aqui antes E
        self.entry = Entry(self.frame)
        self.entry.grid(row = 0, column = 1, sticky = W+E)
        self.entry.insert(0,'Data')
        self.ldBtn = Button(self.frame, text = "Load", width = 10, command = self.loadDir)
        self.ldBtn.grid(row = 0, column = 2, sticky = W)

        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.mainPanel.grid(row = 1, column = 1, rowspan = 6, sticky = W+N) #aqui W+N
        self.parent.bind("<Escape>", self.cancelBBox)
        self.parent.bind("<Control-d>", self.nextImage)
        self.parent.bind("<Control-a>", self.prevImage)
        self.parent.bind("<Control-s>", self.saveImage)


        # showing bbox info & delete bbox
        self.lb1 = Label(self.frame, text = 'Bounding boxes')
        self.lb1.grid(row = 1, column = 2)
        self.listbox = Listbox(self.frame, width = 40, height = 12)
        self.listbox.grid(row = 2, column = 2, sticky = N)
        self.btnDel = Button(self.frame, text = 'Delete', width = 10, command = self.delBBox)
        self.btnDel.grid(row = 3, column = 2, padx = 45, pady = 3, sticky = W)
        self.btnClear = Button(self.frame, text = 'Clear All', width = 10, command = self.clearBBox)
        self.btnClear.grid(row = 3, column = 2, padx = 45, pady = 3, sticky = E)
        self.itemLabel = Label(self.frame, text = "Item")
        self.itemLabel.grid(row = 4, column = 2, sticky = N)
        self.itembox = Listbox(self.frame, width = 40, height = 12)
        self.itembox.grid(row = 4, column = 2, padx = 10, sticky = N+S)
        self.itembox.bind('<<ListboxSelect>>', self.itemselected)
        self.itemEntry = Entry(self.frame)
        self.itemEntry.grid(row = 5, column = 2, padx = 10, sticky = W+E+N)   #aqui label de introducir 
        self.itemEntry.insert(0,'movistar')

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 7, column = 1, columnspan = 2, sticky = W+E)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev (Control - A)', width = 15, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next (Coontrol - D) >>', width = 15, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel)
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)
        self.addcptBtn = Button(self.ctrPanel,text = 'Add Caption', command = self.addCaption)
        self.addcptBtn.pack(side = RIGHT)
        self.addFaceBtn = Button(self.ctrPanel,text = 'Add Face', command = self.addFace)
        self.addFaceBtn.pack(side = RIGHT)

        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side = RIGHT)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

    def loadDir(self, dbg = False):
        if not dbg:
            s = self.entry.get()
            self.parent.focus()
            self.category = str(s)
        else:
            s = r'D:\workspace\python\labelGUI'

        # get image list
        imageDir = os.path.abspath(__file__)
        imageDir.split('interfaz.py')
        self.imageDir = os.path.join(imageDir[0], self.category)
        self.imageDir = 'c:\\Users\\Alex\\Desktop\\Ugiat\\groundtruth\\groundtruth\\autocatalogador\\Data'
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpg'))
        if len(self.imageList) == 0:
            print('No .jpg images found in the specified dir!')
            return

        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

        # set up output dir
        self.outDir = os.path.join('Output') 
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)


        self.loadImage()
        print('%d images loaded from %s' %(self.total, s))


    def loadImage(self):
        # load image
        imagepath = self.imageList[self.cur - 1]
        self.tmpLabel.config(text=imagepath)
        self.img = Image.open(imagepath)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = max(self.tkimg.width(), 400), height = max(self.tkimg.height(), 400))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW) #aqui habia NW 0,0
        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

        # load labels

        self.clearBBox()
        self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.imageDir, labelname)
        bbox_cnt = 0
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                print('Labels from: ' + labelname)
                for (i, line) in enumerate(f):
                    if i == 0:
                    #    bbox_cnt = int(line.strip())
                        continue
                    tmp = [t.strip() for t in line.split()]
                    print(tmp)
                    tmp[0] = float(tmp[0]) * self.img.width
                    tmp[1] = float(tmp[1]) * self.img.height
                    tmp[2] = float(tmp[2]) * self.img.width
                    tmp[3] = float(tmp[3]) * self.img.height
                    print(self.img.size)
                    print(self.img.height)
                    print(self.img.width)
                    print(tmp)
                    self.bboxList.append(tuple(tmp))
                    tmpId = self.mainPanel.create_rectangle(tmp[0], tmp[1], \
                                                            tmp[2], tmp[3], \
                                                            width = 2, \
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    self.bboxIdList.append(tmpId)
                    self.listbox.insert(END, '(%d, %d) -> (%d, %d) : %s' %(float(tmp[0]), float(tmp[1]), float(tmp[2]), float(tmp[3]), tmp[4]))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
                    # Add item to history log
                    
                    if tmp[4] not in self.itembox.get(0, END):
                        print(tmp[4])
                        self.itembox.insert(END, tmp[4])

    def saveImage(self):
        file = os.path.splitext(self.labelfilename)[0]
        im = Image.open(file + '.jpg')
        width, height = im.size

        # Save XML
        # with open(file + '.xml', 'a') as exported:
        #     exported.truncate(0)
        #     exported.write('<?xml version="1.0" encoding="utf-8"?>\n')
        #     exported.write('<KeyFrame>\n')
        #     captions = 0
        #     faces = 0
        #     captionList = []
        #     faceList = []
        #     for bbox in self.bboxList:
        #         if bbox[5] == '0':
        #             captions += 1
        #             captionList.append(bbox)
        #         if bbox[5] == '1':
        #             faces += 1
        #             faceList.append(bbox)
        #     if captions != 0:
        #         exported.write('\t<CaptionsInformation>')
        #         exported.write('\t\t<name>' + 'Number of Captions' + '</name>')
        #         exported.write('\t\t<value>' + str(captions) + '</value>')
        #         exported.write('\t</CaptionsInformation>')
        #         exported.write('\t<Captions>\n')
        #         for capt in captionList:
        #             exported.write('\t\t<caption>\n')
        #             exported.write('\t\t\t<y2>' + str(float(capt[0])/self.img.width) + '</y2>')
        #             exported.write('\t<y1>' + str(float(capt[1])/self.img.height) + '</y1>')
        #             exported.write('\t<x2>' + str(float(capt[2])/self.img.width) + '</x2>')
        #             exported.write('\t<x1>' + str(float(capt[3])/self.img.height) + '</x1>')
        #             exported.write('\t<string>' + capt[4] + '</string>\n')
        #             exported.write('\t\t</caption>\n')
        #         exported.write('\t</Captions>\n')
        #     if faces != 0: 
        #         exported.write('\t<FacesInformation>\n')
        #         exported.write('\t\t<name>' + 'Number of Faces' + '</name>')
        #         exported.write('\t\t<value>' + str(faces) + '</value>\n')
        #         exported.write('\t</FacesInformation>\n')
        #         exported.write('\t<Faces>\n')
        #         for fac in faceList:
        #             exported.write('\t\t<Face>\n')
        #             exported.write('\t\t\t<y2>' + str(float(fac[0])/self.img.width) + '</y2>')
        #             exported.write('\t<y1>' + str(float(fac[1])/self.img.height) + '</y1>')
        #             exported.write('\t<x2>' + str(float(fac[2])/self.img.width) + '</x2>')
        #             exported.write('\t<x1>' + str(float(fac[3])/self.img.height) + '</x1>')
        #             exported.write('\t<person_id>' + fac[4] + '</person_id>\n')
        #             exported.write('\t\t</Face>\n')
        #         exported.write('\t</Faces>\n')
                
        #     exported.write('\t<folder>Annotations</folder>\n')
        #     exported.write('\t<filename>' + str(os.path.basename(file)) + '.jpg' + '</filename>\n')
        #     exported.write('\t<size>\n')
        #     exported.write('\t\t<width>' + str(width) + '</width>\n')
        #     exported.write('\t\t<height>' + str(height) + '</height>\n')
        #     exported.write('\t</size>\n')
        #     exported.write('</KeyFrame>\n')

        # Save TXT
        with open(self.labelfilename, 'w') as f:
            #f.write('%d\n' %len(self.bboxList))
            for bbox in self.bboxList:
                f.write(str(bbox[4]) + ' ')
            f.write('\n')
            for bbox in self.bboxList:
                f.write(str(float(bbox[0])/self.img.width))
                f.write(' ')
                f.write(str(float(bbox[1])/self.img.height))
                f.write(' ')
                f.write(str(float(bbox[2])/self.img.width))
                f.write(' ')
                f.write(str(float(bbox[3])/self.img.height))
                f.write(' ')
                f.write(str(bbox[4]))
                f.write(' ')
                f.write(str(bbox[5]))
                f.write('\n')
        f.close()
                



    def mouseClick(self, event):
        if self.STATE['click'] == 0:
            self.STATE['x'], self.STATE['y'] = event.x, event.y
        else:
            x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
            y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
            actual_item = self.itemEntry.get()
            self.bboxList.append((x1, y1, x2, y2, actual_item.split()[0],actual_item.split()[1]))
            self.bboxIdList.append(self.bboxId)
            self.bboxId = None
            self.listbox.insert(END, '(%d, %d) -> (%d, %d) : %s' %(x1, y1, x2, y2, self.itemEntry.get()))
            print('ACTUAL ITEM HIST LIST: ' + str(self.itembox.get(0, END)))
            if actual_item not in self.itembox.get(0, END):
                self.itembox.insert(END, actual_item)
            self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
        self.STATE['click'] = 1 - self.STATE['click']

    def mouseMove(self, event):
        self.disp.config(text = 'x: %d, y: %d' %(event.x, event.y))
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
            self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], \
                                                            event.x, event.y, \
                                                            width = 2, \
                                                            outline = COLORS[len(self.bboxList) % len(COLORS)])

    def itemselected(self, event):
        index = int(self.itembox.curselection()[0])
        value = self.itembox.get(index)
        self.itemEntry.delete(0, "end")
        self.itemEntry.insert(0,value)
        print('You selected item %d: "%s"' % (index, value))

    def cancelBBox(self, event):
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
                self.bboxId = None
                self.STATE['click'] = 0

    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)

    def clearBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []

    def prevImage(self, event = None):

        self.saveImage()
        self.itembox.delete(0,END) #esto lo he añadido nuevo
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    def nextImage(self, event = None):
        self.saveImage()
        self.itembox.delete(0,END) #esto lo he añadido nuevo
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        self.itembox.delete(0,END) #esto lo he añadido nuevo
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

    def addCaption(self, event = None):
        entrada = []
        entrada.append(self.itemEntry.get())
        entrada.append(int(0))
        self.itembox.insert(END, entrada)

    def addFace(self, event = None):
        entrada = []
        entrada.append(self.itemEntry.get())
        entrada.append(int(1))
        self.itembox.insert(END, entrada)

if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
    root.resizable(width = True, height = True)
    root.mainloop()