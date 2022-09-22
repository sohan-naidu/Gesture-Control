import keras
import cv2 
import numpy as np

def executeTask(task):

    '''--------------------------
    0 - CLOSED PALM
    1 - DOWN
    2 - LEFT
    3 - RIGHT
    4 - UP
    5 - NONE
    6 - OPEN PALM
    7 - THUMBS DOWN
    --------------------------'''
    #global program_state
    task = int(task)
    if task == 0:
        print("closed")

def process_frame(target_frame):
    input = preprocess(target_frame)
    output = model.predict(input)[0]
    class_result = list(output).index(max(output))
    print("class result : ")
    print(class_result)
    return str(class_result)


def preprocess(frame):
    #h_lb,th_ub = getThreshTrackBar()
    mask = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    _,mask = cv2.threshold(mask,130, 255,cv2.THRESH_BINARY_INV)
    frame = cv2.bitwise_and(frame,frame,mask=mask)

    #-------FINAL EXTRACTION OF HAND FROM IMAGE---------#
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    kernel = np.ones((21,21),np.uint8)
    #l_b, u_b = getHSVTrackbarValues()
    l_b, u_b = (np.array([0, 58, 71]), np.array([83, 225, 255]))
    mask = cv2.inRange(frame,l_b,u_b)
    mask = cv2.dilate(mask,kernel)
    frame = cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow("processed",frame)
    frame = cv2.cvtColor(frame,cv2.COLOR_HSV2BGR)

    #-------prepare for processing-------#
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow("frame",frame)
    frame = cv2.GaussianBlur(frame,(15,15),0)
    frame = cv2.resize(frame,(64,64))
    frame = np.reshape(frame,(64,64,1))
    frame = np.expand_dims(frame,axis=0)
    return frame

model = keras.models.load_model('C:/Users/Sohan/GitHub/Gesture Control/final/models/gestureControlModel.h5')
print("MODEL INITIALIZED")

#global  program_state
prev_processed = -1
processed_cnt = 0
decision_threshold = 2
capture = cv2.VideoCapture(0)
while(capture):
    
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

    roi = frame[top:bottom, left:right]

    cv2.imshow("window", roi)
    processed = process_frame(roi)

    #print(processed)
    if processed == prev_processed:
         processed_cnt += 1
    else: 
        processed_cnt = 1
    prev_processed = processed
    if processed_cnt == decision_threshold:
        #print("EXECUTING TASK")
        executeTask(processed)
        processed_cnt = 0
        #-----------------DISPLAY CAMERA------------------#
    frame = cv2.putText(frame,processed,(64 ,64),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
    cv2.imshow("cam",frame)
    cv2.waitKey(1)

