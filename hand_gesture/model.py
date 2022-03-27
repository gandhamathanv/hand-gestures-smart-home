from tensorflow.keras.models import load_model


def load_hand_gesture_model():
    model = load_model('./hand_gesture/mp_hand_gesture')
    return model
