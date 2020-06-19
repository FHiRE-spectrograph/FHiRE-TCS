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

	#board=CS GPIO pin -- toggle relay board 2 AIN2/P1
	def Relay_ON(self, ind): 

		board = relay2[ind][0]
		pin = relay2[ind][1]

		if pin == 1:
			P = 0x010000 #P1/AIN2 - IO_CONTROL_1
		elif pin == 2:
			P = 0x020000 #P2/AIN3 - IO_CONTROL_1

		#Write IO_Control_1 register: pin=low	
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x03,8)) 
		spi.writebytes(bytes(P,24)) 
		GPIO.output(board,GPIO.HIGH)

		state[ind] = 1

	#board=CS GPIO pin -- toggle relay board 2 AIN2/P1
	def Relay_OFF(self, ind): 

		board = relay2[ind][0]
		pin = relay2[ind][1]

		if pin == 1:
			P = 0x110000 #P1/AIN2 - IO_CONTROL_1
		elif pin == 2:
			P = 0x220000 #P1/AIN3 - IO_CONTROL_1

		#Read IO_Control_1 register: pin=high
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(write|0x03,8)) 
		spi.writebytes(bytes(P,24)) 
		GPIO.output(board,GPIO.HIGH)

		state[ind] = 0

	def getTemp(self, sensor):
		sensor += 1

		#sensor:[CS GPIO - board,first AIN pin#] 29,28,27,61-56 = outside
		s = {1:[38,0],2:[38,4],3:[38,6],4:[38,8],5:[38,10],6:[38,12],7:[38,14],
			8:[11,0],9:[11,4],10:[11,6],11:[11,8],12:[11,10],13:[11,12],14:[11,14],
			15:[12,0],16:[12,4],17:[12,6],18:[12,8],19:[12,10],20:[12,12],21:[12,14],
			22:[13,0],23:[13,2],24:[13,4],25:[13,6],26:[13,8],27:[13,10],28:[13,12],29:[13,14],
			30:[15,0],31:[15,2],32:[15,4],33:[15,6],34:[15,8],35:[15,10],36:[15,12],37:[15,14],
			38:[16,0],39:[16,2],40:[16,4],41:[16,6],42:[16,8],43:[16,10],44:[16,12],45:[16,14],
			46:[18,0],47:[18,2],48:[18,4],49:[18,6],50:[18,8],51:[18,10],52:[18,12],53:[18,14],
			54:[22,0],55:[22,2],56:[22,4],57:[22,6],58:[22,8],59:[22,10],60:[22,12],61:[22,14]}

		board = s[sensor][0]; pin1 = s[sensor][1]; pin2 = pin1 + 1

		#Configuration for AIN pins for RTD sensors (even = excitation current, odd = volt. inp.)
		conf = {0:0x0,1:0x20,2:0x2,3:0x60,4:0x4,5:0xA0,6:0x6,7:0xE0,8:0x8,
			9:0x120,10:0xA,11:0x160,12:0xC,13:0x1A0,14:0xE,15:0x1E0}

		Iout = conf[pin1]; Vin = conf[pin2]

		Channel_enable = 0x8013|Vin
		IO_control = 0x100|Iout #50 microA set on AIN pin2

		#Need a more robust way to check that relay is on. 
		if board in [38,11,12]:
			toggle = 0x0
			for relay, status1 in state.items():
				gp = relay2[relay][1] 
				if status1 == 1: #keep general-purpose pin On
					if gp == 1:
						P = 0x010000
					elif gp == 2:
						P = 0x020000
				elif status1 == 0: #keep general-purpose pin Off
					if gp == 1:
						P = 0x110000
					elif gp == 2:
						P = 0x220000
					
				toggle = toggle|P

			#enable both P1 and P2, 50 microA set on AIN pin2, retain relay status
			IO_control = 0x030100|Iout|toggle 

		#Reset to get reading from each board, but it slows the program.
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(reset)
		time.sleep(1)
		GPIO.output(board,GPIO.HIGH)
	
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

		#Read Status register: check that DOUT/RDY is low for conversion
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(read|0x00,8))
		status=decimal(spi.readbytes(1))
		#print "Status Register: %s" %status
		GPIO.output(board,GPIO.HIGH)

		#Formulas and constants taken from HP sensor code. Likely not applicable to LP sensors.:
		C0=-245.19
		C1=5.5293
		C2=-0.066046
		C3=4.0422e-3
		C4=-2.0697e-6
		C5=-0.025422
		C6=1.6883e-3
		C7=-1.3601e-6

		while True:
			#If DOUT/RDY == low, then read conversion from the Data register:
			if status >= 0x80:
				GPIO.output(board,GPIO.LOW)
				spi.writebytes(bytes(read|0x02,8))
				data=decimal(spi.readbytes(3))
				GPIO.output(board,GPIO.HIGH)	
				R = ((2.3e-7*data)/0.00005)/2 # 50 microA excitation current, V might not be right? Also, not sure if it should be divided by 2. 
				output=C0+(R*(C1+R*(C2+R*(C3+C4*R))))/(1+R*(C5+R*(C6+C7*R)))
				return output
				





