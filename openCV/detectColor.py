import cv2
import numpy

while True:
    img = cv2.imread("openCV/image/image.png")
    img = cv2.resize(img,(400,400))

    # ช่วงสี BGR
    upper = numpy.array([96,255,123])
    lower = numpy.array([4,105,7])

    mask = cv2.inRange(img, lower, upper)
    # กลับเลขฐานสอง
    result = cv2.bitwise_and(img, img,mask=mask)

    if cv2.waitKey(0) & 0xFF == ord("e"):
        break

    cv2.imshow("Original",img)
    cv2.imshow("Mask",mask)
    cv2.imshow("Reault",result)

cv2.destroyAllWindows()