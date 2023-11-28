import cv2
import mediapipe as mp
import numpy as np
import time
import datetime



mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
presentDate = datetime.datetime.now()

def calculate_angle(a,b,c):
   a = np.array(a) #first
   b = np.array(b) #middle
   c = np.array(c) #end


   radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
   angle = np.abs(radians*180/np.pi)


   if angle > 180:
       angle = 360 - angle


   return angle




angle = 90


#Video feed
img = cv2.VideoCapture(0)


#setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
   with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    print("Ready")
    for i in range(5):
        print(5-i)
        time.sleep(1)
        
    start_time = datetime.datetime.timestamp(presentDate)
    print(start_time)
    while img.isOpened:
        ret, frame = img.read()
        
        #Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        #Make detection
        poseresults = pose.process(image)
        handresults = hands.process(image)
        #Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)



        #Extract landmarks
        if datetime.datetime.timestamp(datetime.datetime.now()) >= start_time+10:
            #print("*************************8")
            
            try:
                landmarks = poseresults.pose_landmarks.landmark
                for index, arm in enumerate(handresults.multi_handedness):
                    wrist = [handresults.multi_hand_landmarks[index].landmark[0].x, handresults.multi_hand_landmarks[index].landmark[0].y]
                    thumbcmc = [handresults.multi_hand_landmarks[index].landmark[1].x, handresults.multi_hand_landmarks[index].landmark[1].y]
                    lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                rheel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
                lheel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
                
                # calculating distances and angles
                lbleg = np.sqrt((lankle[0] - lknee[0])**2 + (lankle[1] - lknee[1])**2)
                ltleg = np.sqrt((lknee[0] - lhip[0])**2 + (lknee[1] - lhip[1])**2)
                lleg = (lbleg + ltleg)
                print(lleg)
                #lleg = np.sqrt((lankle[0] - lhip[0])**2 + (lankle[1] - lhip[1])**2)
                heel_distance = np.sqrt((rheel[0] - lheel[0])**2 + (rheel[1] - lheel[1])**2)
                posture_lhip = calculate_angle(lshoulder, lhip, lknee)
                posture_lknee = calculate_angle(lhip, lknee, lankle)
                posture_rknee = calculate_angle(rhip, rknee, rankle)
                posture_relbow = calculate_angle(rshoulder, relbow, rwrist)
                posture_rshoulder = calculate_angle(rhip, rshoulder, relbow)
                
                # Left leg distance, left hip angle, left knee angle
                # Right knee angle, right elbow angle, right shoulder angle
                # All measurements need to be valid for the whole move to be right
                distgood = False
                lhipgood = False
                lkneegood = False
                rkneegood = False
                relbowgood = False
                rshouldergood = False
                #main action
                #heel distance feedbaack
                if heel_distance >= lleg/2.45 and heel_distance <= lleg/1.6:
                    distgood = True
                else:
                    #print(heel distance)
                    pass
                if heel_distance > lleg/1.6:
                    print("Pull feet closer together")
                else:
                    pass
                if heel_distance < lleg/2.45:
                    print("Put feet further apart")
                else:
                    pass
                #left hip feedback
                if posture_lhip <= 160 and posture_lhip >= 147:
                    lhipgood = True
                else:
                    pass
                if posture_lhip > 160:
                    print("Bend back less")
                else:
                    pass
                if posture_lhip < 147:
                    print("Bend back more")
                else:
                    pass
                # left knee feedback
                if posture_lknee <= 162 and posture_lknee >= 148:
                    lkneegood = True
                else:
                    pass
                if posture_lknee > 162:
                    print("Bend left knee more")
                else:
                    pass
                if posture_lknee < 148:
                    print("Don't bend left knee as much")
                else:
                    pass
                #Right Knee feedback
                if posture_rknee >= 161 and posture_rknee <= 172:
                    rkneegood = True
                else:
                    pass
                if posture_rknee < 161:
                    print ("Don't bend right knee as much")
                else:
                    pass
                if posture_rknee > 172:
                    print("Bend right knee more")
                else:
                    pass
                # Right elbow feedback
                if posture_relbow >= 165 and posture_relbow <= 195:
                    relbowgood = True
                else:
                    print("Make sure right arm is straight")
                    pass
                # Right shoulder feedback
                if posture_rshoulder > 75 and posture_rshoulder < 105:
                    rshouldergood = True
                else:
                    print("Make sure you punch straight ahead")
                    pass
                #If all parts of the move are correct:
                """ if (distgood and lhipgood and lkneegood and rkneegood):
                    print("Good stance")
                else:
                    print("Fix stance")
                    pass
                if (relbowgood and rshouldergood):
                    print("Good punch")
                else:
                    print("Fix the punch")
                    pass"""
                #lbleg = np.sqrt((lankle[0] - lknee[0])**2 + (lankle[1] - lknee[1])**2)
                #ltleg = np.sqrt((lknee[0] - lhip[0])**2 + (lknee[1] - lhip[1])**2)
                #lleg = (lbleg + ltleg)
            except:
                #print("Ignoring unexpected exception")
                pass


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



