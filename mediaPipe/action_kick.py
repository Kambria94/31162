import cv2
import mediapipe as mp
import numpy as np
import time
import datetime
import sys

from myutils import calculate_angle


class Kick:
    def __init__(self):
        self.knee_file_name = 'knee_capture.jpg'
        self.kick_file_name = 'kick_capture.jpg'
        self.knee_title = 'Kick Capture - Knee'
        self.kick_title = 'Kick Capture - Kick'
        self.knee_completed = False
        self.lenarm = 0
        self.lleg = 0

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

        #length of bottom of left leg (knee to ankle)
        lbleg = np.sqrt((lankle[0] - lknee[0])**2 + (lankle[1] - lknee[1])**2)
        #length of top of left leg (knee to hip)
        ltleg = np.sqrt((lknee[0] - lhip[0])**2 + (lknee[1] - lhip[1])**2)
        #total length of leg (bottom+top) - used for ratio for distance between legs during step
        self.lleg = (lbleg + ltleg)
        print("************** CALIBRATION SUCCESSFUL ****************")

    def capture_kick(self,
        landmarks,
        start_kick_time,              
        image,
        examine_checks):
        return_examine_checks = True

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
    
        if rknee_angle >= 70 and rknee_angle <= 115:
            if (self.knee_completed == False):
                print("+++++++++++++++++++++++++++ KNEE LIFT DETECTED +++++++++++++++++++++++++++")
                print(">>>>>>>>> CAPTURING KNEE")
                cv2.putText(image, "Captured Knee!",
                            tuple(np.multiply([0,0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (255,255,255), 2, cv2.LINE_AA) 
                print("%%%%%%%%%%%%%%%%% WRITING KNEE IMAGE %%%%%%%%%%%%%%%%")
                cv2.imwrite(self.knee_file_name, image)
                self.knee_complted = True

        elif rknee_angle <= 10 and rhip_angle > 70 and rhip_angle < 110 and self.knee_completed:
                print("+++++++++++++++++++++++++++ KICK DETECTED +++++++++++++++++++++++++++")
                print(">>>>>>>>> CAPTURING KICK")
                cv2.putText(image, "Captured Kick!",
                            tuple(np.multiply([0,0.05], [640, 480]).astype(int)),
                            cv2.QT_FONT_NORMAL, 1, (255,255,255), 2, cv2.LINE_AA) 
                print("%%%%%%%%%%%%%%%%% WRITING KICK IMAGE %%%%%%%%%%%%%%%%")
                cv2.imwrite(self.kick_file_name, image)
                return_examine_checks = False

                
        else:
            cv2.putText(image, "1. Turn left",
                        tuple(np.multiply([0,0.05], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, "2. Get in fighting stance",
                        tuple(np.multiply([0,0.13], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, "3. Lift right knee and kick",
                        tuple(np.multiply([0,0.21], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, "4. Land in fighting stance",
                        tuple(np.multiply([0,0.25], [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA)

            return_examine_checks = examine_checks
        
        return return_examine_checks
