import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_dir)

import pickle
import json
from sklearn.model_selection import train_test_split

from hand_gesture import normalize


data_directory = 'data'
image_directory = os.path.join(data_directory, 'image')
keypoint_directory = os.path.join(data_directory, 'keypoint')

image_types = ['only-hand-fix'] # only-hand, include-body

X = []
y = []
for action in os.listdir(keypoint_directory):
    if action.startswith('.'):
        continue
    for image_type in image_types:
        pickle_dir = os.path.join(keypoint_directory, action, image_type)
        for filename in os.listdir(pickle_dir):
            basename = filename.split('.')[0]
            pickle_path = os.path.join(pickle_dir, f'{basename}.pkl')

            with open(pickle_path, 'rb') as file:
                landmarks = pickle.load(file)
            
            if landmarks == []:
                continue
            
            landmarks = normalize(landmarks=landmarks)
            X.append(landmarks)
            y.append(action)

random_state = 32
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, 
                                                    random_state=random_state,
                                                    stratify=y)

data = {
    'train': {
        'features': X_train,
        'labels': y_train,
    },
    'test': {
        'features': X_test,
        'labels': y_test,
    },
}
with open(os.path.join(data_directory, 'dataset.json'), 'w') as file:
    json.dump(data, file, indent=4)
