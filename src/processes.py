from multiprocessing import Process, Value

import imageprocessing
import time

def serial_worker(run, Robo_serial):

    while 1:
        if run.value:
            serial_process(Robo_serial)

def serial_process(Robo_serial):
    print("serial thread")
    Robo_serial.test_serial()
    print(Robo_serial.speeds)
    time.sleep(1)



def vision_worker(run, Robo_serial):
    while 1:
        if run.value:
            vision_process(Robo_serial)


def vision_process(Robo_serial):
    print("vision thread")
    imageprocessing.start(Robo_serial)

    time.sleep(1)
    






