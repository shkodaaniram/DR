import cv2
import CONST
import preprocessing as pp
import drawing
import OD_utils as odu

def get_od_point(self, gray_img, start, part, stop, part_end):
    point = pp.getBigRectIntensity(gray_img,start, stop, part, part_end)
    if self.EYE_ORIENT == 'right':
        point = (point[0], point[1] + CONST.vessel_width * 2)
    elif self.EYE_ORIENT == 'left':
        point = (point[0], point[1] - CONST.vessel_width * 2)
    self.POINT = point
    return point

def choose_optic_disc_size(self, img, color_img, point):
    intensity_diff = []
    step = CONST.ellipse_axes_difference  #difference between axes
    bagel_width = CONST.bagel_width
    prev_aver_color = 0
    exten = 3
    gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    for i in range(35, 75, exten):
        step = int(i * CONST.percentage_between_axes)
        points = odu.getAllBagelPoints(img, gray_img, point, (i+bagel_width, i+bagel_width+step), (i, i+step), 90, 90, 120)
        if len(points) == 0:
            points = odu.getAllBagelPoints(img, gray_img, point, (i+bagel_width, i+bagel_width+step), (i, i+step), 90, 90, 30)
        min_color = min(points)
        min_threshold = min(points) + (max(points) - min(points)) * 0.2
        print 'Min_color: {};max_color: {}  min_threshold: {}'.format(min_color,max(points), min_threshold)
        points_threshold = []
        for j in range(0, len(points)):
            if points[j] >= min_threshold:
                points_threshold.append(points[j])
        print 'Start length: {} Finish length: {}'.format(len(points), len(points_threshold))
        aver_color = odu.getAveradgeColor(points_threshold)
        print 'i: {} av - {} : {}'.format(i, aver_color, aver_color - prev_aver_color)
        intensity_diff.append(aver_color - prev_aver_color)
        prev_aver_color = aver_color

    intensity_diff = intensity_diff[2:]
    min_intensity = min(intensity_diff)
    print 'Intensity_diff: ', intensity_diff
    print 'Min_intensity: ', min_intensity, intensity_diff.index(min_intensity)
    index_min_intensity = (intensity_diff.index(min_intensity) + 2) * exten + 35
    print 'min_intensity - {}; index_min_intensity - {}'.format(min_intensity, index_min_intensity)
    color_img = cv2.circle(color_img, (point[1], point[0]), 2, color=(0,255,0), thickness=3) #ellipse center
    axes = (int(index_min_intensity+index_min_intensity*CONST.percentage_between_axes), int(index_min_intensity))
    pict = cv2.ellipse(color_img, (point[1], point[0]), axes, 90, 0, 360,(0,0,255),2)
    cv2.imwrite(self.IMAGE_ID + self.EYE_ORIENT + "_binar.jpeg", pict)
    return axes

def get_optic_disc(self):
    img = cv2.imread(CONST.resized_img_path)
    width = img.shape[1]
    height = img.shape[0]
    print 'Resized image width - {}, height - {}'.format(width, height)
    start, part, stop, part_end = pp.minimize_od_field(self, img)
    r_comp = pp.get_r_component(img)
    gray_blur,closing_gray,median_vessels = pp.morphology_open_close(r_comp)
    #OD center finding
    point = get_od_point(self, gray_blur, start, part, stop, part_end)
    start, part, stop, part_end = pp.refresh_minimized_od_field(point, start, part, stop, part_end)
    drawing.minimized_od_field(img, start, part, stop, part_end, 'refreshed_minimized_od_lines.jpg')
    #Automatic disc localization
    ellipse_axes = choose_optic_disc_size(self, r_comp, img, point)
    print 'OD size was found: center - ({}); axes - {}'.format(point, ellipse_axes)

