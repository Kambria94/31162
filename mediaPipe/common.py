import cv2
import mediapipe as mp
import numpy as np
import time
import datetime
import sys

from myutils import calculate_angle
from action_punch import Punch

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
presentDate = datetime.datetime.now()


#variable to check if it is the first time through the while loop. Once the first round is over, this variable 
#sets to false
dataCaptured = False
examine_checks = False
chamber = False
punch_time = 0
first_punch_hold = True
punchObject = Punch()

#Video feed
width = 2240
height = 1400

img = cv2.VideoCapture(0)
cv2.namedWindow("Mediapipe feed", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("Mediapipe feed", width, height)

start_punch_hold_time = datetime.datetime.timestamp(datetime.datetime.now()) + 1000000


#setup mediapipe pose instance minimum confidence as 50% with shortened name of "pose"
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
   with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    #10 second countdown so user can get ready before punch
    """print("Ready")
    for i in range(10):
        print(10-i)
        time.sleep(1)"""
    
    #current time - used so data prints every 5 seconds
    start_time = datetime.datetime.timestamp(presentDate)
    #while the image is open
    while img.isOpened:
        print("examine_checks is ", examine_checks, " chamber is ", chamber, " dataCaptured is ", dataCaptured)
        #reading image
        ret, frame = img.read()
        
        #Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        #Make detection for pose and hand
        poseresults = pose.process(image)
        handresults = hands.process(image)
        #Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        #image = cv2.flip(image, 1)

        #Extract landmarks
        try:
            landmarks = poseresults.pose_landmarks.landmark
            #defining different landmarks that we need to use and extracting coordinates
            lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            rheel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
            lheel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
            real_rhip = [rhip[0]+(rshoulder[0]-rhip[0])/3, rhip[1]+(rshoulder[1]-rhip[1])/3]
            lhip_angle = calculate_angle(lshoulder, lhip, lknee)
            #angle of left knee
            lknee_angle = calculate_angle(lhip, lknee, lankle)
            #angle of right knee
            rknee_angle = calculate_angle(rhip, rknee, rankle)
            #angle of right hip
            rhip_angle = calculate_angle(rknee, rhip, rshoulder)
            #distance from right hip to right wrist
            drwist_rhip = np.sqrt((rwrist[0]-real_rhip[0])**2 + (rwrist[1]-real_rhip[1])**2)

            # print("Debugging lknee:", lknee_angle, " rknee:", rknee_angle, " rhip:", rhip_angle)
            # checking for the chamber position
            if lknee_angle >= 145 and rknee_angle >= 145 and rhip_angle >= 160 and drwist_rhip <= (np.sqrt((rshoulder[0] - rwrist[0])**2 + (rshoulder[1] - rwrist[1])**2))/4:
                # We print out the instructions in the chamber position
                cv2.putText(image, "1. Turn left",
                        tuple(np.multiply([0,0.05], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA
                        ) 
                cv2.putText(image, "2. Get in chamber postition",
                        tuple(np.multiply([0,0.13], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA
                        ) 
                cv2.putText(image, "3. Right arm punch, Left foot step",
                        tuple(np.multiply([0,0.21], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA
                    )
                chamber = True
                examine_checks = False
                punchObject.calibrate(landmarks)
                if dataCaptured == True:
                    image_capture = cv2.imread(punchObject.file_name)
                    cv2.imshow(punchObject.image_title, image_capture)
                
            else:
                if chamber == True:
                    examine_checks = True
                    start_punch_time = datetime.datetime.timestamp(datetime.datetime.now())
                    first_punch_hold = True
                chamber = False
                #sys.exit("done")
                    
            #defining landmarks (joints)
            if examine_checks == True:
                examine_checks, first_punch_hold = punchObject.capture_punch(
                   landmarks,
                   start_punch_time,
                   image,
                   examine_checks,
                   first_punch_hold)
               
                dataCaptured = True
        except Exception as e:
            print("Exception: ", e)
            pass

            #when loop runs through, reset start time to now (reset countdown)
            start_time = datetime.datetime.timestamp(datetime.datetime.now())



        #Render detections
        mp_drawing.draw_landmarks(image, poseresults.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                )


        cv2.imshow("Mediapipe feed", image)
        
        if cv2.waitKey(10) & 0xFF == ord("x"):
            break




img.release()
cv2.destroyAllWindows()


