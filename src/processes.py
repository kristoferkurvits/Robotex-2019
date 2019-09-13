from multiprocessing import Process, Value

import imageprocessing
import time

"""
right_wheel_angle = 120
middle_wheel_angle = 0
left_wheel_angle = 240
"""

def serial_worker(run, Robo_serial, processes_variables):

    while 1:
        if run.value:
            serial_process(Robo_serial, processes_variables)

def serial_process(Robo_serial, speeds):
    print("serial thread")

    Robo_serial.speeds = speeds[:3]
    
    Robo_serial.send_speeds()




#changed arguments name
def vision_worker(run, process_variables):
    while 1:
        if run.value:
            vision_process(process_variables)



"""

"""
def vision_process(process_variables):
    print("vision thread")
    imageprocessing.start(process_variables)

    






