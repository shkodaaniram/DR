import math
import matplotlib.pyplot as plt
import cv2
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