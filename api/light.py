import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
values_json_path = os.path.join(project_dir, 'value.json')
import copy
from random import randint
import json

from config import bulb_ips

from hand_gesture import class_names


def turn_on():
    # Read the contents of the JSON file
    with open(values_json_path, 'r') as file:
        data = json.load(file)

    # Make changes to the data
    data["light"]=True

    # Write the modified data back to the JSON file
    with open(values_json_path, 'w') as file:
        json.dump(data, file, indent=4)


def turn_off():
    # Read the contents of the JSON file
    with open(values_json_path, 'r') as file:
        data = json.load(file)

    data["light"]=False

    with open(values_json_path, 'w') as file:
        json.dump(data, file, indent=4)


def increase_speed():
    with open(values_json_path, 'r') as file:
        data = json.load(file)
    data["fan"]=True

    with open(values_json_path, 'w') as file:
        json.dump(data, file, indent=4)


def decrease_speed():
    # Read the contents of the JSON file
    with open(values_json_path, 'r') as file:
        data = json.load(file)
    data["fan"]=False

    # Write the modified data back to the JSON file
    with open(values_json_path, 'w') as file:
        json.dump(data, file, indent=4)

def light_action(command,number_of_time):

    print(command)
    if command == class_names[0]:
        turn_on()
    if command == class_names[1]:
        turn_off()
    if command == class_names[2]:
        increase_speed()
    if command == class_names[3]:
        decrease_speed()
    
    