import cv2
import numpy as np

def minimized_od_field(img, x1, y1, x2, y2, img_name):
    test_img = img
    width = img.shape[1]
    height = img.shape[0]
    cv2.line(test_img, (0, y1),  (width, y1), color=(0, 255, 0), thickness=5)
    cv2.line(test_img, (0, y2),  (width, y2), color=(0, 255, 0), thickness=5)
    cv2.line(test_img, (x1, 0),  (x1, height), color=(0, 255, 0), thickness=5)
    cv2.line(test_img, (x2, 0),  (x2, height), color=(0, 255, 0), thickness=5)
    cv2.imwrite(img_name, test_img)

def join_pictures_horizontally(img1, img2, num):
    width = max(img1.shape[0], img2.shape[0])
    height = max(img1.shape[1], img2.shape[1])
    tmp = np.zeros((width, height), np.uint8)
    tmp2 = np.zeros((width, height), np.uint8)
    tmp[:img2.shape[0], :img2.shape[1]] = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    tmp2[:img1.shape[0], :img1.shape[1]] = img1
    vis = np.concatenate((tmp2, tmp), axis=1)
    cv2.imwrite('concatenation_' + num + '.png', vis)
    return vis