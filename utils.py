import CONST

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