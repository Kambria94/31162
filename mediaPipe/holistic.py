import mediapipe as mp
import cv2
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

width = 2240
height = 1400

img = cv2.VideoCapture(0)
cv2.namedWindow("Mediapipe feed", cv2.WINDOW_NORMAL) 

cv2.resizeWindow("Mediapipe feed", width, height)

color = 0


def calculate_angle(a,b,c):
    a = np.array(a) #first
    b = np.array(b) #middle
    c = np.array(c) #end

    #0 is x-value, 1 is y-value
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180/np.pi)

    if angle > 180:
        angle = 360-angle

    return angle

#setup mediapipe instance
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    while img.isOpened:
        ret, frame = img.read()
        

        #Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        #Make detection
        results = holistic.process(image)
        #Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #Extract landmarks
        angle = 90
        try:
            landmarks = results.pose_landmarks.landmark
            rshoulder = [landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].y]
            rhip = [landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].y]
            relbow = [landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].y]
            shoulder_angle = round(calculate_angle(rhip, rshoulder, relbow), 0).astype(int)
            if shoulder_angle >= 90:
                color = (0,255,0)
            else:
                color = (0,0,255)
            cv2.putText(image, str(shoulder_angle),
                        tuple(np.multiply([rshoulder[0]-0.05, rshoulder[1]-0.05], [width/2, height/2]).astype(int)),
                        cv2.QT_FONT_NORMAL, 1, color, 2, cv2.LINE_AA
                        )

        except Exception as e:
            print(e)
        


        #Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
                                )
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                mp_drawing.DrawingSpec(color=(221, 122, 76), thickness=2, circle_radius=4),
                                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                )
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                mp_drawing.DrawingSpec(color=(221, 122, 76), thickness=2, circle_radius=4),
                                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                )



        cv2.imshow("Mediapipe feed", image)
        
        if cv2.waitKey(10) & 0xFF == ord("x"):
            break

img.release()
cv2.destroyAllWindows()
