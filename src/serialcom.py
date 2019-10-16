import serial
import serial.tools.list_ports
import multiprocessing
import time

class RoboSerial():

	def __init__(self, portname, encoding, name, field, working):
		multiprocessing.Process.__init__(self)
		self.ser = serial.Serial(f"/dev/{portname}", 115200, timeout=0.01)
		self.name = name.upper()
		self.field = field.upper()
		self.encoding = encoding
		self.speeds = [0, 0, 0]
		# working == are we at competition
		self.working = not working
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

		self.ser.write(to_send.encode(self.encoding))
		#r = self.ser.readline()
		#print("response from send_speeds: ", r)
		#self.ser.flush()
		#self.ser.reset_input_buffer()
		#r = self.ser.read(20)
		#print(r, "rrrrr")
		#self.ser.flush()
		
		#print(r)
		

	def start_throw(self, stop):
		
		#print("olen start_throwis")
		
		self.ser.write("fs:0\n".encode(self.encoding))
		#failsafe_init = self.ser.read(20)
		
		if not stop:
			time.sleep(0.001)
			self.ser.write("d:180\n".encode(self.encoding)) # 2.5 m / 2.7 tilted up

			print("wrote d:150")
			#print(f"throw speed response: {read_throw_speed_response}")
		else:
			self.ser.write("d:100\n".encode(self.encoding))
			#print("wrote d:100")
			time.sleep(0.001)
			self.ser.write("fs:1\n".encode(self.encoding))
			#print(f"throw stop response: {read_thow_stop_response}")
		

	def refereeHandler(self):
		
		received = self.ser.readline().decode(self.encoding)
		self.ser.flush()
		if len(received) != 19:
			return
		first_letter = received[5]
		field_name = received[6]
		robot_name = received[7]
		print(first_letter, field_name, robot_name) 
		print("RECEIVED LENGTH: ", len(received), " String: ", received)
		
		if first_letter != 'a':
			return
		
		if field_name == self.field:
			if robot_name == "X" or robot_name == self.name:
				command = received[8:11]
				print(command, "command")
				if command == "STO":
					self.working = False
					self.ser.write(f"rf:a{self.field}{self.name}ACK-----\n".encode(self.encoding))
					
					print("REFEREE: STOP RECEIVED") 
				elif command == "STA":
					self.working = True
					self.ser.write(f"rf:a{self.field}{self.name}ACK-----\n".encode(self.encoding))
					
					print("REFEREE: START RECEIVED") 
				elif command == "PIN":
					self.ser.write(f"rf:a{self.field}{self.name}ACK-----\n".encode(self.encoding))
					
					print("REFEREE: PING RECEIVED") 
		

	@staticmethod
	def available_ports():	
		ports = serial.tools.list_ports.comports()
		for port in ports:
			print(port)

if __name__ == "__main__":
	RoboSerial.available_ports()
