import cv2

img = cv2.imread("openCV/image/S__4857873_0.jpg")

imgResize = cv2.resize(img,(500,500))

# line(ภาพ, จุดเริ่มต้น(x, y), จุดส่งท้าย(x, y), สี(BGR), ควสามหนา)
cv2.line(imgResize,(0,0),(100,100),(255,0,0),10)

cv2.arrowedLine(imgResize,(100,10),(110,110),(0,255,0),10)

# วาดสี่เหลี่ยม 
# rectangle(ภาพ, มุมที่1(บนซ้าย), มุมที่สอง(ล่างขวา), สี, ความหนา)
cv2.rectangle(imgResize,(300,200),(400,300),(0,0,0),5)

cv2.imshow("Output",imgResize)
cv2.waitKey(0)
cv2.destroyAllWindows()