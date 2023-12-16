#right hand reverse punch
#punch with right hand, step with left leg
#forward stance
#Put instructions before user does punch
#Punch with right hand
#step with left foot
import cv2
import mediapipe as mp
import numpy as np
import time
import datetime



mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
presentDate = datetime.datetime.now()

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




#variable to check if it is the first time through the while loop. Once the first round is over, this variable 
#sets to false
firstRound = True


#Video feed
img = cv2.VideoCapture(0)


#setup mediapipe pose instance minimum confidence as 50% with shortened name of "pose"
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
   with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    #10 second countdown so user can get ready before punch
    print("Ready")
    for i in range(10):
        print(10-i)
        time.sleep(1)
    
    #current time - used so data prints every 5 seconds
    start_time = datetime.datetime.timestamp(presentDate)
    #while the image is open
    while img.isOpened:
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



        #Extract landmarks
        #enters this if statement every 10 seconds - if the current time is or is past the starting time + 10 
        #seconds. So only enters if it is 10 seconds past the start time
        if datetime.datetime.timestamp(datetime.datetime.now()) >= start_time+10:
            print("********************************************")
            
            try:
                #defining landmarks (joints)
                landmarks = poseresults.pose_landmarks.landmark




                """if handresults.multi_hand_landmarks:
                    for index, arm in enumerate(handresults.multi_handedness):
                        mp_drawing.draw_landmarks(image, arm, mp_hands.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(221, 122, 76), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                            )
                    wrist = [handresults.multi_hand_landmarks[index].landmark[0].x, handresults.multi_hand_landmarks[index].landmark[0].y]
                    thumbmcp = [handresults.multi_hand_landmarks[index].landmark[2].x, handresults.multi_hand_landmarks[index].landmark[2].y]
                    thumbip = [handresults.multi_hand_landmarks[index].landmark[3].x, handresults.multi_hand_landmarks[index].landmark[3].y]
                    thumbtip = [handresults.multi_hand_landmarks[index].landmark[4].x, handresults.multi_hand_landmarks[index].landmark[4].y]
                    indexmcp = [handresults.multi_hand_landmarks[index].landmark[5].x, handresults.multi_hand_landmarks[index].landmark[5].y]
                    indexpip = [handresults.multi_hand_landmarks[index].landmark[6].x, handresults.multi_hand_landmarks[index].landmark[6].y]
                    indexdip = [handresults.multi_hand_landmarks[index].landmark[7].x, handresults.multi_hand_landmarks[index].landmark[7].y]
                    indextip = [handresults.multi_hand_landmarks[index].landmark[8].x, handresults.multi_hand_landmarks[index].landmark[8].y]
                    indextip = [handresults.multi_hand_landmarks[index].landmark[8].x, handresults.multi_hand_landmarks[index].landmark[8].y]
                    middlemcp = [handresults.multi_hand_landmarks[index].landmark[9].x, handresults.multi_hand_landmarks[index].landmark[9].y]
                    middlepip = [handresults.multi_hand_landmarks[index].landmark[10].x, handresults.multi_hand_landmarks[index].landmark[10].y]
                    middledip = [handresults.multi_hand_landmarks[index].landmark[11].x, handresults.multi_hand_landmarks[index].landmark[11].y]
                    middletip = [handresults.multi_hand_landmarks[index].landmark[12].x, handresults.multi_hand_landmarks[index].landmark[12].y]
                    ringmcp = [handresults.multi_hand_landmarks[index].landmark[13].x, handresults.multi_hand_landmarks[index].landmark[13].y]
                    ringpip = [handresults.multi_hand_landmarks[index].landmark[14].x, handresults.multi_hand_landmarks[index].landmark[14].y]
                    ringdip = [handresults.multi_hand_landmarks[index].landmark[15].x, handresults.multi_hand_landmarks[index].landmark[15].y]
                    ringtip = [handresults.multi_hand_landmarks[index].landmark[16].x, handresults.multi_hand_landmarks[index].landmark[16].y]
                    pinkymcp = [handresults.multi_hand_landmarks[index].landmark[17].x, handresults.multi_hand_landmarks[index].landmark[17].y]
                    pinkypip = [handresults.multi_hand_landmarks[index].landmark[18].x, handresults.multi_hand_landmarks[index].landmark[18].y]
                    pinkydip = [handresults.multi_hand_landmarks[index].landmark[19].x, handresults.multi_hand_landmarks[index].landmark[19].y]
                    pinkytip = [handresults.multi_hand_landmarks[index].landmark[20].x, handresults.multi_hand_landmarks[index].landmark[20].y]
                    print(calculate_angle(indexmcp, indexpip, indexdip))"""
                


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
                #if it is the first loop of the while loop
                if firstRound == True:
                    #getting length of arm for calibration purposes
                    lenarm = np.sqrt((rshoulder[0] - rwrist[0])**2 + (rshoulder[1] - rwrist[1])**2)
                    #it is no longer first loop
                    firstRound = False

                # calculating distances and angles
                #length of bottom of left leg (knee to ankle)
                lbleg = np.sqrt((lankle[0] - lknee[0])**2 + (lankle[1] - lknee[1])**2)
                #length of top of left leg (knee to hip)
                ltleg = np.sqrt((lknee[0] - lhip[0])**2 + (lknee[1] - lhip[1])**2)
                #total length of leg (bottom+top) - used for ratio for distance between legs during step
                lleg = (lbleg + ltleg)
                #the length of the right arm (punching arm) as it appears in the x-axis. If arm it tilted up or
                #to the side, the x-length of the arm will appear less.
                xlenarm = np.abs(rshoulder[0] - rwrist[0])
                #distance between left heel and right heel, used to detect how far step is
                heel_distance = np.sqrt((rheel[0] - lheel[0])**2 + (rheel[1] - lheel[1])**2)
                #angle of left side of hip
                posture_lhip = calculate_angle(lshoulder, lhip, lknee)
                #angle of left knee
                posture_lknee = calculate_angle(lhip, lknee, lankle)
                #angle of right knee
                posture_rknee = calculate_angle(rhip, rknee, rankle)
                #angle of right elbow (punching arm)
                posture_relbow = calculate_angle(rshoulder, relbow, rwrist)
                #angle of right shoulder (punching arm)
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
                xlenarmgood = False
                #measures distance between right heel and left 
                #ratio of length of leg:distance between heels should be 1.6-2.45 
                #(numbers obtained by multiple tests)
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
                #Angle of left side of hip should be between 147 and 160 degrees (mostly straight)
                if posture_lhip <= 160 and posture_lhip >= 147:
                    lhipgood = True
                else:
                    pass
                if posture_lhip > 160:
                    print("Lean forward more")
                else:
                    pass
                if posture_lhip < 147:
                    print("Lean back more")
                else:
                    pass
                # left knee feedback
                #left knee should be between 148 and 162 degrees bent
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
                #right knee should be mostly straight: between 161 and 172 degrees
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
                #Right arm (punching) should be straight at elbow - between 165 and 180 degrees
                if posture_relbow >= 165 and posture_relbow <= 180:
                    relbowgood = True
                else:
                    print("Make sure right arm is straight")
                    pass
                # Right shoulder feedback
                
                #the x-axis length of the arm should be same as real length of arm with margin of 0.02 units
                if xlenarm >= lenarm - 0.02:
                    xlenarmgood = True
                    pass
                else:
                    print("Make sure you punch striaght ahead")


                #If all parts of the move are correct:
                if (distgood == True and lhipgood == True and lkneegood == True and rkneegood == True and relbowgood == True and xlenarmgood == True):
                    print("Great punch!")
                else:
                    pass
                """
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



