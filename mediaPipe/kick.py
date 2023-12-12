import cv2
import mediapipe as mp
import numpy as np
import datetime


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
start_time = datetime.datetime.timestamp(datetime.datetime.now())


def calculate_angle(a,b,c):
    a = np.array(a) #first
    b = np.array(b) #middle
    c = np.array(c) #end


    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180/np.pi)


    if angle > 180:
        angle = 360-angle


    return angle


snaptime = 0
start_snap = 0

#Video feed
img = cv2.VideoCapture(0)


#setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:


    while img.isOpened:
        ret, frame = img.read()
    
        #Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        #Make detection
        results = pose.process(image)
        #Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        #Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            #Measurements
            rknee = calculate_angle(rhip, rknee , rankle)
            rhip = calculate_angle(rshoulder, rhip, rknee)
            kneeup = False
            snap = False
            
            if (rknee <= 130 and rhip <= 130) and kneeup == False:
                print ("Knee Up")
                start_snap = datetime.datetime.timestamp(datetime.datetime.now())
                kneeup = True
            if kneeup == True:
                if rknee >= 160:
                    snap = True
                    kneeup = False
            #if snap == True and 

           
            #distance = np.sqrt((rshoulder[0] - rwrist[0])**2 + (rshoulder[1] - rwrist[1])**2)
            #print(distance)
            if datetime.datetime.timestamp(datetime.datetime.now()) >= start_time+5:
                print("hi")
                start_time = datetime.datetime.timestamp(datetime.datetime.now())

        except:
            pass
        #Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                )
  
        cv2.imshow("Mediapipe feed", image)
       
        if cv2.waitKey(10) & 0xFF == ord("x"):
            break


    img.release()
    cv2.destroyAllWindows()
