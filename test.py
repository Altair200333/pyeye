import datetime
import threading
import tkinter as tk # Python 3
import win32api
import win32gui

import pyscreenshot as ImageGrab
import time

from pynput import keyboard
import os
import tt
from tkinter import Tk, Canvas, Frame, BOTH, W
from PIL import ImageGrab
from pynput.mouse import Controller
from ctypes import windll, Structure, c_long, byref, c_ulong

root = tk.Tk()

mouse = Controller()
point =  [0.0,0.0]
start = [0.0, 0.0]
timeout = 200
awake = 0
current = set()
COMBINATIONS = [
    {keyboard.KeyCode(char='A'), keyboard.Key.alt_l},
    {keyboard.KeyCode(char='a'), keyboard.Key.alt_l}
]

lastResult = ["nothing yet",""]
curText = "nothing.."
class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { pt.x, pt.y}


def execute():
    global timeout
    global awake, start
    if awake == 0:
        print ("Do Something")
        start[0], start[1] = win32api.GetCursorPos()
        awake = 1
        timeout = 30
def unexecute():
    global awake,timeout, lastResult
    if awake == 1:
        print("unex")

        awake = 0;
        timeout = 200
        im = 0
        if (start[0] != point[0]):
            try:
                print(str(start[0])+" "+str(point[0]))

                im = ImageGrab.grab(bbox=(start[0]+1,start[1]+1,point[0],point[1]))
                im.save('screenshot.png')
                print("shot")
            except Exception as e:
                print(e)

            try:
                global curText
                res = tt.extt(im)
                #print(res)
                curText = res[0]
                if len(res[0]) > 0:
                    lastResult = res

                    tt.write(res)
            except Exception as e:
                print(e)
def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):

    if any([key in COMBO for COMBO in COMBINATIONS]):
        try:
            current.remove(key)
        except Exception as e:
            current.clear()
            print(e)
        unexecute()
    current.clear()


def fun1():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
thread1 = threading.Thread(target = fun1)
thread1.start()

# The image must be stored to Tk or it will be garbage collected.
#root.image = tk.PhotoImage(file='startup.gif')
label = tk.Canvas(height=1080, width= 1920, bd=0, bg = "red", highlightthickness=0, takefocus = True)
root.overrideredirect(True)
root.geometry("+0+0")
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "red")
label.pack()

def update():
    global timeout
    global point

    point[0], point[1] = win32api.GetCursorPos()
    #print(str(start[0])+" - "+str(point[0]))
    if awake == 1:
        #print("up")
        label.delete("all")
        label.create_rectangle(start[0], start[1], point[0], point[1], outline="#fb0", fill="red")

        #label.config(text='sad' + str(datetime.datetime.now()))
    if awake == 0:

        #print("-")
        label.delete("all")

        label.create_rectangle(1850, 1010, 1870, 1030, outline="#fb0", fill="red")

        label.create_text(1600, 1015, fill="orange", font="Times 15  bold", text=curText)

        if len(lastResult[1])>0 and lastResult[1][0]!="":
            label.create_text(1800, 1015, fill="grey", font="Times 20  bold", text=lastResult[0])
            for i in range(0, len(lastResult[1])):
                label.create_text(1800, 990-16*i, fill="grey", font="Times 22  bold", text=lastResult[1][i])
        else:
            label.create_text(1800, 980, fill="orange", font="Times 20  bold", text="Nothing")
        #label.config(text='Text on the screen'+str(datetime.datetime.now()))
    root.after(timeout, update)

root.after(100, update)

label.mainloop()