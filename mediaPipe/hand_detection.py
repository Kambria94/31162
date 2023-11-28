import mediapipe as mp
import cv2
import numpy as np
import uuid
import os

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

cap.set(3, 1000)
cap.set(4, 600)


def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:

            #process results
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))

            #extract coordinates
            coords = tuple(np.multiply(
                np.array(hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y),
                [640, 480].astype(int)))
            
            output = label
        
        return output


with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while cap.isOpened:
        ret, frame = cap.read()
        
        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Flip on horizontal
        image = cv2.flip(image, 1)
        
        # Set flag
        image.flags.writeable = False
        
        # Detections
        results = hands.process(image)
        
        # Set flag to true
        image.flags.writeable = True
        
        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

         # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):

                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(221, 122, 76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                        )
        try:
            for index, arm in enumerate(results.multi_handedness):
                #index = arm.classification[0].index
                thumbX = results.multi_hand_landmarks[index].landmark[4].x
                thumbY = results.multi_hand_landmarks[index].landmark[4].y
                indexX = results.multi_hand_landmarks[index].landmark[8].x
                indexY = results.multi_hand_landmarks[index].landmark[8].y
                dX = indexX - thumbX
                dY = indexY - thumbY
                distance = np.sqrt(dX**2 + dY**2)
                if distance <= 0.03:
                   print(arm.classification[0].label + " touching")
           
            
                  
        except: 
            pass

        cv2.imshow("Mediapipe feed", image)
        
        if cv2.waitKey(10) & 0xFF == ord("x"):
            break
        
        # Detections
        