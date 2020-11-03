import numpy as np
import time, math
import spidev
import RPi.GPIO as GPIO

# intialize SPI communication 
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 3
spi.no_cs=False #set false or true? false = manually control spi devices cs. error. Doesn't seem to do anything.

#Convert decimal/hex to a byte array
def bytes(decimal,bitsize):
	if bitsize == 8:
		x=decimal
 		return [int(x)]
	elif bitsize == 16:
		y=math.floor(decimal*2**(-8))
		x=decimal-y*2**8
		return [int(y),int(x)]
	elif bitsize == 24:
		z=math.floor(decimal*2**(-16))
		d2=decimal-z*2**16
		y=math.floor(d2*2**(-8))
		x=d2-y*2**8
		return [int(z),int(y),int(x)]


#Convert byte array to a decimal
def decimal(b):
	bitsize=len(b)
	if bitsize == 1: #8bit
		decimal=b[0]
	elif bitsize == 2: #16bit
		decimal=b[1]+(b[0]<<8)
	elif bitsize == 3: #24bit
		decimal=b[2]+(b[1]<<8)+(b[0]<<16)
	elif bitsize == 4:
		decimal=b[3]+(b[2]<<8)+(b[1]<<16)+(b[0]<<32)

	return decimal


class LP:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		#GPIO.cleanup()
		GPIO_pins=[11,12,13,15,16,18,22,38] #CS 2-8, 1

		#Setup all CS pins and hold high
		for x in GPIO_pins:
			GPIO.setup(x,GPIO.OUT)
			GPIO.output(x,GPIO.HIGH)

		global read, write, reset, state, relay2

		read = 0x40
		write = 0x00

		#Relay:[CS GPIO - board,pin]
		relay2={21:[38,1],22:[38,2],23:[11,1],24:[11,2],25:[12,1],26:[12,2]}

		#Setup relay boards
		for x in GPIO_pins:
			self.Setup(x)

		print "Setup complete"

	def Setup(self, board):

		#Write to CONFIG_0 register: Unipolar, AVDD=ref, gain=1
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x19,8)) 
		spi.writebytes(bytes(0x18,16)) 
		GPIO.output(board,GPIO.HIGH)

		#Write to FILTER_0 register: default
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x21,8)) 
		spi.writebytes(bytes(0x06018,24)) 
		GPIO.output(board,GPIO.HIGH)

		#Write to ADC_CONTROL register: disable int. voltage, low-power, continuous conversion mode, int. clock source
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x01,8))
		spi.writebytes(bytes(0x0004,16)) 
		GPIO.output(board,GPIO.HIGH)

		#Write to CHANNEL_0 register: conversion=disabled, setup_0, AIN0=pos, AIN0=neg
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x09,8))
		spi.writebytes(bytes(0x8033,16))
		GPIO.output(board,GPIO.HIGH)

#########################################################
# Relay Toggle Methods
#########################################################
	def check_status(self,board,pin):
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(read|0x03,8))
		status = decimal(spi.readbytes(3))
		GPIO.output(board,GPIO.HIGH)

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

		#Write IO_Control_1 register: pin=low	
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x03,8)) 
		spi.writebytes(bytes(P|S,24)) 
		GPIO.output(board,GPIO.HIGH)

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

		#Read IO_Control_1 register: pin=high
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x03,8)) 
		spi.writebytes(bytes(P|S,24)) 
		GPIO.output(board,GPIO.HIGH)


