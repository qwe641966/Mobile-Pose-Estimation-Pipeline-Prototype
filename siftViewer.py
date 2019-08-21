import cv2
import sys
import os

sift = cv2.xfeatures2d.SIFT_create()
query_image = cv2.imread(sys.argv[1])
query_image = cv2.cvtColor(query_image,cv2.COLOR_BGR2GRAY)
kp, descriptors = sift.detectAndCompute(query_image,None)

img = cv2.drawKeypoints(query_image, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imwrite(sys.argv[1]+"_sift_viewer.png",img)

