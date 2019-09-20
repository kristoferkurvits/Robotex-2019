from robot_movement import calculate_linear_velocity as linear_mvmt
from serialcom import RoboSerial
import cv2
import numpy as np
img = np.zeros((256, 256, 3))
ser = RoboSerial("ttyACM0", "utf-8")

while 1:
	ser.available_ports()
	cv2.imshow("img", img)
	key = cv2.waitKey(50)
	if key & 0xFF == ord('w'):
		right = linear_mvmt(40, 120, 90)
		middle = linear_mvmt(40, 0, 90)
		left = linear_mvmt(40, 240, 90)
	elif key & 0xFF == ord('a'):
		right = linear_mvmt(40, 120, 180)
		middle = linear_mvmt(40, 0, 180)
		left = linear_mvmt(40, 240, 180)
	elif key & 0xFF == ord('d'):
		right = linear_mvmt(40, 120, 0)
		middle = linear_mvmt(40, 0, 0)
		left = linear_mvmt(40, 240, 0)
	elif key & 0xFF  == ord('s'):
		right = linear_mvmt(40, 120, 270)
		middle = linear_mvmt(40, 0, 270)
		left = linear_mvmt(40, 240, 270)
	elif key & 0xFF  == ord('q'):
		right = linear_mvmt(-40, 120, 120)
		middle = linear_mvmt(-40, 0, 0)
		left = linear_mvmt(-40, 240, 240)
	elif key & 0xFF  == ord('e'):
		right = linear_mvmt(40, 120, 120)
		middle = linear_mvmt(40, 0, 0)
		left = linear_mvmt(40, 240, 240)
	elif key & 0xFF == ord('b'):
		cv2.destroyAllWindows()
		ser.ser.close()
		break
	else:
		continue
	ser.speeds = [right, middle, left]
	ser.send_speeds()


