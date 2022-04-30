import mediapipe as mp

import torch

import cv2
import numpy as np

from hand_gesture.model import HandGestureModel
from hand_gesture.utils import normalize
from hand_gesture.config import class_names, confidence_threshold


mp_hands       = mp.solutions.hands
hand_detection = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw        = mp.solutions.drawing_utils

model = HandGestureModel()
model.load_state_dict(torch.load('./hand_gesture/models/2022-04-30-0/model.pt'))
model.eval()


def hand_gesture_inference(image):
    landmarks, image = detection(image=image)
    action = None
    value = 0
    if landmarks != []:
        landmarks = normalize(landmarks=landmarks)
        logits = hand_gesture_predict(landmarks=landmarks)
        print(logits)
        values, indices = logits.topk(1, dim=1)
        value, index = values.item(), indices.item()
        if value >= confidence_threshold:
            action = class_names[index]
            print(action)
    return image, action, value
    

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


def hand_gesture_predict(landmarks):
    with torch.no_grad():
        landmarks = np.array([landmarks], dtype=np.float32)
        landmarks = torch.tensor(landmarks)
        logits = model(landmarks)
    return logits


if __name__ == '__main__':
    image = cv2.imread('/Users/chi/Downloads/ex2.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    landmarks, result_image = detection(image)
    print(landmarks)
