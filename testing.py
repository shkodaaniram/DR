import math
import matplotlib.pyplot as plt
import cv2

def get_circle_scan(img, center, radius):
    radius -= 2
    angles = []
    intensities = []
    img2 = img
    for i in range(0, 360):
        angles.append(i)
        inten = 0
        width = 3
        for j in range(radius, radius + width):
            x = center[0] + radius * math.cos(math.radians(i))
            y = center[1] + radius * math.sin(math.radians(i))
            inten += img[x][y]
            img2[x][y] = 0
        intensities.append(inten / width)
    cv2.imshow('r', img2)
    print 'Intensities; ', intensities
    plt.plot(angles, intensities)
    plt.grid(True)
    plt.ylabel('Intensity')
    plt.xlabel('Angle')
    plt.show()