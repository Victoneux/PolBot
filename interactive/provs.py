import numpy as np
import common
import cv2
print(cv2.__version__)

common.initialize()

def show_pixel(event, x, y, flags, param):
    global img
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print("x:",x," y:",y, img[y,x,:])
        color = img[y,x,:]
        color = (color[2],color[1],color[0])
        print(color)
        prov = common.getProvinceFromColor(color)
        print(prov)
        mask = cv2.inRange(img,img[y,x,:],img[y,x,:])
        img = cv2.bitwise_not(img, img, mask=mask)

path = "./map/provinces.bmp"
img = cv2.imread(path)
#img = cv2.resize(img, (300,300))
cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
cv2.setMouseCallback('image', show_pixel)

while True:
    cv2.imshow('image', img)
    if cv2.waitKey(2) & 0xFF == 27:
        break
cv2.destroyAllWindows()