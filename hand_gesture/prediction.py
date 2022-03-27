import mediapipe as mp

import cv2


mp_hands       = mp.solutions.hands
hand_detection = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw        = mp.solutions.drawing_utils


def detection(image):
    height, width, _ = image.shape

    result = hand_detection.process(image)

    landmarks = []
    if not result.multi_hand_landmarks:
        return landmarks, image

    for hand_landmarks in result.multi_hand_landmarks:
        for landmark in hand_landmarks.landmark:
            landmark_x = int(landmark.x * height)
            landmark_y = int(landmark.y * width)
            landmarks.append([landmark_x, landmark_y])
        
        mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    return landmarks, image


if __name__ == '__main__':
    image = cv2.imread('/Users/chi/Downloads/ex2.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    landmarks, result_image = detection(image)
    print(landmarks)
