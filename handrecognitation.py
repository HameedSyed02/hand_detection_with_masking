import cv2
import numpy as np


def empty(a):
    pass


def trackbars():
    """cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 260)
    cv2.createTrackbar("Hue min", "TrackBars", 0, 179, empty)
    cv2.createTrackbar("Hue max", "TrackBars", 35, 179, empty)
    cv2.createTrackbar("sat min", "TrackBars", 1, 255, empty)
    cv2.createTrackbar("sat max", "TrackBars", 196, 255, empty)
    cv2.createTrackbar("val min", "TrackBars", 75, 255, empty)
    cv2.createTrackbar("val max", "TrackBars", 255, 255, empty)"""
    pass


def hsv_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


def countersdraw(mask):
    counters, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # counters = max(counters, key=lambda x: cv2.contourArea(x))
    # print(counters, hierarchy)
    return counters


def defects_points(counter):
    hull_defects = cv2.convexHull(counter, returnPoints=False)
    defects = cv2.convexityDefects(counter, hull_defects)
    return defects


def hull_points(counters):
    hull_list = []
    for i in range(len(counters)):
        hull = cv2.convexHull(counters[i])
        hull_list.append(hull)
    return hull_list


#cam = cv2.VideoCapture(0)  # reading video
# trackbars() # track bars for color detection
def run(cam):
    while True:
        success, frame = cam.read()
        frame = cv2.flip(frame, 1) # flip the video
        subframe = frame[0:255, 0:255] # slicing the frame
        # cv2.rectangle(subframe, (0, 0), (250, 250), (0,255,0),2) # DRAW
        # subframe = cv2.blur(subframe, (3, 3))
        hsvframe = hsv_frame(subframe)

        # values of track bar
        h_min = 0  # cv2.getTrackbarPos("Hue min", "TrackBars")
        h_max = 35  # cv2.getTrackbarPos("Hue max", "TrackBars")
        s_min = 1  # cv2.getTrackbarPos("sat min", "TrackBars")
        s_max = 196  # cv2.getTrackbarPos("sat max", "TrackBars")
        v_min = 75  # cv2.getTrackbarPos("val min", "TrackBars")
        v_max = 255  # cv2.getTrackbarPos("val max", "TrackBars")

        # print(h_min, h_max, s_min, s_max, v_min, v_max)

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(hsvframe, lower, upper)
        imgresult = cv2.bitwise_and(subframe, subframe, mask=mask)

        counter = countersdraw(mask)
        hull = hull_points(counter)

        # hull = cv2.convexHull(counter)
        # print(hull)
        cv2.drawContours(frame, counter, -1, (0, 0, 255), 3)
        cv2.drawContours(frame, hull, -1, (0, 255, 255), 2)

        """defects = defects_points(counter)
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(counter[s][0])
            end = tuple(counter[e][0])
            far = tuple(counter[f][0])
            cv2.line(frame, start, end, [0, 255, 0], 2)
            cv2.circle(frame, far, 5, [0, 0, 255], -1)"""

        cv2.imshow("video", frame)
        # cv2.imshow("sf",subframe)
        # cv2.imshow("hsv",hsvframe)
        # cv2.imshow("mask",mask)
        # cv2.imshow("result",imgresult)
        key = cv2.waitKey(1)
        if key == 81 or key == 113:
            break
