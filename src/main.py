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
    robot_vision.start()
    robot_communication.start()

    return run, robot_communication, robot_vision

if __name__ == "__main__":
    getOut = False

    try:
        print("Available ports: ", RoboSerial.available_ports())
        portname = "ttyACM1"
        Robo_serial = RoboSerial(portname, "utf-8")
        manager = Manager()
        processes_variables = manager.list([0,0,0,0])

    except Exception as e:
        print("Available ports: ", RoboSerial.available_ports())
        portname = "ttyACM1"
        Robo_serial = RoboSerial(portname, "utf-8")
        manager = Manager()
        processes_variables = manager.list([0, 0, 0, 0])
        print("Reached exception in main: ", e)
        exit()

    
        print("SELECT DRIVING MODE - m for manual, n for auto")
        char = manual_movement.getch()

        try:
            while not getOut:
                
                if char == "m":
                    print("------MANUAL MODE------\n")

                    print("------VISION CLOSED------\n")
                    #Robo_serial.manipulate_failsafe(True)
                    manual_movement.startManualMovement(Robo_serial, processes_variables)
                    getOut = True
                elif char == "n":
                    print("------AUTO MODE------\n")
                    run, robot_communication, robot_vision = start_processes(Robo_serial, processes_variables)
                    #Robo_serial.manipulate_failsafe(False)
                    getOut = True
        except:
            exit()

        """
        if manual_movement.getch() == "s":
            print("TAHAN SWITCHIDA")
            getOut = False

            robot_vision.close()
            robot_communication.close()
        """


        """
        char = manual_movement.getch()
        if char == "s":
            try:
                processes_variables[3] = 1
                print(processes_variables[3], "PROCESSES VARIABLES 3")
                getOut = False
            except Exception as e:
                print(e, "ERRRRRRRRRRRRRRRRRRROR")
        """

        while True:

            #stop = processes_variables[3]

            input()

            run.value = not run.value
            stop = run.value
            print("Running: ", run.value)

            if stop:
                robot_vision.close()
                robot_communication.close()
                exit()

            

        
        
        
            


