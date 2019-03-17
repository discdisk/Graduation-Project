import cv2
import numpy as np


def recogonize(thresh):
    res = cv2.resize(thresh, (8, 16), interpolation=cv2.INTER_CUBIC)
    res = res.reshape(8 * 16)
    # index = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
    #          'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    data = np.load('data_8x16.npy')
    evidences = []
    for x in range(36):
        evid = 0
        evimax = 0
        for y in range(8 * 16):
            evid += (res[y] - 127) * (data[x][y] - 127)
            evimax += pow(data[x][y] - 127, 2)

        evidences.append(evid / evimax * 100)
    num = np.argmax(evidences)
    # for x in range(36):
    #     if evidences[x] > 50:
    #         print('familier character',index[x], evidences[x])
    if num > 9 and num!=18 and num!=24:
        print('the number is :', chr(65 + num - 10), max(evidences), num)
        return chr(65 + num - 10), max(evidences)
    elif num<10:
        print('the number is :', num, max(evidences))
        return str(num), max(evidences)
    else:
        print('the number is :', num, max(evidences))
        if num ==18:
            return str(1), max(evidences)
        else:
            return str(0), max(evidences)


def recogonize_zh(thresh):
    res = cv2.resize(thresh, (16, 32), interpolation=cv2.INTER_CUBIC)
    res = res.reshape(16 * 32)
    index = ['皖', '京', '津', '沪', '渝', '冀', '晋', '辽', '吉', '黑', '苏', '浙', '闽', '赣', '鲁', '豫',
             '鄂', '湘', '粤', '琼', '川', '贵', '云', '陕', '甘', '青', '藏', '贵', '蒙', '宁', '新', '港', '澳', '台']
    data = np.load('zh_data_16x32_35.npy')
    evidences = []
    for x in range(34):
        evid = 0
        evimax = 0
        for y in range(16 * 32):
            evid += (res[y] - 127) * (data[x][y] - 127)
            evimax += pow(data[x][y] - 127, 2)

        evidences.append(evid / evimax * 100)
    num = np.argmax(evidences)
    print(index[num], max(evidences))
    return index[num], max(evidences)


if __name__ == "__main__":
    for x in range(1):
        print('testing:', str(x))
        im = cv2.imread('1.jpg')
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)
        recogonize(thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows
