import mediapipe as mp

import os
import matplotlib.pyplot as plt


def init_mediapipe():
    mp_hands = mp.solutions.hands
    hands    = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw  = mp.solutions.drawing_utils

    return mp_hands, hands, mp_draw


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


def plot(train_data, val_data, name, save_dir):
    with plt.style.context('ggplot'):
        plt.figure(figsize=(10, 6), dpi=80)
        plt.plot(train_data)
        plt.plot(val_data)
        plt.title(f'Model {name}')
        plt.ylabel(name)
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.savefig(os.path.join(save_dir, f'{name}.jpg'))
