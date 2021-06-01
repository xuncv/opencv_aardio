import cv2
import numpy as np
src = cv2.imread("../images/Lena.jpg")
# dst = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
dst = cv2.medianBlur(src,5)

cv2.imshow("src",src)
cv2.imshow("dst",dst)
cv2.waitKey()