from robot_movement import calculate_linear_velocity as linear_mvmt

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

	while 1:
		char = getch()

		if (char == "s"):
			right = linear_mvmt(40, 120, 90)
			middle = linear_mvmt(40, 0, 90)
			left = linear_mvmt(40, 240, 90)
			print("ssssssssssssssssssssssssssssssssssssssssssssss")
		elif (char == "d"):
			right = linear_mvmt(40, 120, 180)
			middle = linear_mvmt(40, 0, 180)
			left = linear_mvmt(40, 240, 180)
			print("dddddddddddddddddddddddddddddddddddddddddddddd")
		elif (char == "a"):
			right = linear_mvmt(40, 120, 0)
			middle = linear_mvmt(40, 0, 0)
			left = linear_mvmt(40, 240, 0)
			print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
		elif (char == "w"):
			right = linear_mvmt(40, 120, 270)
			middle = linear_mvmt(40, 0, 270)
			left = linear_mvmt(40, 240, 270)
			print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
		elif (char == "q"):
			right = linear_mvmt(-40, 120, 120)
			middle = linear_mvmt(-40, 0, 0)
			left = linear_mvmt(-40, 240, 240)
		elif (char == "e"):
			right = linear_mvmt(40, 120, 120)
			middle = linear_mvmt(40, 0, 0)
			left = linear_mvmt(40, 240, 240)
		elif (char == "j"):
			Robo_serial.start_throw(False) 
		elif (char == "k"):
			Robo_serial.start_throw(True)

		elif (char == "b"):

			break
		else:
			continue
		"""
		ei tööta
		processes_variables[0] = right
		processes_variables[1] = middle
		processes_variables[2] = left
		print(processes_variables[0], processes_variables[1], processes_variables[2], "##########################")
		"""

		Robo_serial.speeds = [right, middle, left]
		Robo_serial.send_speeds()
		print("tere")
		



