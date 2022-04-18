class_names = ['turn_on-off', 'increase_brightness', 'decrease_brightness', 'coloring_temp', 'coloring_randomly', 'coloring_disco']
class_names_to_idx = {class_name: i for i, class_name in enumerate(class_names)}
widths = [205, 325, 335, 235, 300, 240]

data_path = './data/dataset.json'

batch_size = 4
lr = 0.0001
epochs = 1000
gamma = 0.97

confidence_threshold = 0.92
