# Sugiarto Wibowo - c11180016
import cv2
import serial
import time

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

cap = cv2.VideoCapture(1)
cap.set(3, 480)
cap.set(4, 320)


start_point = (300, 100)
end_point = (900, 500)
color = (0, 255, 0)
thickness = 4

tracker = cv2.TrackerCSRT_create()
success, img = cap.read()
bbox = cv2.selectROI("Tracking", img, False)
tracker.init(img, bbox)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


def drawbox(img, bbox):
    rows, cols, sucess = img.shape
    center = int(cols / 2)

    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x,y),((x+w),(y+h)),(255,0,255),3,1)
    cv2.putText(img, 'Status : ' + "Tracking", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    x_medium = int((x + x + w) / 2)
    cv2.line(img, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    print("Medium : ", x_medium, " Center : ", center)

    #  move servo
    if x_medium < center - 20:
        print('aaaaaaaaaa')
        write_read(str(1))
    elif x_medium > center + 20:
        print('bbbbbbbbbb')
        write_read(str(2))


while True:
    timer = cv2.getTickCount()
    success, img = cap.read()
    success,bbox = tracker.update(img)
    print("Ukurannnnnnnn: ", img.shape)
    print(int(bbox[0]), int(bbox[1]))

    if success:
        drawbox(img, bbox)
    else:
        cv2.putText(img, "lost", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)

    cv2.putText(img, 'fps   : ' + str(int(fps)), (75,50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
    cv2.imshow("Tracking", img)

    if cv2.waitKey(1) & 0xff ==ord('x'):
        break

cap.release()
cv2.destroyAllWindows()

