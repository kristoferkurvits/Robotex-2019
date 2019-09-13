import serial
import time





ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)

while 1:
	moving_cmd = input("3 numbers, split by space: ")
	moving_cmd = moving_cmd.split(" ")

	if len(moving_cmd) != 3:
		print("Not enough args")
		continue
	while 1:
		to_send = f"sd:{moving_cmd[0]}:{moving_cmd[1]}:{moving_cmd[2]}"
		ser.write(to_send.encode())
		time.sleep(0.01)
		s = ser.read(100)
		print("Received: ", s)