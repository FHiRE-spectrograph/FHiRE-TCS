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
		return [int(x),int(y)]
	elif bitsize == 24:
		z=math.floor(decimal*2**(-16))
		d2=decimal-z*2**16
		y=math.floor(d2*2**(-8))
		x=d2-y*2**8
		return [int(x),int(y),int(z)]


#Convert byte array to a decimal
def decimal(b):
	if len(b) < 3:
		b.append(0)
		b.append(0)

	decimal=b[0]+(b[1]<<8)+(b[2]<<16)

	return decimal

GPIO.setmode(GPIO.BOARD)
#GPIO.cleanup()
GPIO_pins=[7,11,12,13,15,16,18,22] #CS 1-8

#Setup all CS pins and hold high
for x in GPIO_pins:
	GPIO.setup(x,GPIO.OUT)
	GPIO.output(x,GPIO.HIGH)

# All communication to low-p boards starts with a write operation to the communication register
# data written to the communication register determines if the next operationb is a read or a write
# a 0 means a write operation and a 1 means a read operation on bit 6 of the com reg

# com reg bits: |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
#               | WEN | r/w |         RS[5:0]                   |

read = 0x40
write = 0x00
reset=[255,255,255,255,255,255,255,255] #0xFFFFFFFFFFFFFFFF

# boards 1-3 use IO pins to operate some of the relays. The register that controls the IO pins also controls the excitation current for the sensors. Every time the read function changes channels the excitation current must be changed to that channel as well. this requires that the register controlling the relays/current be reprogramed, therfore a check must be done to see if the relays are supposed to be on or off and the proper bits are combined accordingly.

def Read(board): #board=CS GPIO pin -- toggle relay board 2 AIN2/P1

	#Read ID register: check
	GPIO.output(board,GPIO.LOW)
	time.sleep(0.1)
	spi.writebytes(bytes(read|0x05,8)) 
	print "ID Register: %s" % hex(decimal(spi.readbytes(3))) #Should return 0x14
	time.sleep(0.1)
	GPIO.output(board,GPIO.HIGH)

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

	#Write to CHANNEL_0 register: setup_0, AIN2=pos, DGND=neg
	GPIO.output(board,GPIO.LOW)
	spi.writebytes(bytes(write|0x09,8))
	spi.writebytes(bytes(0x8053,16))
	GPIO.output(board,GPIO.HIGH)

	#Write to ADC_CONTROL register: disable int. voltage, low-power, single-conversion mode, int. clock source
	GPIO.output(board,GPIO.LOW)
	spi.writebytes(bytes(write|0x01,8))
	spi.writebytes(bytes(0x0005,16)) 
	GPIO.output(board,GPIO.HIGH)

	#Read IO_Control_1 register: P1=low, Iout0=50microA on AIN2 pin/P1
	GPIO.output(board,GPIO.LOW)
	time.sleep(0.5)
	spi.writebytes(bytes(write|0x03,8)) 
	time.sleep(0.1)
	spi.writebytes(bytes(0x010102,24)) 
	time.sleep(0.5)
	print "Relay enabled/OFF"
	GPIO.output(board,GPIO.HIGH)

	#Read IO_Control_1 register: P1=high, Iout0=50microA on AIN2 pin/P1
	GPIO.output(board,GPIO.LOW)
	time.sleep(0.5)
	spi.writebytes(bytes(write|0x03,8)) 
	time.sleep(0.1)
	spi.writebytes(bytes(0x210102,24)) 
	time.sleep(0.5)
	print "Relay ON"
	GPIO.output(board,GPIO.HIGH)

	#Read IO_Control_1 register: P1=low, Iout0=50microA on AIN2 pin/P1
	GPIO.output(board,GPIO.LOW)
	time.sleep(0.5)
	spi.writebytes(bytes(write|0x03,8)) 
	time.sleep(0.1)
	spi.writebytes(bytes(0x010102,24)) 
	time.sleep(0.5)
	print "Relay OFF"
	GPIO.output(board,GPIO.HIGH)

	#Reset digital interface
	GPIO.output(board,GPIO.LOW)
	print "Resetting digital interface"
	spi.writebytes(reset) 
	time.sleep(3)
	GPIO.output(board,GPIO.HIGH)
	print "Complete"


if __name__=='__main__':
	try:
		Read(11)
	except KeyboardInterrupt:
		print("*Interrupted*")
		GPIO.cleanup()
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)




