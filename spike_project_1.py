from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()
distance = DistanceSensor('A')
color_scanner = ColorSensor("B")
door_bell = ForceSensor('C')

color_log = ["nullnullcolor"]
last_color_log_len = 0

# hub.light_matrix.show_image('HAPPY')
distance.light_up_all(0) # init distance light!
distance.light_up_all(100)
while True:
    # distance.wait_for_distance_farther_than(10, 'cm', False)
    # print("Distance Farther then 10! {0}".format(distance.get_distance_cm(False)))
    distance_cm = distance.get_distance_cm(False)
    color = color_scanner.get_color();
    if door_bell.is_pressed():
        newtons = door_bell.get_force_newton()
        if newtons <= 5:if last_color_log_len == len(color_log): continue;
        else:print("Strong Press... ignore pressing....")
        print("Length of color_log: {0}".format(len(color_log)))
        last_color_log_len = len(color_log)
    if distance_cm == None:continue;
    if distance_cm >= 100: print("target is so far! target: {0} cm".format(distance_cm))
    if distance_cm >= 200: break;
    if color != None:
        if color_log[-1] != color:
            color_log.append(color)
            print("Detected Color:", color)
    # print("{0}".format(distance.get_distance_cm(False)))
