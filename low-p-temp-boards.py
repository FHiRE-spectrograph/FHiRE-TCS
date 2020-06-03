import numpy as np
import time
import spidev
import RPi.GPIO as GPIO
#import sys

# intialize SPI communication ---------------------------------------
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 3
#spi.no_cs #set false or true? false = manually control spi devices cs. ***ERROR** - ask Stephen

#Initialize GPIO pins on RPI1 ---------------------------------------
# GPIO pins are used for SPI chip select pins. Chip select pins are held high between communication
# brought low when sending commands and go high again when transaction is complete. CS is held low through 
# duration of a read transaction and brought high when read is complete.

GPIO.setmode(GPIO.BOARD)
#GPIO.cleanup()
GPIO_pins=[7,11,12,13,15,16,18,22] #CS 1-8

#for x in GPIO_pins:
#	GPIO.setup(x,GPIO.OUT)
#	GPIO.output(x,GPIO.HIGH)
GPIO.setup(11,GPIO.OUT)
GPIO.output(11,GPIO.HIGH)

def initialize_boards():
	#Activate pins
#	for x in GPIO_pins:
#		GPIO.output(x,GPIO.LOW)
	GPIO.output(11,GPIO.LOW)
	
	spi.writebytes(init_bytes_1)
	
	#De-activate pins
#	for x in GPIO_pins:
#		GPIO.output(x,GPIO.HIGH)
	GPIO.output(11,GPIO.HIGH)
	
	#Activate pins --- **Why can't you send 2 commands at a time?
#	for x in GPIO_pins:
#		GPIO.output(x,GPIO.LOW)
	GPIO.output(11,GPIO.LOW)

	spi.writebytes(init_bytes_2)

#	for x in GPIO_pins:
#		GPIO.output(x,GPIO.HIGH)
	GPIO.output(11,GPIO.HIGH)




# All communication to low-p boards starts with a write operation to the communication register
# data written to the communication register determines if the next operationb is a read or a write
# a 0 means a write operation and a 1 means a read operation on bit 6 of the com reg

# com reg bits: |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
#               | WEN | r/w |         RS[5:0]                   |

read = 0x40
write = 0x00
reset=0xFFFFFFFFFFFFFFFF

# register addresses. Regester addresses must be OR-ed with read or write command 
ADC_Control = 0x01
Data_Reg = 0x02
IO_Ctrl_Reg = 0x03

# because boards are operated in single shot mode, only one channel needs to be addressed 
Ch_1 = 0x09 #Channel register
#Ch_2 = 0x0a
#Ch_3 = 0x0b
#Ch_4 = 0x0c
#Ch_5 = 0x0d
#Ch_6 = 0x0e
#Ch_7 = 0x0f
#Ch_8 = 0x10
#Ch_9 = 0x011
#Ch_10 = 0x12
#Ch_11 = 0x13
#Ch_12 = 0x14
#Ch_13 = 0x15
#Ch_14 = 0x16
#Ch_15 = 0x17
#Ch_16 = 0x18

# only one configuration is being used and is programmed in the "init_bytes" below
#Config_reg0 = 0x19
#Config_reg1 = 0x1a
#Config_reg2 = 0x1b
#Config_reg3 = 0x1c
#Config_reg4 = 0x1d
#Config_reg5 = 0x1e
#Config_reg6 = 0x1f
#Config_reg7 = 0x20


