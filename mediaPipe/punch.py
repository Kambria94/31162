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
#import playsound
#import winsound
import pygame
from pygame.locals import *




mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
presentDate = datetime.datetime.now()
pygame.init()

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
dataCaptured = False
chamber = False
punch_time = 0
first_punch_hold = True
punching = False


#Video feed
width = 2240
height = 1400

img = cv2.VideoCapture(0)

cv2.namedWindow("Mediapipe feed", cv2.WINDOW_NORMAL) 

cv2.resizeWindow("Mediapipe feed", width, height)

start_punch_hold_time = datetime.datetime.timestamp(datetime.datetime.now()) + 1000000
punch_img = cv2.imread('images/right_arm_reverse_punch.png')
backToChamber = pygame.mixer.Sound("audio/Back to Chamber.mp3")
feetCloser = pygame.mixer.Sound("audio/Feet closer.mp3")
feetFurther = pygame.mixer.Sound("audio/Feet Further.mp3")
getInChamber = pygame.mixer.Sound("audio/Get in Chamber start.mp3")
greatJob = pygame.mixer.Sound("audio/Great Job.mp3")
hold = pygame.mixer.Sound("audio/Hold.mp3")
leftKneeLess = pygame.mixer.Sound("audio/Left Knee Less.mp3")
leftKneeMore = pygame.mixer.Sound("audio/Left Knee More.mp3")
punchStraight = pygame.mixer.Sound("audio/Punch Straight ahead.mp3")
reversePunch = pygame.mixer.Sound("audio/Right hand reverse punch.mp3")
rightKneeLess = pygame.mixer.Sound("audio/Right knee Less.mp3")
rightKneeMore = pygame.mixer.Sound("audio/Right Knee More.mp3")
straightenElbow = pygame.mixer.Sound("audio/Straighten Right elbow.mp3")
tryAgain = pygame.mixer.Sound("audio/Try Again.mp3")

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
    getInChamber.play()
    while img.isOpened:
        print("chamber is ", chamber, " dataCaptured is ", dataCaptured)
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

        #Providing instructions S1
        image[150:250,30:131,:] = punch_img[0:100,0:101,:]
        if punching == False:
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
            cv2.putText(image, "4. Go back to chamber position",
                        tuple(np.multiply([0,0.29], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA
                    )
            if dataCaptured == True:
                punch_capture = cv2.imread('images/punch_capture.jpg')
                image[0:480,0:640,:] = punch_capture[0:480,0:640,:]
       
        #Extract landmarks
        #enters this if statement every 10 seconds - if the current time is or is past the starting time + 10 
        #seconds. So only enters if it is 10 seconds past the start time

            
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

            #checking for chamber S2
            if lknee_angle >= 145 and rknee_angle >= 145 and rhip_angle >= 160 and drwist_rhip <= (np.sqrt((rshoulder[0] - rwrist[0])**2 + (rshoulder[1] - rwrist[1])**2))/4:
                punching = False
                chamber = True
                #calibration
                lenarm = np.sqrt((rshoulder[0] - rwrist[0])**2 + (rshoulder[1] - rwrist[1])**2)
                #length of bottom of left leg (knee to ankle)
                lbleg = np.sqrt((lankle[0] - lknee[0])**2 + (lankle[1] - lknee[1])**2)
                #length of top of left leg (knee to hip)
                ltleg = np.sqrt((lknee[0] - lhip[0])**2 + (lknee[1] - lhip[1])**2)
                #total length of leg (bottom+top) - used for ratio for distance between legs during step
                lenleg = (lbleg + ltleg)
                
                
            else:
                if chamber == True:
                    start_punch_time = datetime.datetime.timestamp(datetime.datetime.now())
                    first_punch_hold = True
                    dataCaptured = False
                chamber = False
                #sys.exit("done")
                    
            #defining landmarks (joints)
                
            # calculating distances and angles
            #the length of the right arm (punching arm) as it appears in the x-axis. If arm it tilted up or
            #to the side, the x-length of the arm will appear less.
            xlenarm = np.abs(rshoulder[0] - rwrist[0])
            #distance between left heel and right heel, used to detect how far step is
            heel_distance = np.sqrt((rheel[0] - lheel[0])**2 + (rheel[1] - lheel[1])**2)
            #angle of left side of hip
            lhip_angle = calculate_angle(lshoulder, lhip, lknee)
            #angle of left knee
            lknee_angle = calculate_angle(lhip, lknee, lankle)
            #angle of right knee
            rknee_angle = calculate_angle(rhip, rknee, rankle)
            #angle of right elbow (punching arm)
            relbow_angle = calculate_angle(rshoulder, relbow, rwrist)
            #angle of right shoulder (punching arm)
            rshoulder_angle = calculate_angle(rhip, rshoulder, relbow)
            
            
            #checking for punch S3
            if rshoulder_angle >= 40 and rshoulder_angle <= 140 and rwrist[0] > lankle[0] and rwrist[0] > rankle[0] and relbow[0] > rshoulder[0] and relbow_angle >= 90 and chamber == False and dataCaptured == False:
                punching = True
                #pose evaluation S4
                # Left leg distance, left hip angle, left knee angle
                # Right knee angle, right elbow angle, right shoulder angle
                # All measurements need to be valid for the whole move to be right
                distgood = False
                feetcloser = False
                feetfarther = False
                lhipgood = False
                leanforward = False
                leanback = False
                lkneegood = False
                bendlkneemore = False
                bendlkneeless = False
                rkneegood = False
                bendrkneemore = False
                bendrkneeless = False
                relbowgood = False
                xlenarmgood = False
                allGood = False 
                #2 examine heel distance
                #measures distance between right heel and left 
                #ratio of length of leg:distance between heels should be 1.6-2.45 
                #(numbers obtained by multiple tests)
                if heel_distance >= lenleg/2.2 and heel_distance <= lenleg/1.1:
                    distgood = True
                else:
                    #print(heel distance)
                    pass
                if heel_distance > lenleg/1.1:
                    feetcloser = True
                else:
                    pass
                if heel_distance < lenleg/2.2:
                    feetfarther = True
                else:
                    pass
                #5 examine hip position
                #Angle of left side of hip should be between 147 and 160 degrees (mostly straight)
                if lhip_angle <= 160 and lhip_angle >= 147:
                    lhipgood = True
                else:
                    pass
                if lhip_angle > 160:
                    leanforward = True
                else:
                    pass
                if lhip_angle < 147:
                    leanback = True
                else:
                    pass
                #3 examine left leg position
                #left knee should be between 148 and 162 degrees bent
                if lknee_angle <= 162 and lknee_angle >= 148:
                    lkneegood = True
                else:
                    pass
                if lknee_angle > 162:
                    bendlkneemore = True
                else:
                    pass
                if lknee_angle < 148:
                    bendlkneeless = True
                else:
                    pass
                #4 examine right leg position
                #right knee should be mostly straight: between 161 and 172 degrees
                if rknee_angle >= 161 and rknee_angle <= 172:
                    rkneegood = True
                else:
                    pass
                if rknee_angle < 161:
                    bendrkneeless = True
                else:
                    pass
                if rknee_angle > 172:
                    bendrkneemore = True
                else:
                    pass
                #6 examine Right elbow angle
                #Right arm (punching) should be straight at elbow - between 165 and 180 degrees
                if relbow_angle >= 165 and relbow_angle <= 180:
                    relbowgood = True
                else:
                    
                    pass
                
                if distgood == True and lkneegood == True and rkneegood == True and lhipgood == True and xlenarmgood == True and relbowgood == True:
                    allGood = True

                #7 examine position of right arm
                #the x-axis length of the arm should be same as real length of arm with margin of 0.02 units
                if xlenarm >= lenarm - 0.02:
                    xlenarmgood = True
                else:
                    pass
                if first_punch_hold == True:
                    punch_speed = datetime.datetime.timestamp(datetime.datetime.now())-start_punch_time
                    start_punch_hold_time = datetime.datetime.timestamp(datetime.datetime.now())

                #if prevdistgood != distgood or prevlhipgood != lhipgood or prevlkneegood != lkneegood or prevrkneegood != rkneegood or prevrelbowgood != relbowgood or prevxlenarmgood != xlenarmgood:
                    #   start_punch_hold_time = datetime.datetime.timestamp(datetime.datetime.now())
                if datetime.datetime.timestamp(datetime.datetime.now()) >= start_punch_hold_time and datetime.datetime.timestamp(datetime.datetime.now()) < start_punch_hold_time+0.5:
                    #playsound('audio/low_beep.mp3')
                    cv2.putText(image, "Hold 3",
                        tuple(np.multiply([0,0.12], [640, 480]).astype(int)),
                        cv2.QT_FONT_NORMAL, 2, (255,255,255), 2, cv2.LINE_AA
                    )
                elif datetime.datetime.timestamp(datetime.datetime.now()) >= start_punch_hold_time+0.5 and datetime.datetime.timestamp(datetime.datetime.now()) < start_punch_hold_time+1:
                    #playsound('audio/low_beep.mp3')
                    cv2.putText(image, "Hold 2",
                        tuple(np.multiply([0,0.12], [640, 480]).astype(int)),
                        cv2.QT_FONT_NORMAL, 2, (255,255,255), 2, cv2.LINE_AA
                    ) 
                elif datetime.datetime.timestamp(datetime.datetime.now()) >= start_punch_hold_time+1 and datetime.datetime.timestamp(datetime.datetime.now()) < start_punch_hold_time+1.5:
                    #playsound('audio/low_beep.mp3')
                    cv2.putText(image, "Hold 1",
                        tuple(np.multiply([0,0.12], [640, 480]).astype(int)),
                        cv2.QT_FONT_NORMAL, 2, (255,255,255), 2, cv2.LINE_AA
                    ) 
                elif datetime.datetime.timestamp(datetime.datetime.now()) >= start_punch_hold_time+1.5:
                    backToChamber.play()
                    cv2.putText(image, "Feedback:",
                        tuple(np.multiply([0,0.05], [640, 480]).astype(int)),
                        cv2.QT_FONT_NORMAL, 1, (255,255,255), 2, cv2.LINE_AA
                    ) 
                    if feetcloser == True:
                        text_width, text_height = cv2.getTextSize(
                            "Pull feet closer together", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Pull feet closer together",
                            tuple(np.multiply([lankle[0]-text_width/1280, lankle[1]+0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    if feetfarther == True:
                        text_width, text_height = cv2.getTextSize(
                            "Put feet farther apart", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Put feet farther apart",
                            tuple(np.multiply([lankle[0]-text_width/1280, lankle[1]+0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    if distgood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Feet distance is good", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Feet distance is good",
                            tuple(np.multiply([lankle[0]-text_width/1280, lankle[1]+0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA
                        )
                    if leanforward == True:
                        text_width, text_height = cv2.getTextSize(
                            "Lean forward more", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Lean forward more",
                            tuple(np.multiply([rhip[0]-text_width/1280, rhip[1]-0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    if leanback == True:
                        text_width, text_height = cv2.getTextSize(
                            "Lean back more", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Lean back more",
                            tuple(np.multiply([rhip[0]-text_width/1280, rhip[1]-0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    if lhipgood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Back angle is good", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Back angle is good",
                            tuple(np.multiply([rhip[0]-text_width/1280, rhip[1]-0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA
                        )
                    if bendlkneemore == True:
                        text_width, text_height = cv2.getTextSize(
                            "Bend left knee more", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Bend left knee more",
                            tuple(np.multiply([lknee[0]-text_width/1280, lknee[1]-0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    if bendlkneeless == True:
                        text_width, text_height = cv2.getTextSize(
                            "Bend left knee less", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Bend left knee less",
                            tuple(np.multiply([lknee[0]-text_width/1280, lknee[1]-0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    if lkneegood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Left knee angle is good", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Left knee angle is good",
                            tuple(np.multiply([lknee[0]-text_width/1280, lknee[1]-0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA
                        )
                    if bendrkneemore == True:
                        text_width, text_height = cv2.getTextSize(
                            "Bend right knee more", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Bend right knee more",
                            tuple(np.multiply([rknee[0]-text_width/1280, rknee[1]+0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    if bendrkneeless == True:
                        text_width, text_height = cv2.getTextSize(
                            "Bend right knee less", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Bend right knee less",
                            tuple(np.multiply([rknee[0]-text_width/1280, rknee[1]+0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    if rkneegood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Right knee angle is good", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Right knee angle is good",
                            tuple(np.multiply([rknee[0]-text_width/1280, rknee[1]+0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA
                        )
                    if relbowgood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Right elbow is straight", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Right elbow is straight",
                            tuple(np.multiply([relbow[0]-text_width/1280, relbow[1]-0.15], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA
                        )
                    if relbowgood == False:
                        text_width, text_height = cv2.getTextSize(
                            "Make sure right elbow is straight", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Make sure right elbow is straight",
                            tuple(np.multiply([relbow[0]-text_width/1280, relbow[1]-0.15], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    if xlenarmgood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Punching straight ahead", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Punching straight ahead",
                            tuple(np.multiply([rshoulder[0]-text_width/1280, rshoulder[1]+0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA
                        )
                    if xlenarmgood == False:
                        text_width, text_height = cv2.getTextSize(
                            "Make sure you punch straight ahead", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, "Make sure you punch straight ahead",
                            tuple(np.multiply([rshoulder[0]-text_width/1280, rshoulder[1]+0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    if punch_speed <= 0.4:
                        text_width, text_height = cv2.getTextSize(
                            "Punch is fast", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, str(int(round(punch_speed*1000, 0)))+" milliseconds",
                            tuple(np.multiply([text_width/640, 0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA
                        )
                    if punch_speed > 0.3:
                        text_width, text_height = cv2.getTextSize(
                            "Punch faster", cv2.QT_FONT_NORMAL, 1, 2
                            )[0]
                        cv2.putText(image, str(int(round(punch_speed*1000, 0)))+" milliseconds",
                            tuple(np.multiply([text_width/640, 0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA
                        )
                    #capture_image = cv2.resize(image, (320, 240))
                    cv2.imwrite('images/punch_capture.jpg', image)
                    dataCaptured = True
                first_punch_hold = False

            else:
                if dataCaptured == False:
                    punching = False
                         



                """
                if (relbowgood and rshouldergood):
                    print("Good punch")
                else:
                    print("Fix the punch")
                    pass"""
                #lbleg = np.sqrt((lankle[0] - lknee[0])**2 + (lankle[1] - lknee[1])**2)
                #ltleg = np.sqrt((lknee[0] - lhip[0])**2 + (lknee[1] - lhip[1])**2)
                #lenleg = (lbleg + ltleg)
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



