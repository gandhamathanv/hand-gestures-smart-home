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

<img src="https://media-cdn.bnn.in.th/11189/Google-Nest-Mini-Chalk-01.jpg" width="300"> <img src="https://www.tradeinn.com/f/13782/137822089/apple-homepod-mini.jpg" width="250"> <img src="https://www.powerplanetonline.com/cdnassets/amazon_echo_dot_3_gen_negro_antracita_altavoz_inteligente_alexa_01_l.jpg" width="250">

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


