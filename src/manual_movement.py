from robot_movement import calculate_linear_velocity as linear_mvmt
import vision
import cv2
import time
import config
import pyrealsense2 as rs
import numpy as np
import sys, termios, tty, os, time
img = np.zeros((256, 256, 3))
button_delay = 0.2



def getch():

		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)

		finally:

			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

		return ch




def startManualMovement(Robo_serial, processes_variables):
	speed = 40
	while 1:
		
		char = getch()
		print("once")
		if (char == "s"):
			right = linear_mvmt(speed, 120, 90)
			middle = linear_mvmt(speed, 0, 90)
			left = linear_mvmt(speed, 240, 90)
			print("ssssssssssssssssssssssssssssssssssssssssssssss")
		elif (char == "d"):
			right = linear_mvmt(speed, 120, 180)
			middle = linear_mvmt(speed, 0, 180)
			left = linear_mvmt(speed, 240, 180)
			print("dddddddddddddddddddddddddddddddddddddddddddddd")
		elif (char == "a"):
			right = linear_mvmt(speed, 120, 0)
			middle = linear_mvmt(speed, 0, 0)
			left = linear_mvmt(speed, 240, 0)
			print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
		elif (char == "w"):
			right = linear_mvmt(speed, 120, 270)
			middle = linear_mvmt(speed, 0, 270)
			left = linear_mvmt(speed, 240, 270)
			print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
		elif (char == "q"):
			right = linear_mvmt(-speed, 120, 120)
			middle = linear_mvmt(-speed, 0, 0)
			left = linear_mvmt(-speed, 240, 240)
		elif (char == "e"):
			right = linear_mvmt(speed, 120, 120)
			middle = linear_mvmt(speed, 0, 0)
			left = linear_mvmt(speed, 240, 240)
		elif (char == "j"):
			print("-----------------------------")
			Robo_serial.start_throw(False) 

		elif (char == "k"):
			Robo_serial.start_throw(True)

		elif (char == "b"):
			print("Break reached in manual movement...breaking")
			break
		else:
			left = 0
			right = 0
			middle = 0
		
		time.sleep(0.01)
		Robo_serial.speeds = [right, middle, left]
		Robo_serial.send_speeds()
		print("tere")

		
	pipeline.stop()
	cv2.destroyAllWindows()
    




