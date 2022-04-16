import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_dir)

import numpy as np
import pickle
from tqdm import tqdm

from hand_gesture import load_image, detection, mkdir_if_not_exists


data_directory = 'data'
image_directory = os.path.join(data_directory, 'image')
keypoint_directory = os.path.join(data_directory, 'keypoint')

image_types = ['only-hand'] # only-hand, include-body

for action in os.listdir(image_directory):
    mkdir_if_not_exists(os.path.join(keypoint_directory, action))
    if action.startswith('.'):
        continue
    for image_type in image_types:
        image_dir = os.path.join(image_directory, action, image_type)
        pickle_dir = os.path.join(keypoint_directory, action, image_type)
        mkdir_if_not_exists(pickle_dir)
        print(f'action: {action} image_type: {image_type}')
        for image_name in tqdm(os.listdir(image_dir)):
            basename = image_name.split('.')[0]
            image_path = os.path.join(image_dir, image_name)
            pickle_path = os.path.join(pickle_dir, f'{basename}.pkl')
            if os.path.exists(pickle_path):
                continue

            image = load_image(image_path=image_path)
            image = np.array(image)

            landmarks, _ = detection(image=image)

            with open(pickle_path, 'wb') as file:
                pickle.dump(landmarks, file)
