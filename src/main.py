import processes
import imageprocessing
from multiprocessing import Process, Value, Manager
from serialcom import RoboSerial

"""
    function start processes
    args:
        1)Robo serial - serial object which communicates with the mainboard
        2)Process variables - contains the speeds for the mainboard motors + stopping signal
            needed for interprocess communication
    returns:
        1)run - value to signal whether a process should pause
        2)robot_communication - returns the serial communication process (to close it if we need to)
        3)robot_vision - returns the vision process (to close it if we need to)
"""



def start_processes(Robo_serial, process_variables):
    

    run = processes.Value("i", 1)
    robot_communication = processes.Process(name="Serial", target=processes.serial_worker, args=(run, Robo_serial, process_variables))
    robot_vision = processes.Process(name="Vision", target=processes.vision_worker, args=(run, process_variables))
    robot_vision.start()
    robot_communication.start()

    return run, robot_communication, robot_vision

if __name__ == "__main__":

    try:
        print("Available ports: ", RoboSerial.available_ports())
        portname = "ttyACM0"
        Robo_serial = RoboSerial(portname, "utf-8")
        manager = Manager()
        processes_variables = manager.list([0,0,0,0])
        run, robot_communication, robot_vision = start_processes(Robo_serial, processes_variables)

    except Exception as e:
        print("Reached exception in main: ", e)
        exit()

    while True:

        stop = processes_variables[3]
        if stop:
            robot_vision.close()
            robot_communication.close()
            exit()

        input("Press any key to pause" if run.value else "Press any key to continue")
        run.value = not run.value
        stop = run.value
        print("Running: ", run.value)
        
            