# boards 1-3 use IO pins to operate some of the relays. The register that controls the IO pins also controls the excitation current for the sensors. Every time the read function changes channels the excitation current must be changed to that channel as well. this requires that the register controlling the relays/current be reprogramed, therfore a check must be done to see if the relays are supposed to be on or off and the proper bits are combined accordingly.
#**Not sure about these values**
'''
Board1_relay1_on = 0x31
Board1_relay1_off = 0x30
Board1_relay2_on = 0x32
Board1_relay2_off = 0x30

Board2_relay1_on = 0x31
Board2_relay1_off = 0x30
Board2_relay2_on = 0x32
Board2_relay2_off = 0x30

Board3_relay1_on = 0x31
Board3_relay1_off = 0x30
Board3_relay2_on = 0x32
Board3_relay2_off = 0x30

HR21 = True
HR22 = False
HR23 = False
HR24 = False
HR25 = False
HR26 = False

#What are these prefixes used for?
if HR21 == True and HR22 == True:
	Board1_IO_prefix = Board1_relay1_on|Board1_relay2_on 
elif HR21 == True and HR22 == False:
	Board1_IO_prefix = Board1_relay1_on|Board1_relay2_off
elif HR21 == False and HR22 == False:
	Board1_IO_prefix = Board1_relay1_off|Board1_relay2_off
elif HR21 == False and HR22 == True:
	Board1_IO_prefix = Board1_relay1_off|Board1_relay2_on

Cur_prefix=Board1_IO_prefix #maybe?

if HR21 == True and HR22 == True:
	Board2_IO_prefix = Board2_relay1_on|Board2_relay2_on
elif HR21 == True and HR22 == False:
	Board2_IO_prefix = Board2_relay1_on|Board2_relay2_off
elif HR21 == False and HR22 == False:
	Board2_IO_prefix = Board2_relay1_off|Board2_relay2_off
elif HR21 == False and HR22 == True:
	Board2_IO_prefix = Board2_relay1_off|Board2_relay2_on

if HR21 == True and HR22 == True:
	Board3_IO_prefix = Board3_relay1_on|Board3_relay2_on
elif HR21 == True and HR22 == False:
	Board3_IO_prefix = Board3_relay1_on|Board3_relay2_off
elif HR21 == False and HR22 == False:
	Board3_IO_prefix = Board3_relay1_off|Board3_relay2_off
elif HR21 == False and HR22 == True:
	Board3_IO_prefix = Board3_relay1_off|Board3_relay2_on
'''

# Register setup commands
init_bytes_1 = [0x01,0x02,0xc6] # single shot read mode and disables internal Voltage reference
init_bytes_2 = [0x19,0x0000] # selects reference source, turns off buffers and sets gain to 1


