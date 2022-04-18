import mediapipe as mp

import os
import pyheif
from PIL import Image


def init_mediapipe():
    mp_hands = mp.solutions.hands
    hands    = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw  = mp.solutions.drawing_utils

    return mp_hands, hands, mp_draw


def load_image(image_path):
    extension = image_path.split('.')[-1]
    if extension in ['heic', 'HEIC']:
        heif_file = pyheif.read(image_path)
        image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, 'raw', heif_file.mode, heif_file.stride)
    else:
        image = Image.open(image_path)
    return image


def mkdir_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def normalize(landmarks):
    base_x, base_y = landmarks[0][0], landmarks[0][1]
    landmarks = [[landmark[0] - base_x, landmark[1] - base_y] 
                  for landmark in landmarks]
    max_value = max([max([abs(x) for x in landmark]) 
                  for landmark in landmarks])
    landmarks = [[landmark[0] / max_value, landmark[1] / max_value] 
                  for landmark in landmarks]
    return landmarks
