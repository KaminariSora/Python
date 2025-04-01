import cv2

cap = cv2.VideoCapture(0)

while(True):
    check, frame = cap.read() # รับค่าจากกล้อง Frame ต่อ Frame
    cv2.imshow("Output",frame)

    if cv2.waitKey(1) &0xFF == ord("e"): # รอกดปุ่ม e
        break

cap.release()
cv2.destroyAllWindows()