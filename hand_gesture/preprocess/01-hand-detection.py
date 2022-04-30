import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_dir)

import cv2
import pickle
from tqdm import tqdm

from hand_gesture import detection, mkdir_if_not_exists


data_directory = 'data'
image_directory = os.path.join(data_directory, 'image')
keypoint_directory = os.path.join(data_directory, 'keypoint')
mkdir_if_not_exists(keypoint_directory)

video_types = ['only-hand-fix'] # only-hand, include-body

for action in os.listdir(image_directory):
    mkdir_if_not_exists(os.path.join(keypoint_directory, action))
    if action.startswith('.'):
        continue
    for video_type in video_types:
        video_dir = os.path.join(image_directory, action, video_type)
        pickle_dir = os.path.join(keypoint_directory, action, video_type)
        mkdir_if_not_exists(pickle_dir)
        print(f'action: {action} video_type: {video_type}')
        for file in tqdm(os.listdir(video_dir)):
            if file.startswith('.'):
                continue
            basename = file.split('.')[0]

            video_path = os.path.join(video_dir, file)
            video = cv2.VideoCapture(video_path)

            success, frame = video.read()
            n_frame = 0
            while success:
                pickle_path = os.path.join(pickle_dir, f'{basename}_{n_frame:04d}.pkl')
                if not os.path.exists(pickle_path):
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    landmarks, _ = detection(image=frame_rgb)

                    pickle_path = os.path.join(pickle_dir, f'{basename}_{n_frame:04d}.pkl')
                    with open(pickle_path, 'wb') as file:
                        pickle.dump(landmarks, file)
                
                success, frame = video.read()
                n_frame += 1
