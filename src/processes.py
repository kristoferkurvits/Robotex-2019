import imageprocessing
from multiprocessing import Process, Value
import time
from robot_LUT import get_thrower_speed

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

def serial_process(Robo_serial, processes_variables):
    if Robo_serial.drive:
        Robo_serial.speeds = [-70, 0, 70]
        Robo_serial.send_speeds()
        time.sleep(0.3)
        Robo_serial.drive = 0
    sleep_next = False
    Robo_serial.speeds = processes_variables[:3]
    if processes_variables[4]:
        throwing_speed = get_thrower_speed(processes_variables[3])
        print(f"VISKAN, Kaugus: {processes_variables[3]}, Kiirus: {throwing_speed}")
        Robo_serial.start_throw(False, throwing_speed)
        time.sleep(0.5)
        processes_variables[4] = 0
        sleep_next = True
        Robo_serial.speeds = [-30, 0, 30]
    Robo_serial.refereeHandler()
    time.sleep(0.001)
    if Robo_serial.working:
        Robo_serial.send_speeds()
        time.sleep(0.001)
        if sleep_next:
            time.sleep(1.05)
            Robo_serial.start_throw(True)
        
    


def vision_worker(run, process_variables):
    while 1:
        if run.value:
            vision_process(process_variables)

def vision_process(process_variables):
    imageprocessing.start(process_variables)
    print(process_variables, "MA OLEN PROCESSES.PY")

    






