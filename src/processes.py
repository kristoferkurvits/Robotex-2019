import imageprocessing
from multiprocessing import Process, Value

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

    Robo_serial.speeds = processes_variables[:3]
    if processes_variables[4]:
        Robo_serial.start_throw(False)
        processes_variables[4] = 0
        
    Robo_serial.send_speeds()

def vision_worker(run, process_variables):
    while 1:
        if run.value:
            vision_process(process_variables)

def vision_process(process_variables):
    imageprocessing.start(process_variables)
    print(process_variables, "MA OLEN PROCESSES.PY")

    






