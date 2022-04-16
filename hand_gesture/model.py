import numpy as np

import torch
from torch import nn
from tensorflow.keras.models import load_model


def load_hand_gesture_model():
    model = load_model('./hand_gesture/mp_hand_gesture')
    return model


class HandGestureModel(nn.Module):
    
    def __init__(self):
        super(HandGestureModel, self).__init__()

        self.classifier = nn.Sequential(
            # nn.Linear(in_features=42, out_features=100),
            # nn.ReLU(),
            # nn.Linear(in_features=100, out_features=100),
            # nn.ReLU(),
            # nn.Linear(in_features=100, out_features=100),
            # nn.ReLU(),
            # nn.Linear(in_features=100, out_features=6)
            nn.Linear(in_features=42, out_features=64),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(in_features=64, out_features=128),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(in_features=128, out_features=512),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(in_features=512, out_features=64),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(in_features=64, out_features=32),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=6),
        )

        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = torch.flatten(x, start_dim=1)
        x = self.classifier(x)
        return self.sigmoid(x)


if __name__ == '__main__':
    hand_gesture_model = HandGestureModel()
    landmarks = [
        [525, 467], [506, 451], [498, 397], [504, 337], [512, 295], [486, 309], [480, 215], 
        [478, 162], [477, 116], [504, 299], [507, 256], [511, 315], [510, 352], [523, 301], 
        [526, 273], [527, 333], [526, 363], [541, 309], [545, 268], [546, 283], [545, 285]
    ]
    landmarks = np.array(landmarks, dtype=np.float32)
    landmarks = torch.tensor(landmarks)
    print(landmarks.dtype)
    print(hand_gesture_model(landmarks))
