import serial
import time

serial_port = input("enter serial")

ser = serial.Serial(f'/dev/tty{serial_port}', 115200, timeout=0)
ser.write("gs".encode("utf-8"))
r = ser.read(10)
print("Received: ", r)
while 1:
	moving_cmd = input("3 numbers, split by space: ")
	moving_cmd = moving_cmd.split(" ")

	if len(moving_cmd) != 3:
		print("Not enough args")
		continue
	while 1:
		to_send = f"sd:{moving_cmd[0]}:{moving_cmd[1]}:{moving_cmd[2]}\n"
		ser.write(to_send.encode("utf-8"))
		s = ser.read(10)
		print("Received: ", s)
	


