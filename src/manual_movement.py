from robot_movement import calculate_linear_velocity as linear_mvmt

import numpy as np
import keyboard
img = np.zeros((256, 256, 3))


def startManualMovement(Robo_serial):

	while 1:

		if keyboard.is_pressed("w"):
			right = linear_mvmt(40, 120, 90)
			middle = linear_mvmt(40, 0, 90)
			left = linear_mvmt(40, 240, 90)
		elif keyboard.is_pressed("a"):
			right = linear_mvmt(40, 120, 180)
			middle = linear_mvmt(40, 0, 180)
			left = linear_mvmt(40, 240, 180)
		elif keyboard.is_pressed("d"):
			right = linear_mvmt(40, 120, 0)
			middle = linear_mvmt(40, 0, 0)
			left = linear_mvmt(40, 240, 0)
		elif keyboard.is_pressed("s"):
			right = linear_mvmt(40, 120, 270)
			middle = linear_mvmt(40, 0, 270)
			left = linear_mvmt(40, 240, 270)
		elif keyboard.is_pressed("q"):
			right = linear_mvmt(-40, 120, 120)
			middle = linear_mvmt(-40, 0, 0)
			left = linear_mvmt(-40, 240, 240)
		elif keyboard.is_pressed("e"):
			right = linear_mvmt(40, 120, 120)
			middle = linear_mvmt(40, 0, 0)
			left = linear_mvmt(40, 240, 240)
		elif keyboard.is_pressed("j"):
			Robo_serial.start_throw(False)
		elif keyboard.is_pressed("k"):
			Robo_serial.stop_throw(True)

		elif keyboard.is_pressed("b"):
			break
		else:
			continue

		Robo_serial.speeds = [right, middle, left]
		Robo_serial.send_speeds()
	



