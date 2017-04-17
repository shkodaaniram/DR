import drawing
import cv2
import CONST

def minimize_od_field(self, img):
    width = img.shape[1]
    height = img.shape[0]
    x1 = 0
    x2 = width
    if self.EYE_ORIENT == 'right':
        if width / 3 > x1: x1 = width / 3
    elif self.EYE_ORIENT == 'left':
        if width - width / 3 < x2: x2 = width - width / 3
    else: print 'ERROR: Undefined eye orientation!'
    y1 = int(height / 3.5)
    y2 = height - y1
    print 'Minimized OD field: (x1, y1) - ({}, {}), (x2, y2) - ({}, {})'.format(x1, y1, x2, y2)
    drawing.minimized_od_field(img, x1, y1, x2, y2, 'minimized_od_lines.jpg')
    return x1, y1, x2, y2

def get_r_component(img):
    r_comp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    r_comp = r_comp[:, :, 0] #getting R-component
    cv2.imwrite('r_component.png', r_comp)
    return r_comp

def morphology_open_close(gray):
    closing = gray
    vessel_width = CONST.vessel_width * 2
    for i in range (15, vessel_width):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(i, i))
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    closing_gray = closing - gray
    median_vessels = cv2.medianBlur(closing-gray, 5)
    return closing, closing_gray, median_vessels

def getBigRectIntensity(img, start, stop, start_height, height):
    integral = cv2.integral(img)
    rect_x = int(180 / 3) - 1
    rect_y = int(160 / 3) - 1
    coord = []
    intensity = []
    for j in range(start + rect_y, stop - rect_y, 1):
        for i in range(start_height + rect_x, height - rect_x, 1):
            intensity.append(integral[i][j] + integral[i-rect_x][j-rect_y] - integral[i-rect_x][j] - integral[i][j-rect_y])
            coord.append((int(i - rect_x / 2), int(j - rect_y / 2)))
    test_pnt = coord[intensity.index(max(intensity))]
    return test_pnt

def refresh_minimized_od_field(point, start, part, stop, part_end):
    radius = CONST.max_od_radius
    if point[0] - radius > part:
        part = point[0] - radius
    if point[0] + radius < part_end:
        part_end = point[0] + radius
    if point[1] + radius < stop:
        stop = point[1] + radius
    if point[1] - radius > start:
        start = point[1] - radius
    return start, part, stop, part_end