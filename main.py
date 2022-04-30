import cv2
from datetime import datetime  

from hand_gesture.prediction import hand_gesture_inference
from hand_gesture.config import class_names_to_idx, widths
from config import time_interval

from api.light import light_action


print('Initializing webcam...')
cv2.namedWindow("preview")
cap = cv2.VideoCapture(0)

print('Start capture...')
state = None
start_time_action =  datetime.now()  
while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image, action, confidence = hand_gesture_inference(image=frame_rgb)
    if action != None:
        if state != action:
            state = action 
            start_time_action = datetime.now()
        else:
            number_of_time = datetime.now()  -  start_time_action
            number_of_time = number_of_time.total_seconds() 
            if number_of_time > time_interval:
                light_action(state)
                print(state)
                state = None
        idx = class_names_to_idx[action]
        cv2.rectangle(image, (5, 20), (widths[idx], 85), (255, 255, 255), -1)
        cv2.putText(image, action, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(image, f'confidence: {confidence:.4f}', (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (0, 0, 255), 1, cv2.LINE_AA)
    else: 
        state = action 

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow('Output', image) 

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
