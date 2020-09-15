import numpy as np
import time, math
import spidev
import RPi.GPIO as GPIO

# intialize SPI communication ---------------------------------------
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 3
spi.no_cs=False #set false or true? false = manually control spi devices cs. error. Doesn't seem to do anything.

#Initialize GPIO pins on RPI1 ---------------------------------------
# GPIO pins are used for SPI chip select pins. Chip select pins are held high between communication
# brought low when sending commands and go high again when transaction is complete. CS is held low through 
# duration of a read transaction and brought high when read is complete.

#Convert decimal/hex to a byte array
def bytes(decimal,bitsize):
	if bitsize == 8:
		x=decimal
 		return [int(x)]
	elif bitsize == 16:
		y=math.floor(decimal*2**(-8))
		x=decimal-y*2**8
		#return [int(x),int(y)]
		return [int(y),int(x)]
	elif bitsize == 24:
		z=math.floor(decimal*2**(-16))
		d2=decimal-z*2**16
		y=math.floor(d2*2**(-8))
		x=d2-y*2**8
		#return [int(x),int(y),int(z)]
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
		reset=[255,255,255,255,255,255,255,255] #0xFFFFFFFFFFFFFFFF

		state = {21:0,22:0,23:0,24:0,25:0,26:0} #Keep track whether relay is on/off (off=0)
		relay2={21:[38,1],22:[38,2],23:[11,1],24:[11,2],25:[12,1],26:[12,2]}#Relay:[CS GPIO - board,pin]

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

		#Write to CHANNEL_0 register: conversion=disabled, setup_0, AIN0=pos, AIN0=neg *Configuration might only work for relays*
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x09,8))
		spi.writebytes(bytes(0x8033,16))
		GPIO.output(board,GPIO.HIGH)

	#board=CS GPIO pin -- toggle relay 
	def Relay_ON(self, ind): 
		
		board = relay2[ind][0]
		pin = relay2[ind][1]

		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(read|0x03,8))
		status1 = decimal(spi.readbytes(3))
		GPIO.output(board,GPIO.HIGH)

		if pin == 1:
			P = 0x010000 #P1/AIN2 - IO_CONTROL_1
			S = 0x0
			Q = 0x0
		elif pin == 2:
			P = 0x020000 #P2/AIN3 - IO_CONTROL_1
			Q = 0x0
			S = 0x0

		print P|Q|S
		#Write IO_Control_1 register: pin=low	
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x03,8)) 
		spi.writebytes(bytes(P|Q|S,24)) 
		GPIO.output(board,GPIO.HIGH)
		
		print '%s ON' %ind

	def Relay_OFF(self, ind): 
		
		board = relay2[ind][0]
		pin = relay2[ind][1]

		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(read|0x03,8))
		status1 = decimal(spi.readbytes(3))
		GPIO.output(board,GPIO.HIGH)

		if pin == 1:
			P = 0x110000 #P1/AIN2 - IO_CONTROL_1
			S = 0x0
			Q = 0x0
		elif pin == 2:
			P = 0x220000 #P2/AIN3 - IO_CONTROL_1
			Q = 0x0
			S = 0x0

		print P|Q|S
		#Read IO_Control_1 register: pin=high
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x03,8)) 
		spi.writebytes(bytes(P|Q|S,24)) 
		GPIO.output(board,GPIO.HIGH)

		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(read|0x03,8))
		status1 = decimal(spi.readbytes(3))
		GPIO.output(board,GPIO.HIGH)
		

		print '%s OFF' %ind

	def getTemp(self, sensor):
		sensor += 1

		#sensor:[CS GPIO - board,first AIN pin#,resistance at room temp] 29,28,27,61-56 = outside
		s = {1:[38,0,0.56675,'1-1'],2:[38,4,107.23,'1-2'],3:[38,6,0.56623,'1-3'],4:[38,8,107.15,'1-4'],5:[38,10,107.45,'1-5'],6:[38,12,107.6,'1-6'],7:[38,14,0.54185,'1-7'],
			8:[11,0,0.56713,'2-1'],9:[11,4,108.18,'2-2'],10:[11,6,0.54146,'2-3'],11:[11,8,108.5,'2-4'],12:[11,10,0.56776,'2-5'],13:[11,12,108.3,'2-6'],14:[11,14,0.54187,'2-7'],
			15:[12,0,0.54211,'3-1'],16:[12,4,110.01,'3-2'],17:[12,6,0.566278,'3-3'],18:[12,8,110.4,'3-4'],19:[12,10,0.54306,'3-5'],20:[12,12,110.3,'3-6'],21:[12,14,0.56845,'3-7'],
			22:[13,0,0.574,'4-1'],23:[13,2,110.03,'4-2'],24:[13,4,0.5486,'4-3'],25:[13,6,110.03,'4-4'],26:[13,8,0.548,'4-5'],27:[13,10],28:[13,12],29:[13,14],
			30:[15,0,111.0,'5-1'],31:[15,2,0.5486,'5-2'],32:[15,4,110.32,'5-3'],33:[15,6,0.5486,'5-4'],34:[15,8,0.5497,'5-5'],35:[15,10,110.1,'5-6'],36:[15,12,0.549,'5-7'],37:[15,14,110.2,'5-8'],
			38:[16,0,0.5491,'6-1'],39:[16,2,1111,'6-2'],40:[16,4,0.5755,'6-3'],41:[16,6,0.5490,'6-4'],42:[16,8,111.3,'6-5'],43:[16,10,0.5492,'6-6'],44:[16,12,111.2,'6-7'],45:[16,14,0.5497,'6-8'],
			46:[18,0,109.9,'7-1'],47:[18,2,0.5482,'7-2'],48:[18,4,109.72,'7-3'],49:[18,6,0.5480,'7-4'],50:[18,8,109.6,'7-5'],51:[18,10,0.5736,'7-6'],52:[18,12,109.8,'7-7'],53:[18,14,110.2,'7-8'],
			54:[22,0,0.5746,'8-1'],55:[22,2,108.98,'8-2'],56:[22,4],57:[22,6],58:[22,8],59:[22,10],60:[22,12],61:[22,14]}

		diodes = [1,3,7,8,10,12,14,15,17,19,21,22,24,
			26,31,33,34,36,38,40,41,43,45,47,49,51,54]
		resistors = [2,4,5,6,9,11,13,16,18,20,23,25,30,
			32,35,37,39,42,44,46,48,50,52,53,55]

		board = s[sensor][0]; pin1 = s[sensor][1]; pin2 = pin1 + 1


		#conf = IOUT, conf2 = Vin
		conf = {0:0x0,1:0x1,2:0x2,3:0x3,4:0x4,5:0x5,6:0x6,7:0x7,8:0x8,9:0x9,
			10:0xA,11:0xB,12:0xC,13:0xD,14:0xE,15:0xF}
		conf2 = {0:0x0,1:0x20,2:0x40,3:0x60,4:0x80,5:0xA0,6:0xC0,7:0xE0,8:0x100,
			9:0x120,10:0x140,11:0x160,12:0x180,13:0x1A0,14:0x1C0,15:0x1E0}

		Iout = conf[pin1]; Vin = conf2[pin2]

		Channel_enable = 0x8013|Vin
		IO_control = 0x100|Iout #50 microA set on AIN pin2
	
		#Write to Channel_0 register: Update positive AIN for sensor
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x09,8))
		spi.writebytes(bytes(Channel_enable,16))
		GPIO.output(board,GPIO.HIGH)

		#Write IO_Control_1 register: Update Iout AIN output	
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x03,8)) 
		spi.writebytes(bytes(IO_control,24))
		GPIO.output(board,GPIO.HIGH)	

		#Write to ADC_CONTROL register: Update power mode to single conversion. 
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x01,8))
		spi.writebytes(bytes(0x0004,16)) 
		GPIO.output(board,GPIO.HIGH)

		#Coef. resistors (Resistance)
		r = [31.3231717,2.20213448,1.66482204e-3,-3.98620116e-6,4.74888650e-9,
			7.27263261e-12,-2.80325700e-14,3.11300149e-17,-1.22123964e-20] 
 		#Coef. diodes (Voltage)
		d = [2.06215201e4,-3.72240694e4,2.81733106e4,-1.78708069e4,9.20412215e3,
			-3.73253855e3,1.12440290e3,-2.25464342e2,22.4784626]

		while True:

			#Read Status register: check that DOUT/RDY is low for conversion
			GPIO.output(board,GPIO.LOW)
			spi.writebytes(bytes(read|0x00,8))
			status=decimal(spi.readbytes(1))
			GPIO.output(board,GPIO.HIGH)

			#If DOUT/RDY == low, then read conversion from the Data register:
			if status == 0x0:
				GPIO.output(board,GPIO.LOW)
				spi.writebytes(bytes(read|0x02,8))
				data=decimal(spi.readbytes(3))
				GPIO.output(board,GPIO.HIGH)	

				polyR = np.polynomial.Chebyshev(r)
				polyD = np.polynomial.Chebyshev(d)

				if sensor in diodes:
					V = data*3.3/(2**(24))

					if sensor <= 21:
						V = V*0.5653/s[sensor][2] #conversion at ~24.4C
					else:
						V = V*0.57/s[sensor][2]	#conversion at ~22.3C

					if data > 16700000:
						output = 11111
						break

					output = polyD(V)-273.15

				elif sensor in resistors:
					R = data*3.3/(2**(24)*50e-6)

					if sensor <= 21:
						R = R*109.5/s[sensor][2] #conversion at ~24.4C
					else:
						R = 108.96*R/s[sensor][2] #conversion at ~23C


					R = 108.96*R/s[sensor][2]

					if data > 16700000:
						output = 11111
						break				

					output = polyR(R)-273.15
				break
				
		return output
	


