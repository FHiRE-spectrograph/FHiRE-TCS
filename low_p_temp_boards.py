import numpy as np
import time, math
import spidev
import RPi.GPIO as GPIO

# intialize SPI communication 
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 3
spi.no_cs #set false or true? false = manually control spi devices cs. error. Doesn't seem to do anything.

class LP:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)

		GPIO_pins = [11,12,13,15,16,18,22,38] #CS 2-7,1,8

		#Relay:[CS GPIO - board,pin]
		#relay2={21:[38,1],22:[38,2],23:[11,1],24:[11,2],25:[12,1],26:[12,2]}

		#Setup all CS pins and hold high
		for x in GPIO_pins:
			GPIO.setup(x,GPIO.OUT)
			GPIO.output(x,GPIO.HIGH)

		for x in GPIO_pins:
			self.Initialize(x)
			self.Setup(x)

		print "AD7124-8 setup complete"

	def Initialize(self, board):
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
		self.commands(board,[0x21,0x00,0x60,0x18]) #Setup filter_0 - default

	def getTemp(self,sensor):
		sensor += 1

		#Sensor designations = {sensor#:[CS,pin1,calibration value,board string]}
		s = {1:[22,10,None,'1-1'],2:[22,4,None,'1-2'],3:[22,6,None,'1-3'],4:[22,8,None,'1-4']
		,5:[22,0,None,'1-5'],6:[22,12,None,'1-6'],7:[22,14,None,'1-7']
		,8:[11,0,None,'2-1'],9:[11,4,None,'2-2'],10:[11,6,None,'2-3'],11:[11,8,None,'2-4']
		,12:[11,10,None,'2-5'],13:[11,12,None,'2-6'],14:[11,14,None,'2-7']
		,15:[12,0,None,'3-1'],16:[12,4,None,'3-2'],17:[12,6,None,'3-3'],18:[12,8,None,'3-4']
		,19:[12,10,None,'3-5'],20:[12,12,None,'3-6'],21:[12,14,None,'3-7']
		,22:[13,0,None,'4-1'],23:[13,2,None,'4-2'],24:[13,4,None,'4-3'],25:[13,6,None,'4-4']
		,26:[13,8,None,'4-5']
		,30:[15,0,None,'5-1'],31:[15,2,None,'5-2'],32:[15,4,None,'5-3'],33:[15,6,None,'5-4']
		,34:[15,8,None,'5-5'],35:[15,10,None,'5-6'],36:[15,12,None,'5-7'],37:[15,14,None,'5-8']
		,38:[16,0,None,'6-1'],39:[16,2,None,'6-2'],40:[16,4,None,'6-3'],41:[16,6,None,'6-4']
		,42:[16,8,None,'6-5'],43:[16,10,None,'6-6'],44:[16,12,None,'6-7'],45:[16,14,None,'6-8']
		,46:[18,0,None,'7-1'],47:[18,2,None,'7-2'],48:[18,4,None,'7-3'],49:[18,6,None,'7-4']
		,50:[18,8,None,'7-5'],51:[18,10,None,'7-6'],52:[18,12,None,'7-7'],53:[18,14,None,'7-8']
		,54:[38,0,None,'8-1'],55:[38,2,None,'8-2']}

		diodes = [1,3,5,7,8,10,12,14,15,17,19,21
				,22,24,26,31,33,34,36,38,40,41,43,45,47,49,51,54]
		resistors = [2,4,6,9,11,13,16,18,20
				,23,25,30,32,35,37,39,42,44,46,48,50,52,53,55]

		board = s[sensor][0]; pin1 = s[sensor][1]; pin2 = pin1 + 1

		conf = {0:0x0,1:0x1,2:0x2,3:0x3,4:0x4,5:0x5,6:0x6,7:0x7,8:0x8,9:0x9,
			10:0xA,11:0xB,12:0xC,13:0xD,14:0xE,15:0xF}

		Iout = conf[pin1]; Vin = conf[pin2]

		self.commands(board,[0x09,0x80|(Vin>>3),0x13|(Vin<<5 & 0xFF)]) #Setup channel_0 - AINP=pin2, AINM=DGND
		self.commands(board,[0x03,0x00,0x01,Iout]) #Setup Iout - Iout0 50microA on pin1

		self.commands(board,[0x01,0x02,0xc4]) #ADC_CONTROL - update to single conversion - begins conversion

		print("Sensor %s -----------" %sensor)
		while True:
			time.sleep(0.1)
			status = self.commands(board,[0x40])
			if status[0]&0x40 == 0x40:
				print("LP ADC ERROR - checking error register")
				print("Error: %s" %self.commands(board,[0x46]))

			elif status[0]&0x80 != 0x80:
				time.sleep(0.01)
				data = self.commands(board,[0x42])
				if data[0] | data[1] | data[2] == 0:
					print("***** ZERO VALUE ERROR *****")
				elif data == [0xFF,0xFF,0xFF]:
					print("***** Sensor N/C ERROR *****")
				break

		self.commands(board,[0x03,0x00,0x00,0x00]) #Turn off Iout

		data = data[2]+(data[1]<<8)+(data[0]<<16)

		if sensor in resistors:
			r = [31.3231717,2.20213448,1.66482204e-3,-3.98620116e-6,4.74888650e-9,
				7.27263261e-12,-2.80325700e-14,3.11300149e-17,-1.22123964e-20] 

			R = data*2.5/(2**(24)*50e-6)
			V = data*2.5/(2**(24))
			print("Voltage: %.7s V" %V)
			print("Resistance: %.7s Ohms" %R)

			polyR = np.polynomial.Chebyshev(r)
			output = polyR(R)-273.15
			print("Temperature: %.5s C" %(polyR(R)-273.15))

		elif sensor in diodes:	
			d = [2.06215201e4,-3.72240694e4,2.81733106e4,-1.78708069e4,9.20412215e3,
				-3.73253855e3,1.12440290e3,-2.25464342e2,22.4784626]

			#R = data*2.5/(2**(24)*50e-6)
			V = data*2.5/(2**(24))
			print("Voltage: %.7s V" %V)
			#print("Resistance: %.7s Ohms" %R)

			polyD = np.polynomial.Chebyshev(d)
			output = polyD(V)-273.15
			print("Temperature: %.5s C" %(polyD(V)-273.15))

		error = self.commands(board,[0x46])
		if error[0] | error[1] | error[2] == 0:
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

#======================================================================#
#    Relay toggle
#======================================================================#

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

		self.commands(board,[0x03,P|S]) #might work 



	
