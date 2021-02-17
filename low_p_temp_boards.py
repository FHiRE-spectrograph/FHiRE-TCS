import numpy as np
import time, math
import spidev
import RPi.GPIO as GPIO

# intialize SPI communication 
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 3
spi.no_cs=False #set false or true? false = manually control spi devices cs. error. Doesn't seem to do anything.

class LP:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)

		#GPIO_pins=[11,12,13,15,16,18] #CS 1-7
		GPIO_pins = [11,12]

		#Relay:[CS GPIO - board,pin]
		#relay2={21:[38,1],22:[38,2],23:[11,1],24:[11,2],25:[12,1],26:[12,2]}

		#Setup all CS pins and hold high
		for x in GPIO_pins:
			GPIO.setup(x,GPIO.OUT)
			GPIO.output(x,GPIO.HIGH)

		for x in GPIO_pins:
			self.Initialize(x)
			self.Setup(x)

		#self.Initialize(11)
		#self.Setup(11)

		#self.Initialize(12)
		#self.Setup(12)

		print "AD7124-8 setup complete"

	def Initialize(self, board):
		print("Initializing")

		#Reset ADC
		reset = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF] #Reset w/ 64 consecutive 1s
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(reset)
		time.sleep(0.1) #Could rest for 1ms?
		GPIO.output(board,GPIO.HIGH)

		#Check ID register
		ID = self.commands(board,[0x45])
		if ID[0] != 0x14:
			print("** ADC reset failed (board GPIO %s)- bad ID: %s " %(board,ID))

		#Read status register twice
		self.commands(board,[0x40])
		status = self.commands(board,[0x40])
		if status[0] != 0x80:
			print("** ADC reset failed (board GPIO %s)- bad Status: %s " %(board,status))

		print("Initialization complete (board GPIO %s)" %board)

	def Setup(self, board):
		self.commands(board,[0x19,0x00,0x00]) #Setup config_0 - unipolar, ref=ext.ref1, no buffers, PGA=0
		#self.commands(board,[0x19,0x00,0x18])
		self.commands(board,[0x21,0x00,0x60,0x18]) #Setup filter_0 - default
		#self.commands(board,[0x01,0x00,0x08]) #Setup ADC_CONTROL - standby mode
		self.commands(board,[0x07,0x03,0xF0,0x38]) #Setup error register 

	def getTemp(self,sensor):
		sensor += 1
		#sensor = 19

		s = {1:[11,0,None,'1-1'],2:[11,2,None,'1-2'],3:[11,2,None,'1-3'],4:[11,3,None,'1-4']
		,5:[11,4,None,'1-5'],6:[11,6,None,'1-6'],7:[11,7,None,'1-7'],8:[11,8,None,'1-8']
		,9:[11,9,None,'1-9'],10:[11,10,None,'1-10'],11:[11,11,None,'1-11'],12:[11,12,None,'1-12']
		,13:[11,13,None,'1-13'],14:[11,14,None,'1-14'],15:[12,1,None,'2-1'],16:[12,2,None,'2-2']
		,17:[12,6,None,'2-3'],18:[12,7,None,'2-4'],19:[12,8,None,'2-5'],20:[12,9,None,'2-6']
		,21:[12,10,None,'2-7']}

		diodes = [1,3,5,7,8,10,12,14,15,17,19,21]
		resistors = [2,4,6,9,11,13,16,18,20]

		board = s[sensor][0]; pin1 = s[sensor][1]; pin2 = pin1 + 1

		#conf = IOUT, conf2 = Vin
		conf = {0:0x0,1:0x1,2:0x2,3:0x3,4:0x4,5:0x5,6:0x6,7:0x7,8:0x8,9:0x9,
			10:0xA,11:0xB,12:0xC,13:0xD,14:0xE,15:0xF}

		Iout = conf[pin1]; Vin = conf[pin1]

		if sensor in [3,4]:
			return 0
		elif sensor in [1,2]:
			Iout = conf[pin2]
		elif sensor in [16,17,18,19]:
			Iout = 0x0
			#self.commands(board,[0x03,0x00,0x06,0x0])
			mult = 1


		self.commands(board,[0x09,0x80|(Vin>>3),0x05|(Vin<<5 & 0xFF)]) #Setup channel_0 - AINP=pin1, AINM=AIN5

		self.commands(board,[0x03,0x00,0x04,Iout]) #Setup Iout - Iout0 500microA on pin1

		self.commands(board,[0x01,0x02,0x04]) #ADC_CONTROL - update to single conversion - begins conversion

		print("Sensor %s --------" %sensor)
		while True:
			time.sleep(0.1)
			status = self.commands(board,[0x40])
			print("Status: %s" %status)
			if status[0]&0x40 == 0x40:
				print("LP ADC ERROR - checking error register")
				print("Error: %s" %self.commands(board,[0x46]))

			elif status[0]&0x80 != 0x80:
				time.sleep(0.01)
				data = self.commands(board,[0x42])
				print("Data: %s" %data)
				if data[0] | data[1] | data[2] == 0:
					print("***** ZERO VALUE ERROR *****")
				elif data == [0xFF,0xFF,0xFF]:
					print("***** Sensor N/C ERROR *****")
				break

		self.commands(board,[0x03,0x00,0x00,0x00]) #Turn off Iout - 500 microA AIN3

		data = data[2]+(data[1]<<8)+(data[0]<<16)

		if sensor in resistors:
			r = [31.3231717,2.20213448,1.66482204e-3,-3.98620116e-6,4.74888650e-9,
				7.27263261e-12,-2.80325700e-14,3.11300149e-17,-1.22123964e-20] 

			R = data*2.5/(2**(24)*500e-6)
			V = data*2.5/(2**(24))
			print("Voltage: %.7s V" %V)
			print("Resistance: %.7s Ohms" %R)

			polyR = np.polynomial.Chebyshev(r)
			output = polyR(R)-273.15
			print("Temperature: %.5s C" %(polyR(R)-273.15))
			#output = V

		elif sensor in diodes:	
			d = [2.06215201e4,-3.72240694e4,2.81733106e4,-1.78708069e4,9.20412215e3,
				-3.73253855e3,1.12440290e3,-2.25464342e2,22.4784626]
			#d = [5.50407261e2, -6.96091175e-3, 1.11679275e-7, -2.36461493e-12, 2.90727397e-17, 					-2.15428815e-22, 9.44575204e-28, -2.25464342e-33, 2.24784626e-39]

			R = data*2.5/(2**(24)*500e-6)
			V = data*2.5/(2**(24))
			print("Voltage: %.7s V" %V)
			print("Resistance: %.7s Ohms" %R)

			polyD = np.polynomial.Chebyshev(d)
			output = polyD(V)-273.15
			print("Temperature: %.5s C" %(polyD(V)-273.15))
			#output = V

		error = self.commands(board,[0x46])
		if error[0] | error[1] | error[2] == 0:
			#print("No errors - keep data")
			return output
		else:
			print("Error - throwing out data")
			print("Error: %s" %error)
			return 11111

	#Send a command to AD7124-8 boards - board/CS, byte command
	def commands(self, board, cmd):
		time.sleep(0.05)
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(cmd)
		
		if cmd[0] & 0x40 == 0x40:
			data = spi.readbytes(3)
			GPIO.output(board,GPIO.HIGH)
			return data
		else:
			GPIO.output(board,GPIO.HIGH)

