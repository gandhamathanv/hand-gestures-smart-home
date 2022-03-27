import mediapipe as mp


def init_mediapipe():
    mp_hands = mp.solutions.hands
    hands    = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw  = mp.solutions.drawing_utils

    return mp_hands, hands, mp_draw
