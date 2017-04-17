import cv2

def minimized_od_field(img, x1, y1, x2, y2, img_name):
    test_img = img
    width = img.shape[1]
    height = img.shape[0]
    cv2.line(test_img, (0, y1),  (width, y1), color=(0, 255, 0), thickness=5)
    cv2.line(test_img, (0, y2),  (width, y2), color=(0, 255, 0), thickness=5)
    cv2.line(test_img, (x1, 0),  (x1, height), color=(0, 255, 0), thickness=5)
    cv2.line(test_img, (x2, 0),  (x2, height), color=(0, 255, 0), thickness=5)
    cv2.imwrite(img_name, test_img)