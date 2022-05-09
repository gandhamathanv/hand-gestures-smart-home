# hand-gestures-smart-home

## Overview
Interact with smart home via hand gestures.

## Installation
- Clone repository
```shell
git clone git@github.com:chaichana-t/hand-gestures-smart-home.git
cd hand-gestures-smart-home
```
- Install dependencies (recommend python version >= 3.9)
```shell
pip install -r requirements.txt
```

## How to use
- Run app
```shell
python main.py
```

## Supporting
- Supporting smart home interactions
  - Turn on / off
  - Increase brightness
  - Decrease brightness
  - Coloring
    - Temperature
    - Randomly pick
    - Disco  

# Information
## Problem Statement
Voice is being used as an input for interaction in smart home devices. However, some people aren’t be able to use their voice like everyone else. For example, Deaf people. We recognize the difficulty and want to ensure that everyone has access to smart home technology. As a result, we'll be utilizing computer vision to address this issue.

<img src="/assets/google-nest.jpg" width="300"> <img src="/assets/apple-homepod.jpg" width="250"> <img src="/assets/amazon-echo.jpg" width="250">

## Technical Challenges
We can't predict if users would gesture only the actions that are presented in real-world settings. As a result, we've utilized certain strategies to overcome, which we'll discuss in the upcoming session.

## Related Works
From our researches we found two possible approaches for the work
- Real-time Hand Gesture Recognition: [link](https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/)
  - Detect hand using Google MediaPipe.
  - Recognize hand gesture using hand landmarks using Neural Networks.
- Hand Detection using Object Detection
  - Detect hand with its action using object detection approach.

## Method and Results
- AI
  - Hand Detection
  - Hand Gesture Recognition
- APP
  - Motion Interval
  - Yeelight connection

### AI
Use two stages model
- Hand Detection
- Hand Gesture Recognition
![Model Overview](/assets/model-overview.png)

#### Hand Detection
  - Google MediaPipe (ref. [Github](https://github.com/google/mediapipe))
#### Hand Gesture Recognition
  - Data
    - Collected by ourselves <br /> <br />
      <img src="/assets/data-count.png" width="500">
  - Model
    - Fully Connected Neural Network
      - Input: Coordinate x, y of each key points
        - Normalized by position and size <br /> <br />
          ```py
          def normalize(landmarks):
              base_x, base_y = landmarks[0][0], landmarks[0][1]
              landmarks = [[landmark[0] - base_x, landmark[1] - base_y] 
                            for landmark in landmarks]
              max_value = max([max([abs(x) for x in landmark]) 
                            for landmark in landmarks])
              landmarks = [[landmark[0] / max_value, landmark[1] / max_value] 
                            for landmark in landmarks]
              return landmarks
          ```
        - `[[x0, y0], [x1, y1], …, [x20, y20]]`
      - Output: Action
      - Model Architecture
        ```py
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
          ```
  - Our Contribute (from Technical Challenges)
    - This problem is `Multiclass Single-label Classification`
      - Typical `Softmax` and `CrossEntropyLoss` were applied.
        - Model can recognize every action with high confidence.
        - What about edge cases if we don’t have in dataset?
      - We applied `Sigmoid` and `BCELoss` for idealy minimizing all action's probabilities of edge cases to zero.
        - Train it like `Multiclass Multi-label Classification` (but each label has an 1’s in one-hot encoding)
        - Inference using max confidence and thresholding `0.999`
        - However, this does not perfectly work.

#### Result
- Model Training <br />
<img src="/hand_gesture/models/2022-04-30-0/loss.jpg" width="450"> <img src="/hand_gesture/models/2022-04-30-0/accuracy.jpg" width="450">
- Model Evaluation
  - Classification Report
    ```
                  precision    recall  f1-score   support

               0     1.0000    1.0000    1.0000       613
               1     1.0000    1.0000    1.0000       556
               2     1.0000    1.0000    1.0000       143
               3     1.0000    1.0000    1.0000       618
               4     1.0000    1.0000    1.0000       550
               5     1.0000    1.0000    1.0000       458

        accuracy                         1.0000      2938
       macro avg     1.0000    1.0000    1.0000      2938
    weighted avg     1.0000    1.0000    1.0000      2938
    ```
  - Confusion Matrix <br />
    <img src="/assets/confusion-matrix.png" width="400"> <br /> <br />
    
### APP
- Motion Interval
  - We use time as interval in order to request Yeelight API which currently is 2 seconds.
- Yeelight connection
  - We use YeeLight python library to control our smart light bulb.
  - Our actions that could be used by the model
    - Turn on / off (toggle)
    - Increase brightness
    - Decrease brightness
    - Coloring
      - Temp (toggle)
      - Randomly pick
      - Disco
- Gesture Action

  <table>
    <tr>
      <td> <img src="/assets/action-0.png" alt="1" height="200"> </td>
      <td> <img src="/assets/action-1.png" alt="2" height="200"> </td>
      <td> <img src="/assets/action-2.png" alt="3" height="200"> </td>
    </tr> 
      <td> Turn on / off (toggle) </td>
      <td> Increase brightness </td>
      <td> Decrease brightness </td>
    <tr>
      <td> <img src="/assets/action-3.png" alt="1" height="200"> </td>
      <td> <img src="/assets/action-4.png" alt="2" height="200"> </td>
      <td> <img src="/assets/action-5.png" alt="3" height="200"> </td>
    </tr> 
      <td> Temp (toggle) </td>
      <td> Randomly pick </td>
      <td> Disco </td>
  </table>

## Limitations and Future Work
### AI
- Sufficient lighting is required
- Improve model performance such that actions that aren't supplied aren't recognized
- Improve model more generalized to recognize all possible hand gestures
### APP
- Improve UX/UI
- Port it onto smaller device
- Expand it to more smart devices (Not only Yeelight bulb)
