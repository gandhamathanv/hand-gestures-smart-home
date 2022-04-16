import cv2

from hand_gesture.prediction import hand_gesture_inference


print('Initializing webcam...')
cv2.namedWindow("preview")
cap = cv2.VideoCapture(0)

print('Start capture...')
while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image, action = hand_gesture_inference(image=frame_rgb)

    cv2.putText(image, action, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0,0,255), 2, cv2.LINE_AA)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow('Output', image) 

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
