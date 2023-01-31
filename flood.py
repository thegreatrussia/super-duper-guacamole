from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()
motor_pair_odin = MotorPair('F', 'A')
motor_pair_dva = MotorPair('B', 'E')
distance = DistanceSensor('C')
force = ForceSensor('D')

init_required = False
is_up = False

distance.light_up_all() # 거리 센서 불 킴

while True:
    if init_required == True:
        print("initing something cool...")
        distance.light_up_all(100)
        init_required = False
    
    if force.is_pressed() and force.get_force_newton()!=None:
        if is_up == False:
            print("Ignore")
        elif force.get_force_newton() >= 5:
            print("Going Down Suckers!")
            for i in range(0,7):
                hub.speaker.beep(60, 0.5)
                motor_pair_odin.move(1, 'cm', -100, 100)
                motor_pair_dva.move(1, 'cm', -100, -100)
            is_up = False
            init_required = True
            continue;
    print(distance.get_distance_cm())
    if distance.get_distance_cm()!=None:
        if distance.get_distance_cm() <= 20:
            distance.light_up_all(0)
            for i in range(0,3):
                hub.speaker.beep(60, 0.5)
            for i in range(0,7):
                motor_pair_odin.move(1, 'cm', 100, 100)
                motor_pair_dva.move(1, 'cm', 100, -100)
            is_up = True
            # wait_for_seconds(5)
            continue;
            
