import numpy as np
import cv2
import time
blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByColor = True
blobparams.blobColor = 255
blobparams.filterByArea = False
blobparams.filterByCircularity = False
blobparams.filterByConvexity = False
blobparams.filterByInertia = False
blobparams.minDistBetweenBlobs = 100
blobparams.minArea = 200
blobparams.maxArea = 5000
detector = cv2.SimpleBlobDetector_create(blobparams)

greenH_min = 35
greenS_min = 26
greenV_min = 58
greenH_max = 79
greenS_max = 116
greenV_max = 138

purpleH_min = 35
purpleS_min = 26
purpleV_min = 58
purpleH_max = 79
purpleS_max = 116
purpleV_max = 138

green = [greenH_min, greenS_min, greenV_min, greenH_max, greenS_max, greenV_max]


with open("conf.txt", "w") as conf:
    conf.write("green")
    for i in range(len(green)):
        conf.write(str(green[i]) + "\n")
    conf.write("---")

cap = cv2.VideoCapture(2)
def updateValue(value):
        global trackbar_value
        trackbar_value1 = value
        return
def updateValue2(value):
        global greenS_min
        greenS_min = value
        return
def updateValue3(value):
        global greenV_min
        greenV_min = value
        return
def updateValue4(value):
        global greenH_max
        greenH_max = value
        return
def updateValue5(value):
        global greenS_max
        greenS_max = value
        return
def updateValue6(value):
        global greenV_max
        greenV_max = value
        return



cv2.namedWindow("Trackbars")
cv2.createTrackbar("h_min","Trackbars",greenH_min,255,updateValue)
cv2.createTrackbar("s_min","Trackbars",greenS_min,255,updateValue2)
cv2.createTrackbar("v_min","Trackbars",greenV_min,255,updateValue3)
cv2.createTrackbar("h_max","Trackbars",greenH_max,255,updateValue4)
cv2.createTrackbar("s_max","Trackbars",greenS_max,255,updateValue5)
cv2.createTrackbar("v_max","Trackbars",greenV_max,255,updateValue6)
fps = 0
counter = 0

kernel = np.ones((5,5),np.uint8)

end = 3
start = 1

while True:
    seconds = end - start
    start = time.time()

    ret, frame = cap.read()
    lowerLimits = np.array([greenH_min, greenS_min, greenV_min])
    upperLimits = np.array([greenH_max, greenS_max, greenV_max])
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    erosion = cv2.erode(frame,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
    thresholded = cv2.inRange(dilation, lowerLimits, upperLimits)
    outimage = cv2.bitwise_and(frame, frame, mask = thresholded)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 200)

    #outimage = cv2.bitwise_not(outimage)

    try:
        keypoints = detector.detect(thresholded)
        print(len(keypoints))
        for k in keypoints:
            cv2.putText(frame, str(int(k.pt[0])) + " " + str(int(k.pt[1])), (int(k.pt[0]), int(k.pt[1])),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.putText(frame, str(round(1/seconds,1)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    except:
        continue


    cv2.imshow('thresholded', thresholded)
    cv2.imshow('Original', frame)
    counter+=1
    cv2.imshow('Processed', outimage)

    end = time.time()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
