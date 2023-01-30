from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()
motor = MotorPair('B', 'A')
# distance = DistanceSensor('A')
# color_scanner = ColorSensor("B")
door_bell = ForceSensor('F')
start = 1

while True:
    if door_bell.is_pressed(): break
    motor.move(100, 'cm', 0, 100)
    start += 1

# while True:
