import numpy as np
import time, math
import spidev
import RPi.GPIO as GPIO

# Intialize SPI communication.
spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode = 3

# Set false or true? false = manually control spi devices cs. error. 
# Doesn't seem to do anything.
spi.no_cs  

class LP:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)

		# Setup the 6 relays attached to LP boards 1-3.
		# Relay number:[CS GPIO/board, analog pin]
		self.relay={21:[22,1], 22:[22,2], 23:[11,1], 24:[11,2], 
			    25:[12,1], 26:[12,2]}
		self.relayStatus = 0x030000  # enables GPIO pins for boards 1-3

		# Setup all Clock Select pins and hold high.
		GPIO_pins = [11, 12, 13, 15, 16, 18, 22, 38]  # CS 2-7,1,8
		for x in GPIO_pins:
			GPIO.setup(x, GPIO.OUT)
			GPIO.output(x, GPIO.HIGH)
			print("LP Board: %s pin setup" %x)

		for x in GPIO_pins:
			self.Initialize(x)
			self.Setup(x)

		print("AD7124-8 setup complete")

	def Initialize(self, board):
		# Reset ADC by sending 64 consecutive 1s to the LP board.
		reset = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
		GPIO.output(board, GPIO.LOW)
		spi.writebytes(reset)
		time.sleep(0.01)  # Could rest for 1ms?
		GPIO.output(board, GPIO.HIGH)

		# Check ID register.
		ID = self.commands(board, [0x45])
		if ID[0] != 0x14:
			print("** ADC reset failed (board GPIO %s)- bad ID: %s " 
			      %(board, ID))

		# Read status register twice.
		for x in range(2):
			status = self.commands(board, [0x40])
			print(status)
			if status[0]&0x80 != 0x80:
				print("** ADC reset failed (board GPIO %s)"
				      "- bad Status: %s " %(board, status))

		print("Initialization complete (board GPIO %s)" %board)

	def Setup(self, board):
		# Setup config_0 - unipolar, int ref, no buffers, gain=2
		self.commands(board, [0x19,0x00,0x11])  
		# Setup filter_0 - default *Sets status reg to 0 ?*
		#self.commands(board, [0x21,0x00,0x60,0x18])  

		#self.commands(board, [0x09,0x80|(0x08>>3),0x13|(0x08<<5 & 0xFF)])
		#self.commands(board, [0x03,0x00,0x01,0x09])

	def getTemp(self, sensor):
		# Sensor designations = {sensor#: [CS,pin1,calibration value,board string]}
		s = {
			1:[22,0,0.6433,'1-1'],   2:[22,4,106.77,'1-2'],   
			3:[22,6,0.6432,'1-3'],   4:[22,8,106.9,'1-4'],
   			5:[22,10,0.0535,'1-5'],  6:[22,12,106.9,'1-6'],
			7:[22,14,0.6438,'1-7'],  8:[11,0,0.6428,'2-1'],
			9:[11,4,107.95,'2-2'],   10:[11,6,0.6453,'2-3'], 
			11:[11,8,108.04,'2-4'],  12:[11,10,0.6427,'2-5'],
			13:[11,12,108.08,'2-6'], 14:[11,14,0.6427,'2-7'], 
			15:[12,0,0.6426,'3-1'],  16:[12,4,109.94,'3-2'],  
			17:[12,6,0.6460,'3-3'],  18:[12,8,110.05,'3-4'],
			19:[12,10,0.6455,'3-5'], 20:[12,12,110.12,'3-6'], 
			21:[12,14,0.6459,'3-7'], 22:[13,0,0.6443,'4-1'],  
			23:[13,2,111.09,'4-2'],  24:[13,4,0.6445,'4-3'],
			25:[13,6,111.12,'4-4'],  26:[13,8,0.6460,'4-5'],  
			27:[13,10,0.6870,'4-6'], 28:[13,12,0.6885,'4-7'], 
			29:[13,14,0.6862,'4-8'], 30:[15,0,111.2,'5-1'],
			31:[15,2,0.6451,'5-2'],  32:[15,4,111.15,'5-3'],  
			33:[15,6,0.6469,'5-4'],  34:[15,8,0.6441,'5-5'],  
			35:[15,10,111.80,'5-6'], 36:[15,12,0.6430,'5-7'],
			37:[15,14,111.08,'5-8'], 38:[16,0,0.6449,'6-1'],
			39:[16,2,112.40,'6-2'],  40:[16,4,0.6458,'6-3'],
			41:[16,6,0.6445,'6-4'],  42:[16,8,112.27,'6-5'],
			43:[16,10,0.6452,'6-6'], 44:[16,12,112.33,'6-7'], 
			45:[16,14,0.6452,'6-8'], 46:[18,0,110.2,'7-1'],
			47:[18,2,0.6442,'7-2'],  48:[18,4,110.29,'7-3'],
			49:[18,6,0.6443,'7-4'],  50:[18,8,110.0,'7-5'],
			51:[18,10,0.6448,'7-6'], 52:[18,12,110.1,'7-7'],
			53:[18,14,110.3,'7-8'],  54:[38,0,0.6473,'8-1'],
			55:[38,2,109.58,'8-2'],  56:[38,4,0.6881,'8-3'],
			57:[38,6,0.6876,'8-4'],  58:[38,8,0.6864,'8-5'],
			59:[38,10,0.6854,'8-6'], 60:[38,12,0.6850,'8-7ncal'],
			61:[38,14,0.6872,'8-8']}

		diodes = [
			1, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 21,
			22, 24, 26, 31, 33, 34, 36, 38, 40, 41, 
			43, 45, 47, 49, 51, 54, 27, 28, 29, 56, 
			57, 58, 59, 60, 61]

		resistors = [
			2, 4, 6, 9, 11, 13, 16, 18, 20, 23, 25, 30, 
			32, 35, 37, 39, 42, 44, 46, 48, 50, 52, 53, 55]

		board = s[sensor][0]; pin1 = s[sensor][1]; pin2 = pin1 + 1

		conf = {
			0:0x0, 1:0x1, 2:0x2, 3:0x3, 4:0x4, 5:0x5, 6:0x6,
			7:0x7, 8:0x8, 9:0x9, 10:0xA, 11:0xB, 12:0xC, 13:0xD,
			14:0xE, 15:0xF}

		Iout = conf[pin2]; Vin = conf[pin1]

		# Setup channel_0 - AINP=pin2, AINM=DGND.
		self.commands(board, [0x09,0x80|(Vin>>3),0x13|(Vin<<5 & 0xFF)])  

		# Setup Iout - Iout 500microA on pin1.
		if board in [22,11,12]:  # GPIO pins enabled for relays
			self.commands(board, [0x03,self.relayStatus,0x04,Iout])
		else:
			self.commands(board, [0x03,0x00,0x04,Iout])

		# Update to single conversion, full power, CS_EN/int Ref=ENABLE.
		self.commands(board, [0x01,0x03,0xc4])  

		print("Sensor %s ------------------------" %sensor)
		n = 0
		while True:
			status = self.commands(board, [0x40])
			if status[0] & 0x40 == 0x40:
				print("LP ADC ERROR - checking error register")
				time.sleep(2)
				print("Error: %s" %self.commands(board, [0x46]))
				# Need to add catch for invalid error reading.
				return 11111
			elif n == 5000:
				print("Timeout error")
				return 11111
			if status[0] & 0x80 != 0x80:	
				data = self.commands(board, [0x42])
				if data[0] | data[1] | data[2] == 0:
					print("***** ZERO VALUE ERROR *****")
					return 11111
				elif data == [0xFF, 0xFF, 0xFF]:
					print("***** Sensor N/C ERROR *****")
				break
			n += 1
			#time.sleep(0.001)

		self.commands(board, [0x03,0x00,0x00,0x00])  # Turn off Iout

		data = data[2] + (data[1] << 8) + (data[0] << 16)

		if sensor in resistors:
			r = [31.3231717, 2.20213448, 1.66482204e-3,
	  		     -3.98620116e-6, 4.74888650e-9, 7.27263261e-12, 
			     -2.80325700e-14, 3.11300149e-17, -1.22123964e-20] 

			R = data *2.5 / (2 ** (24) * 500e-6 * 2)
			V = data *2.5 / (2 ** (24) * 2)
			R = R * 109.391 / s[sensor][2]

			polyR = np.polynomial.Chebyshev(r)
			output = polyR(R) - 273.15
			print("Temperature: %.5s C (%.7s Ohms)" 
			      %((polyR(R) - 273.15), R))

		elif sensor in diodes:	
			d = [2.06215201e4, -3.72240694e4, 2.81733106e4, 
			     -1.78708069e4, 9.20412215e3, -3.73253855e3, 
			     1.12440290e3, -2.25464342e2, 22.4784626]

			V = data * 2.5 / (2 ** (24) * 2)
			# Seperate calibration for external sensors.
			if sensor in [27, 28, 29, 56, 57, 58, 59, 60, 61]:
				#V = V * 0.6212 / s[sensor][2]
				#print(V)
				V = V - (s[sensor][2] - 0.621163)
				#print(V)
			else:
				V = V * 0.5660 / s[sensor][2]

			polyD = np.polynomial.Chebyshev(d)
			output = polyD(V) - 273.15
			print("Temperature: %.5s C (%.7s V)" 
			      %((polyD(V) - 273.15), V))

		error = self.commands(board, [0x46])
		if error[0] | error[1] | error[2] == 0:
			return output
		else:
			print("Error - throwing out data")
			print("Error: %s" %error)
			return 11111

	# Send a command to AD7124-8 boards - board/CS, byte command.
	def commands(self, board, cmd):
		GPIO.output(board, GPIO.LOW)
		spi.writebytes(cmd)
		
		if cmd[0] & 0x40 == 0x40:
			data = spi.readbytes(3)
			GPIO.output(board, GPIO.HIGH)
			return data
		else:
			GPIO.output(board, GPIO.HIGH)

#======================================================================#
#    Relay toggle
#======================================================================#

	# Check current status of IO_registor to make sure that
	# relays that are ON/OFF keep their states with new commands
	def check_status(self, board, pin):
		status = self.commands(board, [0x43])

		if pin == 1:  # Check if pin 2 is ON/OFF
			if status[0] & 0x220000 == 0x220000:  # OFF
				return 0x220000
			elif status[0] & 0x020000 == 0x020000:  # ON
				return 0x020000

		elif pin == 2:  # Check if pin 1 is ON/OFF
			if status[0] & 0x110000 == 0x110000:  # OFF
				return 0x110000
			elif status[0] & 0x010000 == 0x010000:  # ON
				return 0x010000
		return 0x0

	# Toggle relays ON/OFF
	def Relay_ON(self, ind): 
		board = self.relay[ind][0] # CS GPIO pin
		pin = self.relay[ind][1] #AIN1 or AIN2

		if pin == 1:
			P = 0x01  # P1/AIN2 - IO_CONTROL_1
		if pin == 2:
			P = 0x02  # P2/AIN3 - IO_CONTROL_1

		S = self.check_status(board, pin)
		self.relayStatus = P|S	

		self.commands(board, [0x03,self.relayStatus,0x0,0x0]) 

	def Relay_OFF(self, ind): 
		board = self.relay[ind][0]
		pin = self.relay[ind][1]

		if pin == 1:
			P = 0x11  # P1/AIN2 - IO_CONTROL_1
		if pin == 2:
			P = 0x22  # P2/AIN3 - IO_CONTROL_1

		S = self.check_status(board, pin)
		self.relayStatus = P|S

		self.commands(board, [0x03,self.relayStatus,0x0,0x0])  





	
