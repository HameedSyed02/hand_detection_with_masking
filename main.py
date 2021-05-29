import handrecognitation
import cv2

cam = cv2.VideoCapture(0)
handrecognitation.run(cam)