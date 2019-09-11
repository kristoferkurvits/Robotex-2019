import serial
import serial.tools.list_ports

class RoboSerial():

	def __init__(self, portname, encoding):
		self.ser = serial.Serial(f"/dev/{portname}", 115200, timeout=0.01)
		self.encoding = encoding
		self.speeds = [0, 0, 0]
		print("Serial configured")

	def test_serial(self):
		self.ser.write("gs\n".encode(self.encoding))
		r = self.ser.read(20)
		print("Test message response: ", r)

	def set_speeds(self, speeds):
		if len(speeds) != 3:
			print("Not enough args")
			return
		self.speeds = speeds

	def send_speeds(self):
		speed1, speed2, speed3 = self.speeds
		to_send = f"sd:{speed1}:{speed2}:{speed3}\n"
		self.ser.write(to_send.encode(self.encoding))
		r = self.ser.read(20)
		print(r)

	@staticmethod
	def available_ports():
		ports = serial.tools.list_ports.comports()
		for port in ports:
			print(port)

if __name__ == "__main__":
	RoboSerial.available_ports()