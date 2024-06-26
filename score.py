#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import os
import os.path
import random
import codecs
import time
import argparse
#import keyboard

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *

from PIL import Image, ImageTk
from scoredata import ScoreData
from dataclasses import dataclass

@dataclass
class ButtonData:
    text: str
    value: str
    keybinding: str

class Fullscreen_Window:
    def __init__(self):
        self.state = False
        self.ended = False
        self.firstImage = True
        self.tk = Tk()

        parser = argparse.ArgumentParser()
        parser.add_argument('--log', dest='log', type=str, help='Add log')
        args = parser.parse_args() 
        logpath = args.log
        print(logpath)

        if os.name == 'nt':
            w, h = self.tk.winfo_screenwidth(), self.tk.winfo_screenheight()
            self.tk.geometry("%dx%d+0+0" % (w, h))
        else:
            self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.

        self.frame = Frame(self.tk)

        #label0 = Message(self.frame, width=800, text=config['message'], justify=CENTER, font=(None, 18))
        #label0.grid(row=1,column=1)

        label1 = Message(self.frame, width=800, pady=25, text=config['q'][0], justify=CENTER, font=(None, 18))
        label1.grid(row=2,columnspan=5)
        self.button_score1 = Button(self.frame, text =buttons[0].text, command = self.onscore(buttons[0].value), font=(None, 18))
        self.button_score1.grid(row=3, column=0)
        self.button_score2 = Button(self.frame, text =buttons[1].text, command = self.onscore(buttons[1].value), font=(None, 18))
        self.button_score2.grid(row=3, column=1)
        self.button_score3 = Button(self.frame, text =buttons[2].text, command = self.onscore(buttons[2].value), font=(None, 18))
        self.button_score3.grid(row=3, column=2)
        self.button_score4 = Button(self.frame, text =buttons[3].text, command = self.onscore(buttons[3].value), font=(None, 18))
        self.button_score4.grid(row=3, column=3)
        self.button_score5 = Button(self.frame, text =buttons[4].text, command = self.onscore(buttons[4].value), font=(None, 18))
        self.button_score5.grid(row=3, column=4)

        #self.button_yes1 = Button(self.frame, text =u"<- Да", command = self.onyes1, font=(None, 18))
        #self.button_yes1.grid(row=3, column=0)
        #self.button_no1  = Button(self.frame, text =u"Нет ->", command = self.onno1, font=(None, 18))
        #self.button_no1.grid(row=3, column=1)
        #label2 = Label(self.frame, text=config['q'][1], font=(None, 18))
        #label2.grid(row=3,columnspan=2)
        #self.button_yes2 = Button(self.frame, text ="Да", command = self.onyes2, font=(None, 18))
        #self.button_yes2.grid(row=4, column=0)
        #self.button_no2  = Button(self.frame, text ="Нет", command = self.onno2, font=(None, 18))
        #self.button_no2.grid(row=4, column=1)

        self.imcounter = Label(self.frame, text='AA', justify=CENTER, font=(None, 18))
        self.imcounter.grid(row=6, columnspan=5)

        self.nextImage()
        #button_yes1.pack()
        #button_yes2.pack()
        #button_no1.pack()
        #button_no2.pack()
        self.frame.pack()

        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        for i in range(len(buttons)):
            self.tk.bind(buttons[i].keybinding, self.onscore(buttons[i].value))   
        #self.tk.bind("1", self.onscore(1))
        #self.tk.bind("2", self.onscore(2))
        #self.tk.bind("3", self.onscore(3))
        #self.tk.bind("4", self.onscore(4))
        #self.tk.bind("5", self.onscore(5))
        self.tk.focus_set()
        #while True:
        #    try:
        #        if keyboard.is_pressed('z'):
        #            self.prevImage
        #    except:
        #        break

    def nextImage(self):
        if(self.ended):
            return
        if(hasattr(self,'currentState')):
            data.setScore(self.currentState['path'], self.currentState['answer'])
        if(hasattr(self,'currentState') and self.currentState['count']-1 == 0):
            #self.disable1()
            self.imcounter.config(text='Оценка завершена.')
            self.ended = True
            return
        self.button_score1.config(state="normal")
        self.button_score2.config(state="normal")
        self.button_score3.config(state="normal")
        self.button_score4.config(state="normal")
        self.button_score5.config(state="normal")
        #self.button_yes2.config(state="normal")
        #self.button_no2.config(state="normal")
        start_time = time.time()
        self.photo = None
        self.currentState = {'answer':[-1]};
        self.currentState['path'], self.currentState['count'] = data.randomunscored()

        print(time.time() - start_time)
        start_time = time.time()

        if(self.currentState['path']):
            image = Image.open(self.currentState['path'])
        else:
            print('No images left to score. Make a new log file.')
            exit()

        print(time.time() - start_time)
        start_time = time.time()

        print(self.currentState)
        self.imcounter.config(text=str('Осталось: '+str(self.currentState['count']-1)))
        self.photo = ImageTk.PhotoImage(image);
        self.imageLabel = Label(self.frame, image = self.photo)
        self.imageLabel.grid(row=5,columnspan=5)
        if (not self.firstImage):
            self.update_clock()
        else:
            self.firstImage = False;

        print(time.time() - start_time)
        start_time = time.time()
    
    def prevImage(self):
        if(hasattr(self,'currentState')):
            data.setScore(self.currentState['path'], self.currentState[0])             
    #def update_clock(self):
    #    if(config['time'] > 1000):
    #        return

    #    if(hasattr(self,'timer_id')):
    #      self.frame.after_cancel(self.timer_id)

        #self.timer_id = self.frame.after(config['time']*1000, self.forceNextImage)

    def forceNextImage(self):
        if(self.ended):
            return
        a = self.currentState['answer']
        if a[0] == -1:
            self.currentState['answer'][0] = 0
        #if a[1] == -1:
        #    self.currentState['answer'][1] = 0
        self.nextImage()

    def scoreandnext(self, score):
        #self.disable1()
        self.currentState['answer'][0] = score;
        #if(self.currentState['answer'][1] > -1):
        self.nextImage()

    def onscore(self, value, event=None):
        self.scoreandnext(value)

    #def onscore1(self, event=None):
    #    self.scoreandnext(1)
    #def onscore2(self, event=None):
    #    self.scoreandnext(2)
    #def onscore3(self, event=None):
    #    self.scoreandnext(3)
    #def onscore4(self, event=None):
    #    self.scoreandnext(4)
    #def onscore5(self, event=None):
    #    self.scoreandnext(5)

    def onyes2(self):
        self.currentState['answer'][0] = 1;
        #self.currentState['answer'][1] = 1;
        self.nextImage()

    def onno1(self, event=None):
        self.currentState['answer'][0] = 0;
        #self.currentState['answer'][1] = 0;
        self.nextImage()

    def onno2(self):
        self.currentState['answer'][1] = 0;
        #self.disable2()
        if(self.currentState['answer'][0] > -1):
            self.nextImage()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"


