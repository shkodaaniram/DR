import CONST
import cv2
import numpy as np

def onScaleImg(img):
    width = img.GetWidth()
    height = img.GetHeight()
    screen_res = CONST.screen_resol_x, CONST.screen_resol_y
    scale_width = screen_res[0] / width
    scale_height = screen_res[1] / height
    scale = min(scale_width, scale_height)
    window_width = int(width * scale)
    window_height = int(height * scale)
    img = img.Scale(window_width, window_height)
    print '{} - {}'.format(img.GetWidth(), img.GetHeight())
    return img

def truncateImg(filename):
    img = cv2.imread(filename)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    max_value = 255
    th, thresh = cv2.threshold(gray_img, CONST.threshold_for_truncate, max_value, cv2.THRESH_BINARY)
    x, y, w, h = cv2.boundingRect(thresh)
    print x,y,w,h
    return img[y:y + h, x:x + w]

def resizeImg(img):
    img = truncateImg(img)
    return cv2.resize(img, (int(img.shape[1] / CONST.resize), int(img.shape[0] / CONST.resize)))