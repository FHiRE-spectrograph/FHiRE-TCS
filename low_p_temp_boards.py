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

		global read, write, reset

		read = 0x40
		write = 0x00
		reset=[255,255,255,255,255,255,255,255] #0xFFFFFFFFFFFFFFFF

		self.Setup(38); self.Setup(11); self.Setup(12) #Setup relay boards
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
		spi.writebytes(bytes(0x0,16)) 
		GPIO.output(board,GPIO.HIGH)

		#Write to CHANNEL_0 register: conversion=disabled, setup_0, AIN0=pos, AIN0=neg *Configuration might only work for relays*
		GPIO.output(board,GPIO.LOW)
		time.sleep(0.1)
		spi.writebytes(bytes(write|0x09,8))
		spi.writebytes(bytes(0x0,16))
		time.sleep(0.1)
		GPIO.output(board,GPIO.HIGH)

	#board=CS GPIO pin -- toggle relay board 2 AIN2/P1
	def Relay_ON(self, board, pin): 

		if pin == 1:
			P = 0x010000 #P1/AIN2 - IO_CONTROL_1
		elif pin == 2:
			P = 0x020000 #P2/AIN3 - IO_CONTROL_1

		#Write IO_Control_1 register: pin=low	
		GPIO.output(board,GPIO.LOW)
		time.sleep(0.1)
		spi.writebytes(bytes(write|0x03,8)) 
		time.sleep(0.1)
		spi.writebytes(bytes(P,24)) 
		time.sleep(0.1)
		GPIO.output(board,GPIO.HIGH)

	#board=CS GPIO pin -- toggle relay board 2 AIN2/P1
	def Relay_OFF(self, board, pin): 

		if pin == 1:
			P = 0x110000 #P1/AIN2 - IO_CONTROL_1
		elif pin == 2:
			P = 0x220000 #P1/AIN3 - IO_CONTROL_1


		#Read IO_Control_1 register: pin=high
		GPIO.output(board,GPIO.LOW)
		time.sleep(0.1)
		spi.writebytes(bytes(write|0x03,8)) 
		time.sleep(0.1)
		spi.writebytes(bytes(P,24)) 
		time.sleep(0.1)
		GPIO.output(board,GPIO.HIGH)

	def getTemp(self, sensor):
		sensor += 1
		#sensor:[CS GPIO - board,AIN pin#] 29,28,27,61-56 = outside
		s = {1:[38,0],2:[38,4],3:[38,],4:[38,],5:[38,],6:[38,],7:[38,],
			8:[11,],9:[11,],10:[11,],11:[11,],12:[11,],13:[11,],14[11,],
			15:[12,],16:[12,],17:[12,],18:[12,],19:[12,],20:[12,],21:[12,]
			22:[13,],23:[13,],24:[13,],25:[13,],26:[13,],27:[13,],28:[13,],29:[13,],
			30:[15,],31:[15,],32:[15,],33:[15,],34:[15,],35:[15,],36:[15,],37:[15,],
			38:[16,],39:[16,],40:[16,],41:[16,],42:[16,],43:[16,],44:[16,],45:[16,],
			46:[18,],47:[18,],48:[18,],49:[18,],50:[18,],51:[18,],52:[18,],53:[18,],
			54:[22,],55:[22,],56:[22,],57:[22,],58:[22,],59:[22,],60:[22,],61:[22,]}

		board = s[sensor][0]; pin = s[sensor][1]




#board=CS GPIO pin -- Read sensor board 1 AIN0/AIN1
def Sensor(board): 

	#Write to CHANNEL_0 register: setup_0, AIN0=pos, DGND=neg
	GPIO.output(board,GPIO.LOW)
	spi.writebytes(bytes(write|0x09,8))
	spi.writebytes(bytes(0x8013,16))
	GPIO.output(board,GPIO.HIGH)

	#Write to ADC_CONTROL register: disable int. voltage, low-power, single-conversion mode, int. clock source
	GPIO.output(board,GPIO.LOW)
	time.sleep(0.1)
	spi.writebytes(bytes(write|0x01,8))
	time.sleep(0.1)
	spi.writebytes(bytes(0x0000,16)) 
	time.sleep(0.1)
	GPIO.output(board,GPIO.HIGH)

	#Read ADC_CONTROL register: check that mode=standby
	GPIO.output(board,GPIO.LOW)
	spi.writebytes(bytes(read|0x01,8))
	print "ADC_CONTROL Register: %s" %decimal(spi.readbytes(3))
	GPIO.output(board,GPIO.HIGH)

	#Write to IO_CONTROL_1 register: IOUT1=IOUT0=50microA, IOUT1=AIN1, IOUT2=AIN0
	GPIO.output(board,GPIO.LOW)
	spi.writebytes(bytes(write|0x03,8))
	spi.writebytes(bytes(0x000910,24)) 
	GPIO.output(board,GPIO.HIGH)

	#Read Status register: check that DOUT/RDY is low for conversion
	GPIO.output(board,GPIO.LOW)
	spi.writebytes(bytes(read|0x00,8))
	status=decimal(spi.readbytes(3))
	print "Status Register: %s" %status
	GPIO.output(board,GPIO.HIGH)

	#If DOUT/RDY == low, then read conversion from the Data register:
	if status >= 0x80:
		GPIO.output(board,GPIO.LOW)
		spi.writebytes(bytes(read|0x02,8))
		data=decimal(spi.readbytes(3))
		print "Data: %s" %data
		GPIO.output(board,GPIO.HIGH)

	#If you wanted to read more, then you'll have to reset the ADC_control next...

	#Read ADC_CONTROL register: check that mode=standby **Doesn't read 16bit value**
	GPIO.output(board,GPIO.LOW)
	spi.writebytes(bytes(read|0x01,8))
	print "ADC_CONTROL Register: %s" %decimal(spi.readbytes(3))
	GPIO.output(board,GPIO.HIGH)




