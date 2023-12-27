import cv2
import mediapipe as mp
import numpy as np
import time
import datetime
import sys

from myutils import calculate_angle


class Punch:
    def __init__(self):
        self.file_name = 'punch_capture.jpg'
        self.image_title = 'Punch Capture'
        self.lenarm = 0
        self.lleg = 0
        self.punch_speed = 0
        self.start_punch_hold_time = 0

    def calibrate(self, landmarks):
        mp_pose = mp.solutions.pose

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

        self.lenarm = np.sqrt((rshoulder[0] - rwrist[0])**2 + (rshoulder[1] - rwrist[1])**2)
        #length of bottom of left leg (knee to ankle)
        lbleg = np.sqrt((lankle[0] - lknee[0])**2 + (lankle[1] - lknee[1])**2)
        #length of top of left leg (knee to hip)
        ltleg = np.sqrt((lknee[0] - lhip[0])**2 + (lknee[1] - lhip[1])**2)
        #total length of leg (bottom+top) - used for ratio for distance between legs during step
        self.lleg = (lbleg + ltleg)
        print("************** CALIBRATION SUCCESSFUL ****************")

    def capture_punch(self,
        landmarks,
        start_punch_time,              
        image,
        examine_checks,
        first_punch_hold):

        return_examine_checks = True
        return_first_punch_hold = False

        mp_pose = mp.solutions.pose

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

        #2 examine heel distance
        #measures distance between right heel and left 
        #ratio of length of leg:distance between heels should be 1.6-2.45 
        #(numbers obtained by multiple tests)
        if heel_distance >= self.lleg/2.2 and heel_distance <= self.lleg/1.1:
            distgood = True
        else:
            #print(heel distance)
            pass
        if heel_distance > self.lleg/1.1:
            feetcloser = True
        else:
            pass
        if heel_distance < self.lleg/2.2:
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
    
        #7 examine position of right arm
        #the x-axis length of the arm should be same as real length of arm with margin of 0.02 units
        if xlenarm >= self.lenarm - 0.02:
            xlenarmgood = True
        else:
            pass
        if rshoulder_angle >= 40 and rshoulder_angle <= 140 and rwrist[0] > lankle[0] and rwrist[0] > rankle[0]:
                print("+++++++++++++++++++++++++++ PUNCH DETECTED +++++++++++++++++++++++++++")
                #Minimum requirements to even consider this a punch
                if first_punch_hold == True:
                    self.punch_speed = datetime.datetime.timestamp(datetime.datetime.now())-start_punch_time
                    self.start_punch_hold_time = datetime.datetime.timestamp(datetime.datetime.now())

                print(">>>>>>>>> Time diff = ", datetime.datetime.timestamp(datetime.datetime.now()) - self.start_punch_hold_time)
                if datetime.datetime.timestamp(datetime.datetime.now()) >= self.start_punch_hold_time and datetime.datetime.timestamp(datetime.datetime.now()) < self.start_punch_hold_time+1:
                    cv2.putText(image, "3",
                        tuple(np.multiply([0,0.12], [640, 480]).astype(int)),
                        cv2.QT_FONT_NORMAL, 2, (255,255,255), 2, cv2.LINE_AA)
                    print(">>>>>>>>> 3")
                elif datetime.datetime.timestamp(datetime.datetime.now()) >= self.start_punch_hold_time+1 and datetime.datetime.timestamp(datetime.datetime.now()) < self.start_punch_hold_time+2:
                    cv2.putText(image, "2",
                        tuple(np.multiply([0,0.12], [640, 480]).astype(int)),
                        cv2.QT_FONT_NORMAL, 2, (255,255,255), 2, cv2.LINE_AA) 
                    print(">>>>>>>>> 2")
                elif datetime.datetime.timestamp(datetime.datetime.now()) >= self.start_punch_hold_time+2 and datetime.datetime.timestamp(datetime.datetime.now()) < self.start_punch_hold_time+3:
                    cv2.putText(image, "1",
                        tuple(np.multiply([0,0.12], [640, 480]).astype(int)),
                        cv2.QT_FONT_NORMAL, 2, (255,255,255), 2, cv2.LINE_AA)
                    print(">>>>>>>>> 1")
                elif datetime.datetime.timestamp(datetime.datetime.now()) >= self.start_punch_hold_time+3:
                    print(">>>>>>>>> CAPTURING")
                    cv2.putText(image, "Captured!",
                        tuple(np.multiply([0,0.05], [640, 480]).astype(int)),
                        cv2.QT_FONT_NORMAL, 1, (255,255,255), 2, cv2.LINE_AA) 
                    if feetcloser == True:
                        text_width, text_height = cv2.getTextSize(
                            "Pull feet closer together", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Pull feet closer together",
                                tuple(np.multiply([lankle[0]-text_width/1280, lankle[1]+0.05], [640, 480]).astype(int)),
                                cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    if feetfarther == True:
                        text_width, text_height = cv2.getTextSize(
                            "Put feet farther apart", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Put feet farther apart",
                                        tuple(np.multiply([lankle[0]-text_width/1280, lankle[1]+0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    if distgood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Feet distance is good", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Feet distance is good",
                                    tuple(np.multiply([lankle[0]-text_width/1280, lankle[1]+0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA)
                    if leanforward == True:
                        text_width, text_height = cv2.getTextSize(
                            "Lean forward more", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Lean forward more",
                                    tuple(np.multiply([rhip[0]-text_width/1280, rhip[1]-0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    if leanback == True:
                        text_width, text_height = cv2.getTextSize(
                            "Lean back more", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Lean back more",
                                    tuple(np.multiply([rhip[0]-text_width/1280, rhip[1]-0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    if lhipgood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Back angle is good", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Back angle is good",
                                    tuple(np.multiply([rhip[0]-text_width/1280, rhip[1]-0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA)
                    if bendlkneemore == True:
                        text_width, text_height = cv2.getTextSize(
                            "Bend left knee more", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Bend left knee more",
                                    tuple(np.multiply([lknee[0]-text_width/1280, lknee[1]-0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    if bendlkneeless == True:
                        text_width, text_height = cv2.getTextSize(
                            "Bend left knee less", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Bend left knee less",
                                    tuple(np.multiply([lknee[0]-text_width/1280, lknee[1]-0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    if lkneegood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Left knee angle is good", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Left knee angle is good",
                                    tuple(np.multiply([lknee[0]-text_width/1280, lknee[1]-0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA)
                    if bendrkneemore == True:
                        text_width, text_height = cv2.getTextSize(
                            "Bend right knee more", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Bend right knee more",
                                    tuple(np.multiply([rknee[0]-text_width/1280, rknee[1]+0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    if bendrkneeless == True:
                        text_width, text_height = cv2.getTextSize(
                            "Bend right knee less", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Bend right knee less",
                                    tuple(np.multiply([rknee[0]-text_width/1280, rknee[1]+0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    if rkneegood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Right knee angle is good", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Right knee angle is good",
                                    tuple(np.multiply([rknee[0]-text_width/1280, rknee[1]+0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA)
                    if relbowgood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Right elbow is straight", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Right elbow is straight",
                                    tuple(np.multiply([relbow[0]-text_width/1280, relbow[1]-0.15], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA)
                    if relbowgood == False:
                        text_width, text_height = cv2.getTextSize(
                            "Make sure right elbow is straight", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Make sure right elbow is straight",
                                    tuple(np.multiply([relbow[0]-text_width/1280, relbow[1]-0.15], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    if xlenarmgood == True:
                        text_width, text_height = cv2.getTextSize(
                            "Punching straight ahead", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Punching straight ahead",
                                    tuple(np.multiply([rshoulder[0]-text_width/1280, rshoulder[1]+0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA)
                    if xlenarmgood == False:
                        text_width, text_height = cv2.getTextSize(
                            "Make sure you punch straight ahead", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Make sure you punch straight ahead",
                                    tuple(np.multiply([rshoulder[0]-text_width/1280, rshoulder[1]+0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    if self.punch_speed <= 0.3:
                        text_width, text_height = cv2.getTextSize(
                            "Punch is fast", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Punch is Fast",
                                    tuple(np.multiply([text_width/640, 0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,255,0), 2, cv2.LINE_AA)
                    if self.punch_speed > 0.3:
                        text_width, text_height = cv2.getTextSize(
                            "Punch faster", cv2.QT_FONT_NORMAL, 1, 2)[0]
                        cv2.putText(image, "Punch Faster",
                                    tuple(np.multiply([text_width/640, 0.05], [640, 480]).astype(int)),
                                    cv2.QT_FONT_NORMAL, 1, (0,0,255), 2, cv2.LINE_AA)
                    print("%%%%%%%%%%%%%%%%% WRITING IMAGE %%%%%%%%%%%%%%%%")
                    cv2.imwrite(self.file_name, image)
                    return_examine_checks = False
                return_first_punch_hold = False

        else:
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
            return_examine_checks = examine_checks
            return_first_punch_hold = first_punch_hold
        
        return (return_examine_checks, return_first_punch_hold)
