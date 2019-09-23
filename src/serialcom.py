import serial
import serial.tools.list_ports
import multiprocessing
import time

class RoboSerial():

	def __init__(self, portname, encoding):
		multiprocessing.Process.__init__(self)
		self.ser = serial.Serial(f"/dev/{portname}", 115200, timeout=0.01)
		self.encoding = encoding
		self.speeds = [0, 0, 0]

		print("Serial configured.")

	def test_serial(self):
		self.ser.write("gs\n".encode(self.encoding))
		r = self.ser.read(20)
		print("Test message response: ", r)

	def manipulate_failsafe(self, stop):
		if not stop:
			self.ser.write("fs:1")
			print("failsafe enabled")
		else:
			self.ser.write("fs:0")
			print("failsafe disabled")


	def send_speeds(self):

		speed1, speed2, speed3 = self.speeds
		to_send = f"sd:{speed1}:{speed2}:{speed3}\n"
		print(to_send, "TOSEND")
		self.ser.write(to_send.encode(self.encoding))
		r = self.ser.read(20)
		print(r, "RESPONSEEEE")
	
	def start_throw(self, stop):
		
		print("olen start_throwis")
		"""
		self.ser.write("fs:0\n".encode(encoding))
		failsafe_init = self.ser.read(20)
		"""
		if not stop:
			self.ser.write("d:210\n".encode(self.encoding))
			print("wrote d:210")
			read_throw_speed_response = self.ser.read(20)
			print(f"throw speed response: {read_throw_speed_response}")
		else:
			self.ser.write("d:100\n".encode(self.encoding))
			print("wrote d:100")
			read_thow_stop_response = self.ser.read(20)
			print(f"throw stop response: {read_thow_stop_response}")
		
		

	@staticmethod
	def available_ports():
		ports = serial.tools.list_ports.comports()
		for port in ports:
			print(port)

if __name__ == "__main__":
	RoboSerial.available_ports()