with codecs.open("./config.json", 'r', 'utf-8') as f:
    config = json.load(f)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', dest='log', type=str, help='Add log')
    parser.add_argument('--cut', nargs=2)
    parser.add_argument('--cutdir', dest='cutdir' , type = str)
    args = parser.parse_args() 
    
    if args.log is None:
        logpath = os.path.abspath(os.getcwd()) + "log.txt"
    else:
        logpath = args.log

    buttonSettins = (config['keys'])
    buttonCount = len(buttonSettins)
    buttons = []
    
    for i in range(buttonCount):
        button = (buttonSettins[i])
        buttons.append(ButtonData(button['text'],button['value'],button['keybinding']))

data = ScoreData(logpath, config['database'])

if args.cut is not None:
        im = Image.open(data.filename) 
        rowcount = args.cut[0]
        colcount = args.cut[1]
        rechight = int(im.height/rowcount) 
        recwight = int(im.width/colcount)
        for i in range(rowcount):
            for j in range(colcount):
                outputIm = im.crop((recwight*j,rechight*i,recwight*(j+1),rechight*(i+1)))
                outputIm.save(args.cutdir + "\r" + str(i) + "_c" + str(j) + ".png")                
sys.exit

if __name__ == '__main__':
    w = Fullscreen_Window()
    w.tk.mainloop()

