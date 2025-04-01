import cv2

img = cv2.imread("openCV/image/S__4857873_0.jpg",0)
imgResize = cv2.resize(img,(400,400))

cv2.imshow("Output",imgResize)
cv2.waitKey(0)
cv2.destroyAllWindows()