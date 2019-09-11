import processes
import imageprocessing
from multiprocessing import Process, Value
from serialcom import RoboSerial


def start_processes(Robo_serial):
    run = processes.Value("i", 1)
    robot_communication = processes.Process(name="Serial", target=processes.serial_worker, args=(run, Robo_serial))
    robot_vision = processes.Process(name="Vision", target=processes.vision_worker, args=(run, Robo_serial))
    robot_vision.start()
    robot_communication.start()

    return run, robot_communication, robot_vision



if __name__ == "__main__":

    try:
        print(RoboSerial.available_ports())
        
        portname = "ttyACM0"
        
        Robo_serial = RoboSerial("ttyACM0", "utf-8")
        print("Start: ", id(Robo_serial))
    except:
        print("except")

    run, robot_communication, robot_vision = start_processes(Robo_serial)

    
    
    while True:
        print("main",imageprocessing.stop())

        if imageprocessing.stop():
            robot_vision.Close()
            robot_communication.Close()
            exit()
        input()
        
        run.value = not run.value
        print("Running: ", run.value)
        
            


