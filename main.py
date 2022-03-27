import cv2
import numpy as np

from hand_gesture.model import load_hand_gesture_model
from hand_gesture.utils import init_mediapipe
from hand_gesture.config import class_names


print('Initializing mediapipe...')
mp_hands, hands, mp_draw = init_mediapipe()

print('Loading model...')
model = load_hand_gesture_model()

print(class_names)

# Initialize the webcam
print('Initializing webcam...')
cap = cv2.VideoCapture(0)

print('Start capture...')
while True:
    _, frame = cap.read()
    x, y, _ = frame.shape

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(frame_rgb)
    # print(result)
    
    class_name = ''

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        
        for hand_landmarks in result.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                landmark_x = int(landmark.x * x)
                landmark_y = int(landmark.y * y)
                landmarks.append([landmark_x, landmark_y])
            print(landmarks)

            # Drawing landmarks on frames
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model.predict([landmarks])

            class_id = np.argmax(prediction)
            class_name = class_names[class_id]

    # show the prediction on the frame
    cv2.putText(frame, class_name, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,0,255), 2, cv2.LINE_AA)

    # Show the final output
    cv2.imshow('Output', frame) 

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()

cv2.destroyAllWindows()
