from multiprocessing import Process, Value
import time

def worker1(run):
    while 1:
        if run.value:
            threadedprocess1()

def threadedprocess1():
    print("im threaded 1")
    time.sleep(1)

def worker2(run):
    while 1:
        if run.value:
            threadedprocess2()

def threadedprocess2():
    print("im threaded 2")
    time.sleep(1)

if __name__ == "__main__":
    run = Value("i", 1)
    p1 = Process(name = "p1", target = worker1, args=(run,))
    p2 = Process(name = "p2", target = worker2, args=(run,))
    p1.start()
    p2.start()
    while 1:
        input()
        run.value = not run.value
        print("Running: ", run.value)


