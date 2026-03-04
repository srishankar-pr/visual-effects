import cv2 as cv
import numpy as np

img = cv.imread('test.jpg')
if img is None:
    print("Error: Image not found or unreadable.")
    exit()

scale = 1.0
img_small = cv.resize(img, (0, 0), fx=scale, fy=scale)

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,^."


block_w = 8
block_h = 16

height, width = img_small.shape[:2]
ascii_img = np.ones_like(img_small)*0 # black background

for y in range(0, height, block_h):
    for x in range(0, width, block_w):
        roi = img_small[y:min(y+block_h, height), x:min(x+block_w, width)]
        avg_color = roi.mean(axis=(0,1))
        avg_rgb = avg_color[::-1]
        avg_brightness = 0.299 * avg_rgb[0] + 0.587 * avg_rgb[1] + 0.114 * avg_rgb[2]
        char_idx = int((avg_brightness/255) * (len(chars)-1))
        char = chars[char_idx]
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        thickness = 1
        cv.putText(
            ascii_img,
            char,
            (x, y + block_h),
            font,
            font_scale,
            avg_color.tolist(),
            thickness,
            cv.LINE_AA
        )
#ascii_gray=cv.cvtColor(ascii_img,cv.COLOR_BGR2GRAY)
cv.imwrite('outside.jpg', ascii_img)
