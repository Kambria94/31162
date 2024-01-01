import cv2
import mediapipe as mp
import numpy as np
import time
import datetime
import sys

from myutils import calculate_angle
from action_kick import Kick

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
presentDate = datetime.datetime.now()


#variable to check if it is the first time through the while loop. Once the first round is over, this variable 
#sets to false
dataCaptured = False
examine_checks = False
fighting_stance = False
kick_time = 0
kickObject = Kick()

#Video feed
width = 2240
height = 1400

img = cv2.VideoCapture(0)
cv2.namedWindow("Mediapipe feed", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("Mediapipe feed", width, height)


#setup mediapipe pose instance minimum confidence as 50% with shortened name of "pose"
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
   with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    
    #current time - used so data prints every 5 seconds
    start_time = datetime.datetime.timestamp(presentDate)
    #while the image is open
    while img.isOpened:
        print("examine_checks is ", examine_checks, " fighting stance is ", fighting_stance, " dataCaptured is ", dataCaptured)
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
            lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            rheel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
            lheel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
            lhip_angle = calculate_angle(lshoulder, lhip, lknee)
            #angle of left knee
            lknee_angle = calculate_angle(lhip, lknee, lankle)
            #angle of right knee
            rknee_angle = calculate_angle(rhip, rknee, rankle)
            #angle of right hip
            rhip_angle = calculate_angle(rknee, rhip, rshoulder)
            # angle of left elbow
            lelbow_angle = calculate_angle(lwrist, lelbow, lshoulder)

            #distance from right hip to right knee
            dist_top_leg = np.sqrt((rhip[0]-rknee[0])**2 + (rhip[1]-rknee[1])**2)
            #distance from right knee to right angle
            dist_bottom_leg = np.sqrt((rknee[0]-rankle[0])**2 + (rknee[1]-rankle[1])**2)
            dist_leg = dist_top_leg + dist_bottom_leg
            dist_heel = np.sqrt((lankle[0]-rankle[0])**2 + (lankle[1]-rankle[1])**2)
            dist_ratio = dist_heel/dist_leg

            print("Debugging lknee:", lknee_angle, " rknee:", rknee_angle, " rhip:", rhip_angle, " lelbow_angle: ", lelbow_angle, " distance ratio: ", dist_ratio)
            # checking for the fighting stance position
            if lknee_angle >= 130 and rknee_angle >= 135 and rhip_angle >= 150 and lelbow_angle >= 27 and lelbow_angle <= 62 and dist_ratio > (1/2.6) and dist_ratio < (1/1.2):
                print(">>>>>>>>>>>>>>>>>> FIGHTING STANCE DETECTED <<<<<<<<<<<<<<<<<<<<")
                # We print out the instructions in the fighting stance position
                cv2.putText(image, "1. Turn left",
                        tuple(np.multiply([0,0.05], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA) 
                cv2.putText(image, "2. Get in fighting stance",
                        tuple(np.multiply([0,0.13], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA) 
                cv2.putText(image, "3. Lift Right knee and kick",
                        tuple(np.multiply([0,0.21], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, "4. Land in fighting stance",
                        tuple(np.multiply([0,0.25], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
                fighting_stance = True
                examine_checks = False
                kickObject.calibrate(landmarks)
                if dataCaptured == True:
                    image_capture = cv2.imread(kickObject.kick_file_name)
                    cv2.imshow(kickObject.kick_title, image_capture)
                
            else:
                if fighting_stance == True:
                    examine_checks = True
                    start_kick_time = datetime.datetime.timestamp(datetime.datetime.now())
                fighting_stance = False
                #sys.exit("done")
                    
            #defining landmarks (joints)
            if examine_checks == True:
                examine_checks = kickObject.capture_kick(
                   landmarks,
                   start_kick_time,
                   image,
                   examine_checks)
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


