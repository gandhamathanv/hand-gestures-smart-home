import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
values_json_path = os.path.join(project_dir, 'value.json')
print(values_json_path)
import copy
from random import randint
import json

from yeelight import Bulb
from yeelight import RGBTransition
from yeelight import Flow
from config import bulb_ips

from hand_gesture import class_names


bulb1 = Bulb(bulb_ips[0])
bulb2 = Bulb(bulb_ips[1])


def toggle_light():
    # Read the contents of the JSON file
    with open(values_json_path, 'r') as file:
        data = json.load(file)

    # Make changes to the data
    if data['light']==100:
        data['light']=0
    else:
        data['light']=100

    # Write the modified data back to the JSON file
    with open(values_json_path, 'w') as file:
        json.dump(data, file, indent=4)


def increase_brightness(number_of_time):
    # Read the contents of the JSON file
    with open(values_json_path, 'r') as file:
        data = json.load(file)

    data['light']+=1*number_of_time

    # Write the modified data back to the JSON file
    with open(values_json_path, 'w') as file:
        json.dump(data, file, indent=4)


def decrease_brightness():
    bulb1.set_brightness(int(bulb1.get_properties()['bright']) - 20)
    bulb2.set_brightness(int(bulb2.get_properties()['bright']) - 20)


def toggle_color_temp():
    ct = copy.copy(int(bulb1.get_properties()['ct']))
    if ct != 6000:
        bulb1.set_color_temp(6000)
        bulb2.set_color_temp(6000)
    else:
        bulb1.set_color_temp(3000)
        bulb2.set_color_temp(3000)


def random_color():
    red   = randint(0, 255)
    green = randint(0, 255)
    blue  = randint(0, 255)
    bulb1.set_rgb(red,green,blue)
    bulb2.set_rgb(red,green,blue)


def disco_toggle():
    if int(bulb1.get_properties()['flowing']) != 1:
        transitions = [RGBTransition(255, 0, 0),RGBTransition(0, 255, 0),RGBTransition(0, 0, 255)]
        flow = Flow(0, Flow.actions.recover, transitions)
        bulb1.start_flow(flow)
        bulb2.start_flow(flow)
    else:
        bulb1.set_color_temp(6000)
        bulb2.set_color_temp(6000)


def light_action(command,number_of_time):
    if command == class_names[0]:
        toggle_light()
    if command == class_names[1]:
        increase_brightness(number_of_time)
    # if command == class_names[2]:
    #     decrease_brightness()
    # if command == class_names[3]:
    #     toggle_color_temp()
    # if command == class_names[4]:
    #     random_color()
    # if command == class_names[5]:
    #     disco_toggle()
    