import cv2
import math
import CONST

def getAveradgeColor(pnts):
    sum = 0
    for pnt in pnts:
        sum += pnt
    return sum / float(len(pnts))

def isEllipsePoint(center, axes, angle, point):
    if float((math.cos(angle)*(point[0]-center[0]) + math.sin(angle)*(point[1]-center[1]))**2)/float(axes[0]**2) + float((math.sin(angle)*(point[0]-center[0]) + math.cos(angle)*(point[1]-center[1]))**2)/float(axes[1]**2) <= 1.0:
        return True
    return False

def getAllEllipsePoints(img, center, axes, angle):
    angle = math.radians(angle)
    all_points = []
    for i in range(center[1]-axes[0], center[1]+axes[0]):
        for j in range(center[0]-axes[1], center[0]+axes[1]):
            if isEllipsePoint(center, axes, angle, (j, i)):
                all_points.append(img[j][i]) # 22.02 changed from img[i][j]
    return all_points

def getAllBagelPoints(img_hls, gray_img, center, l_axes, s_axes, l_angle, s_angle, threshold):
    #get bagel points
    l_angle = math.radians(l_angle)
    s_angle = math.radians(s_angle)
    all_points = []
    x_start = 0
    y_start = 0
    x_end = img_hls.shape[0]
    y_end = img_hls.shape[1]
    if center[0]-l_axes[1] > x_start:
        x_start = center[0]-l_axes[1]
    if center[0]+l_axes[1] < x_end:
        x_end = center[0]+l_axes[1]
    if center[1]-l_axes[0] > y_start:
        y_start = center[1]-l_axes[0]
    if center[1]+l_axes[0] < y_end:
        y_end = center[1]+l_axes[0]
    for i in range(x_start, x_end):
        for j in range(y_start, y_end):
            if isEllipsePoint(center, l_axes, l_angle, (i, j)) and not isEllipsePoint(center, s_axes, s_angle, (i, j)):
                if gray_img[i][j] > threshold: #!= 0:
                   all_points.append(img_hls[i][j])   # for gray on channel img
    return all_points
