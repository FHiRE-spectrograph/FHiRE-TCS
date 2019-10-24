import numpy as np
import time
import spidev
import RPi.GPIO as GPIO

# intialize SPI communication
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 3
spi.no_cs

# All communication to low-p boards starts with a write operation to the communication register
# data written to the communication register determines if the next operationb is a read or a write
# a 0 means a write operation and a 1 means a read operation on bit 6 of the com reg

# com reg bits: |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
#               | WEN | r/w |         RS[5:0]                   |

read = 0x40
write = 0x00

# register addresses. Regester addresses must be OR-ed with read or write command 
ADC_Control = 0x01
Data_Reg = 0x02
IO_Ctrl_Reg = 0x03


# because boards are operated in single shot mode, only one channel needs to be addressed
Ch_1 = 0x09
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

HR21 = False
HR22 = False
HR23 = False
HR24 = False
HR25 = False
HR26 = False


if HR21 = True and HR22 = True:
	Board1_IO_prefix = Board1_relay1_on|Board1_relay2_on
elif HR21 = True and HR22 = False:
	Board1_IO_prefix = Board1_relay1_on|Board1_relay2_off
elif HR21 = False and HR22 = False:
	Board1_IO_prefix = Board1_relay1_off|Board1_relay2_off
elif HR21 = False and HR22 = True:
	Board1_IO_prefix = Board1_relay1_off|Board1_relay2_on


if HR21 = True and HR22 = True:
	Board2_IO_prefix = Board2_relay1_on|Board2_relay2_on
elif HR21 = True and HR22 = False:
	Board2_IO_prefix = Board2_relay1_on|Board2_relay2_off
elif HR21 = False and HR22 = False:
	Board2_IO_prefix = Board2_relay1_off|Board2_relay2_off
elif HR21 = False and HR22 = True:
	Board2_IO_prefix = Board2_relay1_off|Board2_relay2_on


if HR21 = True and HR22 = True:
	Board3_IO_prefix = Board3_relay1_on|Board3_relay2_on
elif HR21 = True and HR22 = False:
	Board3_IO_prefix = Board3_relay1_on|Board3_relay2_off
elif HR21 = False and HR22 = False:
	Board3_IO_prefix = Board3_relay1_off|Board3_relay2_off
elif HR21 = False and HR22 = True:
	Board3_IO_prefix = Board3_relay1_off|Board3_relay2_on



if channel = 1:
	Iout = 0x1
	Vin = 0x0
elif channel = 2:
	Iout = 0x3
	Vin = 0x2
elif channel = 3:
	Iout = 0x5
	Vin = 0x4
elif channel = 4:
	Iout = 0x7
	Vin = 0x6
elif channel = 5:
	Iout = 0x9
	Vin = 0x8
elif channel = 6:
	Iout = 0xb
	Vin = 0xa
elif channel = 7:
	Iout = 0xd
	Vin = 0xc
elif channel = 8:
	Iout = 0xf
	Vin = 0xe


shifted_Vin = Vin<<5

Shifted_cur_prefix = Cur_prefix<<16

Channel_enable = 0x8013|shifted_Vin
Current_enable = 0x000100|shifted_cur_prefix|Iout
Channel_disable = 0x0013|shifted_vin
Current_disable = 0x000000|shifted_cur_prefix|Iout


# Register setup commands
init_bytes_1 = [0x01,0x02,0xc6] # single shot read mode and disables internal Voltage reference
init_bytes_2 = [0x19,0x0000] # selects reference source, turns off buffers and sets gain to 1

# GPIO pins are used for SPI chip select pins. Chip select pins are held high between communication
# brought low when sending commands and go high again when transaction is complete. CS is held low through 
# duration of a read transaction and brought high when read is complete.
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

GPIO.setup(7,GPIO.OUT)
GPIO.output(7,GPIO.HIGH)

GPIO.setup(11,GPIO.OUT)
GPIO.output(11,GPIO.HIGH)

GPIO.setup(12,GPIO.OUT)
GPIO.output(12,GPIO.HIGH)

GPIO.setup(13,GPIO.OUT)
GPIO.output(13,GPIO.HIGH)

GPIO.setup(15,GPIO.OUT)
GPIO.output(15,GPIO.HIGH)

GPIO.setup(16,GPIO.OUT)
GPIO.output(16,GPIO.HIGH)

GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.HIGH)

GPIO.setup(22,GPIO.OUT)
GPIO.output(22,GPIO.HIGH)




def initialize_boards():
	GPIO.output(7,GPIO.LOW)
	GPIO.output(11,GPIO.LOW)
	GPIO.output(12,GPIO.LOW)
	GPIO.output(13,GPIO.LOW)
	GPIO.output(15,GPIO.LOW)
	GPIO.output(16,GPIO.LOW)
	GPIO.output(18,GPIO.LOW)
	GPIO.output(22,GPIO.LOW)
	spi.writebytes(init_bytes_1)
	
	GPIO.output(7,GPIO.HIGH)
	GPIO.output(11,GPIO.HIGH)
	GPIO.output(12,GPIO.HIGH)
	GPIO.output(13,GPIO.HIGH)
	GPIO.output(15,GPIO.HIGH)
	GPIO.output(16,GPIO.HIGH)
	GPIO.output(18,GPIO.HIGH)
	GPIO.output(22,GPIO.HIGH)

	GPIO.output(7,GPIO.LOW)
	GPIO.output(11,GPIO.LOW)
	GPIO.output(12,GPIO.LOW)
	GPIO.output(13,GPIO.LOW)
	GPIO.output(15,GPIO.LOW)
	GPIO.output(16,GPIO.LOW)
	GPIO.output(18,GPIO.LOW)
	GPIO.output(22,GPIO.LOW)
	spi.writebytes(init_bytes_2)

	GPIO.output(7,GPIO.HIGH)
	GPIO.output(11,GPIO.HIGH)
	GPIO.output(12,GPIO.HIGH)
	GPIO.output(13,GPIO.HIGH)
	GPIO.output(15,GPIO.HIGH)
	GPIO.output(16,GPIO.HIGH)
	GPIO.output(18,GPIO.HIGH)
	GPIO.output(22,GPIO.HIGH)
	





def Read(board,channel):
	GPIO.output(board,GPIO.LOW)
	spi.writebytes(channel_write,Channel_enable)
	GPIO.output(board,GPIO.HIGH)

	GPIO.output(board,GPIO.LOW)
	spi.writebytes(IO_write,Current_enable)
	GPIO.output(board,GPIO.HIGH)

	GPIO.output(board,GPIO.LOW)
	spi.writebytes(read)
	GPIO.output(board,GPIO.HIGH)

	GPIO.output(board,GPIO.LOW)
	spi.readbytes(3)
	GPIO.output(board,GPIO.HIGH)

	GPIO.output(board,GPIO.LOW)
	spi.writebytes(channel_write,Channel_disable)
	GPIO.output(board,GPIO.HIGH)

	GPIO.output(board,GPIO.LOW)
	spi.writebytes(IO_write,Current_disable)
	GPIO.output(board,GPIO.HIGH)





initialize_boards()





