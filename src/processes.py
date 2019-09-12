from multiprocessing import Process, Value

import imageprocessing
import time

def serial_worker(run, Robo_serial, processes_variables):

    while 1:
        if run.value:
            serial_process(Robo_serial, processes_variables)

def serial_process(Robo_serial, speeds):
    print("serial thread")

    Robo_serial.speeds = speeds[:3]
    
    Robo_serial.send_speeds()




def vision_worker(run, Robo_serial):
    while 1:
        if run.value:
            vision_process(Robo_serial)



"""

"""
def vision_process(Robo_serial):
    print("vision thread")
    imageprocessing.start(Robo_serial)

    






