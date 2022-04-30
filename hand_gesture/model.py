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
