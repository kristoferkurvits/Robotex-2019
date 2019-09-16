import imageprocessing
import time

"""
    serial_worker - function that supervises the serial process to stop it when necessary
    serial_process - process that sends the speeds for the motors over serial
    vision_worker - supervises the vision process to stop it when necessary
    vision_process - process that detects balls and basket from the image 
        and modifies the current speeds to be sent
"""
def serial_worker(run, Robo_serial, processes_variables):
    while 1:
        if run.value:
            serial_process(Robo_serial, processes_variables)

def serial_process(Robo_serial, speeds):
    Robo_serial.speeds = speeds[:3]
    Robo_serial.send_speeds()

def vision_worker(run, process_variables):
    while 1:
        if run.value:
            vision_process(process_variables)

def vision_process(process_variables):
    imageprocessing.start(process_variables)

    






