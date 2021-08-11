import cv2
import numpy as np
import math

def Canny(img, threshold1, threshold2):
    # 高斯滤波
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    new_gray = cv2.GaussianBlur(gray, (5, 5), 1)
    
    gaussian_result = np.uint8(np.copy(new_gray))
    cv2.imshow("gaussian", gaussian_result)

    # 求解梯度峰值
    W1,H1 = new_gray.shape[:2]
    dx = np.zeros([W1 - 1, H1 - 1])
    dy = np.zeros([W1 - 1, H1 - 1])
    d = np.zeros([W1 - 1, H1 - 1])
    ddegree = np.zeros([W1 - 1, H1 - 1])

    for i in range(1, W1 - 1):
        for j in range(1, H1 - 1):
            dx[i, j] = new_gray[i - 1, j - 1] + 2 * new_gray[i, j - 1] + new_gray[i, j + 1] - \
                new_gray[i - 1, j + 1] - 2 * new_gray[i, j + 1] - new_gray[i + 1, j + 1]
            dy[i, j] = new_gray[i - 1, j - 1] + 2 * new_gray[i - 1, j] + new_gray[i - 1, j + 1] - \
                new_gray[i + 1, j - 1] - 2 * new_gray[i + 1, j] - new_gray[i + 1, j + 1]
            # 图像梯度峰值作为图像强度值
            d[i, j] = np.sqrt(np.square(dx[i, j]) + np.square(dy[i, j]))
            # 梯度方向
            ddegree[i, j] = math.degrees(math.atan2(dy[i, j], dx[i, j]))
            if ddegree[i, j] < 0:
                ddegree[i, j] += 360
    
    d_r = np.uint8(np.copy(d))
    cv2.imshow("gradient", d_r)

    # 非极大值抑制
    W2, H2 = d.shape
    NMS = np.copy(d)
    NMS[0, :] = NMS[W2 - 1, :] = NMS[:, 0] = NMS[:, H2 - 1] = 0
    for i in range(1, W2 - 1):
        for j in range(1, H2 - 1):
            if d[i, j] == 0:
                NMS[i, j] = 0
            else:
                g1 = None
                g2 = None
                if (ddegree[i, j] <= 22.5 and ddegree[i, j] >= 0) or (ddegree[i, j] >= 337.5):
                    g1 = NMS[i, j - 1]
                    g2 = NMS[i, j + 1]
                elif (ddegree[i, j] <= 67.5 and ddegree[i, j] > 22.5) or (ddegree[i, j] <= 337.5 and ddegree[i, j] > 292.5):
                    g1 = NMS[i - 1, j + 1]
                    g2 = NMS[i + 1, j - 1]
                elif (ddegree[i, j] <= 112.5 and ddegree[i, j] > 67.5) or (ddegree[i, j] <= 292.5 and ddegree[i, j] > 247.5):
                    g1 = NMS[i - 1, j]
                    g2 = NMS[i + 1, j]
                elif (ddegree[i, j] <= 157.5 and ddegree[i, j] > 112.5) or (ddegree[i, j] <= 247.5 and ddegree[i, j] > 202.5):
                    g1 = NMS[i - 1, j - 1]
                    g2 = NMS[i + 1, j + 1]
                else:
                    g1 = NMS[i, j - 1]
                    g2 = NMS[i, j + 1]
                
                if NMS[i, j] < g1 or NMS[i, j] < g2:
                    NMS[i, j] = 0

    nms_r = np.uint8(np.copy(NMS))
    cv2.imshow('nms', nms_r)

    # 双阈值算法检测, 连接边缘
    W3, H3 = NMS.shape
    DT = np.zeros([W3, H3], dtype = np.uint8)
    # 定义高低阈值
    TL = min(threshold1, threshold2)
    TH = max(threshold1, threshold2)

    for i in range(1, W3 - 1):
        for j in range(1, H3 - 1):
            if NMS[i, j] < TL:
                DT[i, j] = 0
            elif NMS[i, j] > TH:
                DT[i, j] = 255
            else:
                if NMS[i - 1, j] > TH or NMS[i - 1, j - 1] > TH or NMS[i - 1, j + 1] > TH or NMS[i, j - 1] > TH \
                    or NMS[i, j + 1] > TH or NMS[i + 1, j] > TH or NMS[i + 1, j - 1] > TH or NMS[i + 1, j + 1] > TH:
                    DT[i, j] = 255

    return DT

def main():
    img = cv2.imread('images/seattle.jpg')
    cv2.imshow('src', img)
    result = Canny(img, 60, 120)
    cv2.imshow('canny', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

                 
