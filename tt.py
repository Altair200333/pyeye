import os
from PIL import ImageGrab
import PIL
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from googletrans import Translator
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from skimage import data
import tra
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
translator = Translator()

def extt(im):

    print("exec..")
    #blur = cv.GaussianBlur(cv.imread('screenshot.png',0), (1, 1), 0)
    #ret3, th3 = cv.thres#hold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    #th3 = cv.adaptiveThreshold(cv.imread('screenshot.png',0),255,cv.ADAPTIVE_THRESH_MEAN_C,\
            #cv.THRESH_BINARY,11,2)

    imS = cv.imread('screenshot.png', 0)
    #print(imS)
    height = len(imS)
    width = len(imS[0])
    newimg = cv.resize(imS, (int(width), int(height)))

    th3 = cv.threshold(newimg,127,255,cv.THRESH_BINARY)
    #cv.imwrite('messigray.png', th3)

    #---
    text = pytesseract.image_to_string(newimg)

    #os.remove("screenshot.png")
    print("text is: "+text)  # print image_to_string(Image.open(‘find.jpg’))
    text = tra.correct_word(text)
    trans = []
    if(len(text.split(' '))>1):
        trans.append(tra.yandexT(text))

    else:
        trans = tra.yandexD(text)
    if(len(trans)==0):
        trans.append("")
    print(trans)
    return callb(text, trans)

def callb(text, trans):
    return [text, trans]

def write(res):
    file = open("words.txt", "a+")
    str = ""

    for i in res[1]:
        str+=i+"/ "
    file.write(res[0] +" - " + str+"\r")
    file.close()