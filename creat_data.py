import cv2
import numpy as np
data = []
index = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
         'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
for x in range(34):
    dat = cv2.imread('model/zh' + str(x) + '.jpg')
    dat = cv2.cvtColor(dat, cv2.COLOR_BGR2GRAY)
    dat = cv2.erode(dat, (5,5))
    dat = cv2.erode(dat, (5,5))
    dat = cv2.erode(dat, (5,5))
    dat = cv2.erode(dat, (5,5))
    # dat = cv2.GaussianBlur(dat,(5,5),1)
    # dat = cv2.blur(dat, (5,5))
    #dat_ret, dat_thresh = cv2.threshold(dat, 127, 255, cv2.THRESH_BINARY)
    dat_res = cv2.resize(dat, (16, 32),
                         interpolation=cv2.INTER_CUBIC)
    data.append(dat_res.reshape(16 * 32))
np.save("zh_data_16x32_35", data)

   

