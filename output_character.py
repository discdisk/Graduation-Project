import cv2
import numpy as np
from img_cut import subimage
from recogonize_v3 import recogonize, recogonize_zh
import time
global name
name = 0
import urllib.request  
  
def getHtml(url):  
    page = urllib.request.urlopen(url)  
    html=page.read()  
    return html  
  

def findPlateNumberRegion(contours, gray):
    region = []
    for i in range(len(contours)):
        cnt = contours[i]
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        area = cv2.contourArea(box)
        # contour区域大于2000 并且比例正确才被认作是车牌
        if (area > 1000):
            ratio = round(max(rect[1]) / min(rect[1]), 2)
            if (2 < ratio < 7):
                # 提取出车牌区域

                img = subimage(gray, rect)
                region.append(img)
    return region


def divide_letters(region, plate_threshhold):
    global name

    characters = []
    for pic in range(len(region)):

        sub_img = region[pic]
        #gray = cv2.cvtColor(sub_img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(
            sub_img, plate_threshhold, 255, cv2.THRESH_BINARY)

        last = 0
        pix_line = 0
        markup = []
        # 像素在y轴上的投影，二值化
        # pix_line为连续像素值，保存在markup中
        # 除去图像上下多余部分
        divide_thresh = 7 * 255 * thresh.shape[1] / 45
        for y in range(thresh.shape[0]):
            pix = sum(thresh[y])
            if ((last < divide_thresh and pix > divide_thresh) or (last > divide_thresh and pix < divide_thresh)):
                markup.append(pix_line)
                pix_line = 0
            pix_line += 1
            last = pix

        if len(markup) < 2:
            continue
        try:
            roiy = np.argmax(markup)
            # 截取上下多余部分
            thresh = thresh[sum(markup[:roiy]):sum(markup[:roiy + 1]), :]
        except Exception as e:
            print(e)

        if(8 > thresh.shape[0] / thresh.shape[1] > 4):
            continue

        # 像素在x轴方向上的投影
        # markdown为每段markup上的像素总和，用以分割字符
        last = 0
        markup = []
        markdown = []
        pix_line = 0
        sum_pix = 0
        divide_thresh = 255 * thresh.shape[0] / 13

        for x in range(thresh.shape[1]):
            pix = sum(thresh[:, x])
            if ((last < divide_thresh and pix > divide_thresh) or (last > divide_thresh and pix < divide_thresh) or (x == thresh.shape[1] - 1)):
                markup.append(pix_line)
                markdown.append(sum_pix)
                sum_pix = 0
                pix_line = 0
            sum_pix += pix
            pix_line += 1
            last = pix

        # markup应大于15

        if len(markup) < 15 or len(markup) > 40:
            continue

        individual_num = []
        markup_sort = markup.copy()
        markup_sort.sort()
        markdown_sort = markdown.copy()
        markdown_sort.sort()
        maxlen = markup_sort[-4]

        for i in range(len(markup)):
            if maxlen * 1.1 > markup[i] > maxlen * 0.2 and markdown[i] > markdown_sort[-8]:
                individual_num.append(
                    thresh[:, sum(markup[:i]):sum(markup[:i + 1])])

        if len(individual_num) == 7:
            for im_num in range(7):
                res = cv2.resize(individual_num[im_num], (32, 64),
                                 interpolation=cv2.INTER_CUBIC)
                characters.append(res)
    return characters


def findPlate(img, Environment_threshhold):
    global name
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray, (5, 5), 1)
    ret, thresh = cv2.threshold(
        gray1, Environment_threshhold, 255, cv2.THRESH_BINARY)
    blur = cv2.GaussianBlur(thresh, (5, 5), 1)
    edge_img = cv2.Canny(gray, threshold1=120, threshold2=300)
    image, contours, hierarchy = cv2.findContours(
        edge_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img1 = thresh.copy()
    img1 = cv2.drawContours(img1, contours, -1, (0, 255, 255), 2)
    cv2.imshow('winname', img1)
    region = findPlateNumberRegion(contours, gray)
    return region


def output_character(frame):
    output = []
    evidence = []
    plate = findPlate(frame, 100)
    character = divide_letters(plate, 100)
    amount = len(character)

    if amount > 0:
        print('plate amount:', amount / 7)
        for i in range(amount):
            if i % 7 == 0:
                out, evi = recogonize_zh(character[i])
                #cv2.imshow('zh', character[i])
            else:
                out, evi = recogonize(character[i])
                #cv2.imshow(str(i), character[i])
            output.append(out)
            evidence.append(evi)
        answersum = []
        for answer in range(amount // 7):
            answersum.append(sum(evidence[answer * 7:answer * 7 + 7]))
        maxnum = (np.argmax(answersum))
        print('proper plate', maxnum)
        print('plate number', output[maxnum * 7:maxnum * 7 + 7])
        return(output[maxnum * 7:maxnum * 7 + 7],max(answersum))


if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    while True:
        time.sleep(1)
        distance=getHtml("http://192.168.4.1/check").decode()
        distance=3
        print('distance',distance)
        if float(distance)<10:
            (grabbed, frame) = camera.read()
            while True:
                output = []
                evidence = []
                (grabbed, frame) = camera.read()
                frame=cv2.imread('2.jpg')
                plate = findPlate(frame, 80)
                character = divide_letters(plate, 100)
                amount = len(character)
                print('plate amount:', amount )

                if amount > 0:
                    print('plate amount:', amount / 7)
                    for i in range(amount):
                        if i % 7 == 0:
                            out, evi = recogonize_zh(character[i])
                            #cv2.imshow('zh', character[i])
                        else:
                            out, evi = recogonize(character[i])
                            #cv2.imshow(str(i), character[i])
                        output.append(out)
                        evidence.append(evi)
                    answersum = []
                    for answer in range(amount // 7):
                        answersum.append(sum(evidence[answer * 7:answer * 7 + 7]))
                    maxnum = (np.argmax(answersum))
                    print('proper plate', maxnum)
                    print('plate number', output[maxnum * 7:maxnum * 7 + 7])
                    getHtml("http://192.168.4.1/complete")
                    break

                key = cv2.waitKey(30)

                # if the 'q' key is pressed, stop the loop
                if key == ord("q"):
                    break
    cv2.waitKey(0)
    camera.release()
    cv2.destroyAllWindows()
