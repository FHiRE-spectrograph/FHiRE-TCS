## Paired with temp_sensor.py on other RPI. 

import serial, time
import RPi.GPIO as GPIO
import sys,os

ser=serial.Serial(port='/dev/serial0',baudrate=115200, bytesize=serial.EIGHTBITS, timeout=0)
#ser=serial.Serial(port='/dev/ttyUSB0',baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

GPIO.setmode(GPIO.BOARD)
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

GPIO.setup(29,GPIO.OUT) 
GPIO.output(29,GPIO.HIGH)

GPIO.setup(31,GPIO.OUT) 
GPIO.output(31,GPIO.HIGH)

GPIO.setup(32,GPIO.OUT) 
GPIO.output(32,GPIO.HIGH)

GPIO.setup(33,GPIO.OUT) 
GPIO.output(33,GPIO.HIGH)

GPIO.setup(36,GPIO.OUT) 
GPIO.output(36,GPIO.HIGH)

GPIO.setup(38,GPIO.OUT) 
GPIO.output(38,GPIO.HIGH)

'''
def on(pin):
	GPIO.output(pin,GPIO.LOW)
	print("Relay %.f turned ON" %pin)

def off(pin):
	GPIO.output(x,GPIO.HIGH)
	print("Relay %.f turned OFF" %pin)

def toggle(pin):
	state=GPIO.input(pin)
	if (state is True): #on?
'''	

dat=''
def main():
	while True:
		'''
		pin=ser.read()
		time.sleep(0.5)	
		r=ser.inWaiting()
		pin+=ser.read(r)
		#print(pin)
		'''
	#print(hr)
		
		pin=raw_input("Turn relay on/off[N]: ").strip("\r\n")

		if pin=="on2":
			GPIO.output(7,GPIO.LOW)
			print("Relay 2 turned ON")
		elif pin=="off2":
			GPIO.output(7,GPIO.HIGH)
			print("Relay 2 turned OFF")
		elif pin=="on3":
			GPIO.output(38,GPIO.LOW)
			print("Relay 2 turned ON")
		elif pin=="off3":
			GPIO.output(38,GPIO.HIGH)
			print("Relay 2 turned OFF")


if __name__=='__main__':
	try:
		main()
	except KeyboardInterrupt:
		print("*Interrupted*")
		GPIO.cleanup()
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

ser.close()