#======================#
#    Relay toggle
#======================#

	def check_status(self,board,pin):
		status = self.commands(board,[0x43])

		if pin == 1: #Check if pin 2 is ON/OFF
			if status & 0x220000 == 0x220000: #OFF
				#print('P2 kept OFF')
				return 0x220000
			elif status & 0x020000 == 0x020000: #ON
				#print('P2 kept ON')
				return 0x020000

		elif pin == 2: #Check if pin 1 is ON/OFF
			if status & 0x110000 == 0x110000: #OFF
				#print('P1 kept OFF')
				return 0x110000
			elif status & 0x010000 == 0x010000: #ON
				#print('P1 kept ON')
				return 0x010000
		return 0x0

	#board=CS GPIO pin -- toggle relay 
	def Relay_ON(self, ind): 
		board = relay2[ind][0]
		pin = relay2[ind][1]

		if pin == 1:
			#print('P1 turning ON')
			P = 0x010000 #P1/AIN2 - IO_CONTROL_1
		elif pin == 2:
			#print('P2 turning ON')
			P = 0x020000 #P2/AIN3 - IO_CONTROL_1
		
		S = self.check_status(board,pin)

		#self.commands(board,0x03,'w',P|S,24) #Write IO_Control_1 register: pin=low	
		self.commands(board,[0x03,P|S]) #might work 

	def Relay_OFF(self, ind): 
		board = relay2[ind][0]
		pin = relay2[ind][1]

		if pin == 1:
			#print('P1 turning OFF')
			P = 0x110000 #P1/AIN2 - IO_CONTROL_1
		elif pin == 2:
			#print('P2 turning OFF')
			P = 0x220000 #P2/AIN3 - IO_CONTROL_1

		S = self.check_status(board,pin)

		#self.commands(board,0x03,'w',P|S,24) #Write IO_Control_1 register: pin=high
		self.commands(board,[0x03,P|S]) #might work 



	
