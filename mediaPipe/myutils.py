import cv2
import mediapipe as mp
import numpy as np
import time
import datetime
import sys

#function to calculate angle between three points
def calculate_angle(a,b,c):
   a = np.array(a) #first point coordinates
   b = np.array(b) #middle point coordinates
   c = np.array(c) #end point coordinates

   #calculate radians using arctan and coverting it to degrees
   radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
   angle = np.abs(radians*180/np.pi)

    #if the angle is greater than 180, use the angle on the other side, or 360-angle
   # for example if angle is 200 degrees, it makes it 160.
   if angle > 180:
       angle = 360 - angle


   return angle

