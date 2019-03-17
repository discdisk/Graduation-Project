import cv2
from numpy import sin,cos
import numpy as np

def subimage(image, rect):
    center=rect[0]
    theta=rect[-1]
    width=int(rect[1][0])
    height=int(rect[1][1])

    theta *= np.pi / 180 # convert to rad

    v_x = (cos(theta), sin(theta))
    v_y = (-sin(theta), cos(theta))
    s_x = int(center[0]) - v_x[0] * (width / 2) - v_y[0] * (height / 2)
    s_y = int(center[1]) - v_x[1] * (width / 2) - v_y[1] * (height / 2)


    mapping = np.array([[v_x[0],v_y[0], s_x],
                        [v_x[1],v_y[1], s_y]])


    sub_img = cv2.warpAffine(image,mapping,(width, height),flags=cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)
    if sub_img.shape[0]>sub_img.shape[1]:
        sub_img = cv2.rotate(sub_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #cv2.imshow(str(int(sub_img.shape[1]/sub_img.shape[0]))+'   '+str(theta), sub_img) 
    return sub_img
if __name__=='__main__':
    im = cv2.imread('owl.jpg')
    cv2.imshow('winname', im)
    
    rect=((110,125),(100,200),30)
    subimage(im, rect)
    cv2.waitKey(0)
    cv2.destroyAllWindows
