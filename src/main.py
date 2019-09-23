import processes
import imageprocessing
from multiprocessing import Process, Value, Manager
from serialcom import RoboSerial
import manual_movement
import keyboard

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
    return run, robot_communication, robot_vision

def choose_movement_method(robot_vision, robot_communication):
    while 1:
        try:
            char = input("SELECT DRIVING MODE - m for manual, n for auto\n")
            if char == "m":
                print("------MANUAL MODE------\n")
                print("------VISION CLOSED------\n")
                #Robo_serial.manipulate_failsafe(True)
                manual_movement.startManualMovement(Robo_serial, processes_variables)
                continue
            elif char == "n":
                print("------AUTO MODE------\n")
                robot_vision.start()
                robot_communication.start()
                #Robo_serial.manipulate_failsafe(False)
                break
            elif char == "q":
                print("q pressed, exiting")
                exit()
            elif char == "b":
                print("b pressed, exiting")
                break
        except Exception as e:
            print("Reached exception in manual/auto...exiting: ", e)
            continue

if __name__ == "__main__":
    print("Available ports: ", RoboSerial.available_ports())
    portname = input("Enter desired port")
    try:
        portname = f"ttyACM{portname}"
        Robo_serial = RoboSerial(portname, "utf-8")
        manager = Manager()
        processes_variables = manager.list([0,0,0,0])

    except Exception as e:
        print("Reached exception in main: ", e)
        exit()
    run, robot_communication, robot_vision = start_processes(Robo_serial, processes_variables)
    choose_movement_method(robot_vision, robot_communication)

    while True:
        input()

        run.value = not run.value
        stop = run.value
        print("Running: ", run.value)
        if stop:
            robot_vision.start()
            robot_communication.start()
        else:
            print("Stop reached")
            robot_vision.close()
            robot_communication.close()
            choose_movement_method(robot_vision, robot_communication)


            

        
        
        
            


