import cv2
import CONST
import preprocessing as pp

def get_vessels(self):
    img = cv2.imread(CONST.resized_img_path)
    width = img.shape[1]
    height = img.shape[0]
    g_comp = pp.get_g_comonent(img)
    cv2.imshow('g_component', g_comp)
