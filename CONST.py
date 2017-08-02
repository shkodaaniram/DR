screen_resol_x = 720.0
screen_resol_y = 576.0

resized_img_path = r"D:\Diplom\resized_img.jpeg"

tmp = 2

threshold_for_truncate = 45
resize = 3 * tmp #value for resizing initial image
vessel_width = 30 / resize

max_od_radius = 125

ellipse_axes_difference = 10
bagel_width = 3
percentage_between_axes = 0.15

#rectangle size for intensities for finding OD center
rect_x = 180 / tmp
rect_y = 160 / tmp
