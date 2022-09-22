import cv2
import numpy as np

capture = cv2.VideoCapture(0)





def save_frame(frame, file_number):
    file_number += 1
    file_name = directory + str(file_number) + ".jpg"
    cv2.imwrite(file_name, frame)
    print("SAVED",file_name)
    return frame, file_number

def preprocess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    _, threshold = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY_INV)

    #cv2.imshow("processed", threshold)
    frame = cv2.bitwise_and(frame, frame, mask=threshold)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel = np.ones((21, 21), np.uint8)
    l_b, u_b = (np.array([0, 58, 71]), np.array([83, 225, 255]))
    mask = cv2.inRange(frame, l_b, u_b)
    mask = cv2.dilate(mask, kernel)
    frame = cv2.bitwise_and(frame, frame, mask=mask)
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    #cv2.imshow("processed", frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (15, 15), 0)
    frame = cv2.resize(frame, (64, 64))
    
    return frame



file_number = 0

while(capture):
    directory = "final/data/right/"
    _, frame = capture.read()
    point1 = (25, 350)
    point2 = (200, 120)
    top, right, bottom, left = 200, 200, 400, 40
    color = (255, 250, 50)
    thickness = 2
    res = (900, 600)
    frame = cv2.rectangle(frame, (left, top), (right, bottom), color, thickness)
    cv2.namedWindow("window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('window', res)


    
    #roi = frame[point1[0]:point2[0], point1[1]:point2[1], :]
    #top, right, bottom, left = 10, 350, 225, 590
    roi = frame[top:bottom, left:right]
    #rint(roi)
    cv2.imshow("window", roi)
    processed = preprocess(roi)
    #a, b = segment(frame)
    saved, file_number = save_frame(processed, file_number)
    cv2.waitKey(1)
