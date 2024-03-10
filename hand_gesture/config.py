class_names = ['turn_on', 'turn_off', 'fan_on', 'fan_off']
class_names_to_idx = {class_name: i for i, class_name in enumerate(class_names)}
widths = [205, 325, 335, 235, 300, 240]

data_path = './data/dataset.json'

model_dir = './hand_gesture/models'


batch_size = 8
lr = 0.0001
epochs = 50
gamma = 0.97

confidence_threshold = 0.999
