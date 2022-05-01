import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

import copy
from random import randint

from yeelight import Bulb
from yeelight import RGBTransition
from yeelight import Flow

from hand_gesture import class_names


bulb1 = Bulb('192.168.1.71')
bulb2 = Bulb('192.168.1.62')


def toggle_light():
    bulb1.toggle()
    bulb2.toggle()


def increase_brightness():
    bulb1.set_brightness(int(bulb1.get_properties()['bright']) + 20)
    bulb2.set_brightness(int(bulb2.get_properties()['bright']) + 20)


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


def light_action(command):
    if command == class_names[0]:
        toggle_light()
    if command == class_names[1]:
        increase_brightness()
    if command == class_names[2]:
        decrease_brightness()
    if command == class_names[3]:
        toggle_color_temp()
    if command == class_names[4]:
        random_color()
    if command == class_names[5]:
        disco_toggle()
    