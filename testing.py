import math
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage.segmentation import active_contour
from skimage import exposure
import skimage
import drawing

def get_circle_scan(img, center, radius, self):
    radius -= 2
    angles = []
    intensities = []
    img2 = img.copy()
    for i in range(0, 360):
        angles.append(i)
        inten = 0
        width = 4
        for j in range(radius, radius + width):
            x = center[0] + radius * math.cos(math.radians(i))
            y = center[1] + radius * math.sin(math.radians(i))
            inten += img[x][y]
            img2[x][y] = 0
        intensities.append(inten / width)
        if i == 0:
             img2 = cv2.circle(img2, (int(y), int(x)), 2, color=1, thickness=2)
        elif i == 90:
             img2 = cv2.circle(img2, (int(y), int(x)), 5, color=1, thickness=2)
        elif i ==180:
            img2 = cv2.circle(img2, (int(y), int(x)), 8, color=1, thickness=2)
    #cv2.imshow('r', img2)
    print 'Intensities; ', intensities
    plt.plot(angles, intensities)
    plt.grid(True)
    plt.ylabel('Intensity')
    plt.xlabel('Angle')
    plt.savefig("intensities.png")
    plt.clf() #clear figure
    drawing.join_pictures_horizontally(img2, cv2.imread("intensities.png"), self.IMAGE_ID + self.EYE_ORIENT)

def snakes_localization(grayscale_image, start_pnt, radius):
    s = np.linspace(0, 2 * np.pi, 400)
    x = start_pnt[0] + radius * np.cos(s)
    y = start_pnt[1] + radius * np.sin(s)
    init = np.array([x, y]).T

    snake = active_contour(skimage.filters.gaussian(grayscale_image, 3),
                           init, bc='periodic', alpha=0.01, beta=10, gamma=0.1,
                           w_line=0, w_edge=-10)
    cv2.imwrite('hist_equal.png', exposure.equalize_adapthist(grayscale_image))
    img = grayscale_image #cv2.cvtColor(grayscale_image, cv2.COLOR_GRAY2BGR)
    cv2.circle(img, (start_pnt[1], start_pnt[0]), radius, color=(0, 255, 0), thickness=3)
    print "Snake size: {}".format(len(snake))
    for i in range(0, len(snake)):
        cv2.circle(img, (int(snake[i][1]), int(snake[i][0])), 1, color=(0, 0, 255), thickness=1)
    cv2.imshow("snakes", img)
    print 'Snakes localization is finished'
