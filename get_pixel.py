import numpy as np  
import cv2, common
print(cv2.__version__)

common.minimalInitialize()


def show_pixel(event, x, y, flags, param): 
    global img
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print("----")
        prov = common.getProvinceFromPixel((x,y))
        print("Prov: " + str(prov))
        region = common.getRegionFromPixel((x,y))
        print("Region: " + region)
        print("----")
  
def thing(imagename):
    global img

    img = cv2.imread(imagename)
    cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
    cv2.setMouseCallback('image', show_pixel)    
            
    while (1):
       cv2.imshow('image', img)
       if cv2.waitKey(2) & 0xFF == 27:       
           break  
    cv2.destroyAllWindows()
