import cv2
import numpy as np
src = cv2.imread("4708f19c-2085-437b-8e67-bb95e000b8c6.jpg")
gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray_src,60,120)
cv2.imshow("canny",canny)
#cv2.imshow("input image", src)
#cv2.imshow("gray image", gray_src)
#cv2.waitKey(0)
gray_src = cv2.bitwise_not(gray_src)
#二值化
binary_src = cv2.adaptiveThreshold(gray_src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
cv2.namedWindow("result image", cv2.WINDOW_AUTOSIZE)
cv2.imshow("result image", binary_src)
#cv2.waitKey(0)
# 提取水平线  src.shape[1]得到src列数
#hline = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1), (-1, -1))
hline = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 4), (-1, -1)) #定义结构元素，卷积核
# 提取垂直线  src.shape[0]得到src行数
vline = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 1), (-1, -1))
#vline = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# 这两步就是形态学的开操作——先腐蚀再膨胀
#temp = cv2.erode(binary_src, hline)   #腐蚀
#dst = cv2.dilate(temp, hline)      #膨胀
# 开运算
dst = cv2.morphologyEx(binary_src, cv2.MORPH_OPEN, hline)  #水平方向
dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, vline)  #垂直方向
#将二指图片的效果反转既黑色变白色，白色变黑色。 非操作
dst = cv2.bitwise_not(dst)
cv2.imshow("Final image", dst)
cv2.waitKey(0)