def Read(board_GPIO,channel):
	#IO_write, channel_write not defined anywhere
	board=board_GPIO	

	if channel == 1:
		Iout = 0x1 #AIN1
		Vin = 0x0  #AIN0?
	elif channel == 2:
		Iout = 0x3 #AIN3
		Vin = 0x2  #AIN2?
	elif channel == 3:
		Iout = 0x5 #AIN5
		Vin = 0x4  #AIN4?
	elif channel == 4:
		Iout = 0x7 #AIN7
		Vin = 0x6  #AIN6?
	elif channel == 5:
		Iout = 0x9 #AIN9
		Vin = 0x8  #AIN8?
	elif channel == 6:
		Iout = 0xb #AIN11
		Vin = 0xa  #AIN10?
	elif channel == 7:
		Iout = 0xd #AIN13
		Vin = 0xc  #AIN12?
	elif channel == 8:
		Iout = 0xf #AIN15
		Vin = 0xe  #AIN14?

	shifted_Vin = Vin<<5

	High=0x110000; #High=format(High,'08b') #Set P1 high
	#print(High)
	Low=0x0010000; #Low=format(Low,'08b') #Set P1 low - add 7 leading zeros
	#print(Low)

	Cur_prefix=0x0
	shifted_cur_prefix = Cur_prefix<<16 #Need to defin Cur_prefix **What is it?

	
	Channel_enable = 0x8013|shifted_Vin
	Current_enable = 0x000100|shifted_cur_prefix|Iout
	Channel_disable = 0x0013|shifted_Vin
	Current_disable = 0x000000|shifted_cur_prefix|Iout
	#print(Current_enable)

	Current_high=Current_enable|High	
	#print(Current_high)
	Current_low=Current_enable|Low

	channel_write=write|Ch_1
	IO_write=write|IO_Ctrl_Reg

	#print(hex(channel_write))
	#print(IO_write)
	print(Channel_enable)


	#Commands:
	GPIO.output(board,GPIO.LOW)
	spi.writebytes([read|0x00]) #read bits from Status register
	print spi.readbytes(3)
	spi.writebytes([reset])
	GPIO.output(board,GPIO.HIGH)

	time.sleep(0.5)

	GPIO.output(board,GPIO.LOW)
	spi.writebytes([read|Ch_1]) #read bits from IO_CONTROL_1 register
	print spi.readbytes(3)
	spi.writebytes([reset])
	GPIO.output(board,GPIO.HIGH)

	time.sleep(0.5)

	GPIO.output(board,GPIO.LOW)
	spi.writebytes([channel_write,0x8001]) #Power-on Channel_0 register
	spi.writebytes([reset])
	GPIO.output(board,GPIO.HIGH)
	'''
	time.sleep(0.5)

	GPIO.output(board,GPIO.LOW)
	spi.writebytes([IO_write]) #Power-on IO_CONTROL_1 register
	spi.writebytes([0x000000])
	spi.writebytes([reset])
	GPIO.output(board,GPIO.HIGH)
	'''
	time.sleep(0.5)
	
	GPIO.output(board,GPIO.LOW)
	spi.writebytes([read|Ch_1]) #read bits from IO_CONTROL_1 register
	print spi.readbytes(3)
	spi.writebytes([reset])
	GPIO.output(board,GPIO.HIGH)
	
	time.sleep(0.5)
	
	GPIO.output(board,GPIO.LOW)
	spi.writebytes([channel_write,Channel_enable])	
	spi.writebytes([reset])
	GPIO.output(board,GPIO.HIGH)	

	time.sleep(0.5)
	
	GPIO.output(board,GPIO.LOW)
	spi.writebytes([read|Ch_1]) #read bits from IO_CONTROL_1 register
	print spi.readbytes(3)
	spi.writebytes([reset])
	GPIO.output(board,GPIO.HIGH)

	time.sleep(0.5)
	'''
	GPIO.output(board,GPIO.LOW)
	spi.writebytes([IO_write,Current_enable])
	spi.writebytes([reset])
	GPIO.output(board,GPIO.HIGH)
	
	time.sleep(0.5)
	
	#GPIO.output(board,GPIO.LOW)
	#spi.writebytes([read]) 
	#GPIO.output(board,GPIO.HIGH)
	
	#GPIO.output(board,GPIO.LOW)
	#spi.readbytes(3)
	#GPIO.output(board,GPIO.HIGH)
	GPIO.output(board,GPIO.LOW)
	spi.writebytes([IO_write,Current_high])
	GPIO.output(board,GPIO.HIGH)	
	print("Relay ON") #Not toggling though.

	time.sleep(2)

	GPIO.output(board,GPIO.LOW)
	spi.writebytes([IO_write,Current_low])
	GPIO.output(board,GPIO.HIGH)
	print("Relay OFF")

	time.sleep(2)

	GPIO.output(board,GPIO.LOW)
	spi.writebytes([IO_write,Current_high])
	spi.writebytes([reset])
	GPIO.output(board,GPIO.HIGH)	
	print("Relay ON")
	'''
	time.sleep(2)

	GPIO.output(board,GPIO.LOW)
	spi.writebytes([channel_write,Channel_disable])
	spi.writebytes([reset])
	GPIO.output(board,GPIO.HIGH)

	time.sleep(0.5)
	
	GPIO.output(board,GPIO.LOW)
	spi.writebytes([IO_write,Current_disable])
	GPIO.output(board,GPIO.HIGH)
	print("END")


initialize_boards()
Read(11,2)

#Need to clear memory and set up a closing case.
GPIO.cleanup()
#sys.exit(0)




