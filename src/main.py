import processes
import imageprocessing
from multiprocessing import Process, Value, Manager

from serialcom import RoboSerial


def start_processes(Robo_serial, l):
    run = processes.Value("i", 1)
    robot_communication = processes.Process(name="Serial", target=processes.serial_worker, args=(run, Robo_serial, l))
    robot_vision = processes.Process(name="Vision", target=processes.vision_worker, args=(run, l))
    robot_vision.start()
    robot_communication.start()

    return run, robot_communication, robot_vision

if __name__ == "__main__":

    try:
        print(RoboSerial.available_ports())
        
        portname = "ttyACM0"
        Robo_serial = RoboSerial("ttyACM0", "utf-8")

        manager = Manager()
        l = manager.list([0, 0, 0])

    except Exception as e:
        print("except: ", e)

    run, robot_communication, robot_vision = start_processes(Robo_serial, l)

    
    
    while True:
        print("main",imageprocessing.stop())

        if imageprocessing.stop():
            robot_vision.Close()
            robot_communication.Close()
            exit()
        input()
        
        run.value = not run.value
        print("Running: ", run.value)
        
            