###########################################################
# Read Temperature Method
###########################################################

	def getTemp(self, sensor):
		sensor += 1

		#sensor:[CS GPIO - board,first AIN pin#,resistance at room temp] 29,28,27,61-56 = outside
		s = {1:[38,0,0.5668,'1-1'],2:[38,4,41.4,'1-2'],3:[38,6,0.5662,'1-3'],4:[38,8,0.5431,'1-4'],5:[38,10,107.58,'1-5'],6:[38,12,0.5431,'1-6'],7:[38,14,0.5433,'1-7'],
			8:[11,0,0.5679,'2-1'],9:[11,4,109.2,'2-2'],10:[11,6,0.5436,'2-3'],11:[11,8,109.2,'2-4'],12:[11,10,0.552,'2-5'],13:[11,12,109.4,'2-6'],14:[11,14,0.5447,'2-7'],
			15:[12,0,0.5443,'3-1'],16:[12,4,109.98,'3-2'],17:[12,6,0.5666,'3-3'],18:[12,8,110.4,'3-4'],19:[12,10,0.5447,'3-5'],20:[12,12,110.0,'3-6'],21:[12,14,0.5684,'3-7'],
			22:[13,0,0.5681,'4-1'],23:[13,2,110.85,'4-2'],24:[13,4,0.5439,'4-3'],25:[13,6,110.84,'4-4'],26:[13,8,0.5435,'4-5'],27:[13,10],28:[13,12],29:[13,14],
			30:[15,0,111.5,'5-1'],31:[15,2,0.5438,'5-2'],32:[15,4,113.65,'5-3'],33:[15,6,0.5438,'5-4'],34:[15,8,0.5446,'5-5'],35:[15,10,114.7,'5-6'],36:[15,12,0.5441,'5-7'],37:[15,14,113.5,'5-8'],
			38:[16,0,0.5441,'6-1'],39:[16,2,116.2,'6-2'],40:[16,4,0.5689,'6-3'],41:[16,6,0.5442,'6-4'],42:[16,8,113.8,'6-5'],43:[16,10,0.5444,'6-6'],44:[16,12,114.5,'6-7'],45:[16,14,0.5451,'6-8'],
			46:[18,0,112.3,'7-1'],47:[18,2,0.5435,'7-2'],48:[18,4,113.3,'7-3'],49:[18,6,0.5433,'7-4'],50:[18,8,112.3,'7-5'],51:[18,10,0.5675,'7-6'],52:[18,12,112.3,'7-7'],53:[18,14,110.7,'7-8'],
			54:[22,0,0.5686,'8-1'],55:[22,2,109.68,'8-2'],56:[22,4,1,'8-3'],57:[22,6,0.565,'8-4'],58:[22,8,110,'8-5'],59:[22,10,110,'8-6'],60:[22,12,110,'8-7'],61:[22,14,1,'8-8']}

		#diodes = [1,3,5,7,8,10,12,14,15,17,19,21,22,24,
		#	26,31,33,34,36,38,40,41,43,45,47,49,51,54]
		#resistors = [2,4,6,9,11,13,16,18,20,23,25,30,
		#	32,35,37,39,42,44,46,48,50,52,53,55]

		diodes = [1,3,4,6,7,8,10,12,14,15,17,19,21,22,24,
			26,31,33,34,36,38,40,41,43,45,47,49,51,54,57]
		resistors = [2,5,9,11,13,16,18,20,23,25,30,
			32,35,37,39,42,44,46,48,50,52,53,55,58,59,60]

		board = s[sensor][0]; pin1 = s[sensor][1]; pin2 = pin1 + 1

		#conf = IOUT, conf2 = Vin
		conf = {0:0x0,1:0x1,2:0x2,3:0x3,4:0x4,5:0x5,6:0x6,7:0x7,8:0x8,9:0x9,
			10:0xA,11:0xB,12:0xC,13:0xD,14:0xE,15:0xF}
		conf2 = {0:0x0,1:0x20,2:0x40,3:0x60,4:0x80,5:0xA0,6:0xC0,7:0xE0,8:0x100,
			9:0x120,10:0x140,11:0x160,12:0x180,13:0x1A0,14:0x1C0,15:0x1E0}

		Iout = conf[pin1]; Vin = conf2[pin2]

		Channel_enable = 0x8013|Vin
		IO_control = 0x100|Iout #50 microA set on AIN pin2

		#print("board = %s, sensor = %s" %(board,sensor))
		#print(hex(Channel_enable))
	
		#Write to Channel_0 register: Update positive AIN for sensor
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x09,8))
		spi.writebytes(bytes(Channel_enable,16))
		GPIO.output(board,GPIO.HIGH)

		#if board == 38:
		#	channel = [0x09,0xA,0xB,0xC,0xD,0xE,0xF,0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18]
		#	for x in channel:
		#		GPIO.output(board,GPIO.LOW)
		#		spi.writebytes(bytes(read|x,8))
		#		ch_check = decimal(spi.readbytes(3))
		#		GPIO.output(board,GPIO.HIGH)
		#		print(hex(ch_check))
		#		if ch_check != 0x0001:
		#			print("Channel_%s is enabled. Disabling." %(channel.index(x)+1))
		#			GPIO.output(board,GPIO.LOW)
		#			spi.writebytes(bytes(write|x,8))
		#			spi.writebytes(bytes(0x0001,16))
		#			GPIO.output(board,GPIO.HIGH)		

		#Write IO_Control_1 register: Update Iout AIN output	
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x03,8)) 
		spi.writebytes(bytes(IO_control,24))
		GPIO.output(board,GPIO.HIGH)	

		#Write to ADC_CONTROL register: Update power mode to single conversion - begins conversion 
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x01,8))
		spi.writebytes(bytes(0x0004,16)) 
		GPIO.output(board,GPIO.HIGH)

		#Coefficients for Chebyshev polynomials - convert resistance/voltage to temp.
		#Coef. resistors (Resistance)
		r = [31.3231717,2.20213448,1.66482204e-3,-3.98620116e-6,4.74888650e-9,
			7.27263261e-12,-2.80325700e-14,3.11300149e-17,-1.22123964e-20] 
 		#Coef. diodes (Voltage)
		d = [2.06215201e4,-3.72240694e4,2.81733106e4,-1.78708069e4,9.20412215e3,
			-3.73253855e3,1.12440290e3,-2.25464342e2,22.4784626]
		#print("here: %s" %sensor)

		while True:
			#Read Status register: check that DOUT/RDY is low for conversion
			GPIO.output(board,GPIO.LOW)
			spi.writebytes(bytes(read|0x00,8))
			status = decimal(spi.readbytes(1))
			GPIO.output(board,GPIO.HIGH)
			#print(hex(status))
			time.sleep(0.01)

			#print(hex(status))
			#if board == 11:
			#	print(hex(status))

			if status == 0x40:
				print("LP ADC error - check error register")
				GPIO.output(board,GPIO.LOW)
				spi.writebytes(bytes(read|0x06,24))
				error = decimal(spi.readbytes(3))
				GPIO.output(board,GPIO.HIGH)
				print("Error register: %s" %hex(error))
				#time.sleep(0.01)

				output = 11111
				break
			elif status == 0x3:
				print("Sensor %s - wrong channel error" %sensor)
				output = 11111
				break

			#If DOUT/RDY == low, then read conversion from the Data register:
			#if 0x0 <= status and 0x0F >= status:
			if status == 0x0:
				#print("reading")
				GPIO.output(board,GPIO.LOW)
				spi.writebytes(bytes(read|0x02,8))
				data = decimal(spi.readbytes(3))
				GPIO.output(board,GPIO.HIGH)	

				polyR = np.polynomial.Chebyshev(r)
				polyD = np.polynomial.Chebyshev(d)

				if sensor in diodes:
					V = data*3.3/(2**(24)) #24bits to voltage w/ 3.3V reference
					#print(data)
					#print(V)
					#output = V

					V = V*0.5647/s[sensor][2]
					#if sensor <= 21: #Bottom shield sensors
					#	V = V*0.5653/s[sensor][2] #conversion at ~24.4C
					#else: #Top shield sensors
					#	V = V*0.57/s[sensor][2]	#conversion at ~22.3C

					if data > 16700000:
						#print("Sensor %s - N/C" %sensor)
						output = 11111
						break

					output = polyD(V)-273.15
					#output = V

				elif sensor in resistors:
					R = data*3.3/(2**(24)*50e-6) #24bits to resistance w/ 3.3V reference and 50microA excitation current
					V = data*3.3/(2**(24))
					#print(data)					
					#print(R)
					#print(R*50e-6)

					R = R*109.605/s[sensor][2]
					#if sensor <= 21: 
					#	R = R*109.5/s[sensor][2] #conversion at ~24.4C
					#else:
					#	R = 108.96*R/s[sensor][2] #conversion at ~23C

					if data > 16700000:
						#print("Sensor %s - N/C" %sensor)
						output = 11111
						break	
			
					output = polyR(R)-273.15
					#output = R
				break

			#elif 0x0 < status and 0x0F >= status:
			#	print("Sensor %s converting from wrong channel. Passing." %s[sensor][0])
			#	output = 11111
			#	break

				#if board == 11:
				#	print(output)
					#output = R
				#output = data
		#output = data
		#print(output)
		return output
	
