## Paired with temp_sensor.py on other RPI. 

import serial, time
import RPi.GPIO as GPIO
import sys,os

ser=serial.Serial(port='/dev/serial0',baudrate=115200, bytesize=serial.EIGHTBITS, timeout=0)


relay = {7:38,8:11,9:12,10:13,11:15,12:16,13:18,14:22,15:29,16:31,17:32,
	18:33,19:36,20:37,27:35,28:40}

GPIO.setmode(GPIO.BOARD)

for key, value in relay.items():
	GPIO.setup(value,GPIO.OUT)
	GPIO.output(value,GPIO.HIGH)
	print "%s pin setup" %value

dat=''
def main():
	while True:
		pin=ser.read()
		time.sleep(0.1)	
		r=ser.inWaiting()
		pin += ser.read(r)
		
		if pin:
			pin=int(pin)
			#print pin
			#time.sleep(0.1)
			
			if pin in relay:
				GPIO.output(relay[pin],GPIO.LOW)
			elif pin/100 in relay:
				GPIO.output(relay[pin/100],GPIO.HIGH)
			else:
				pass
			pass
		else:
			pass

if __name__=='__main__':
	try:
		main()
	except KeyboardInterrupt:
		print("*Interrupted*")
		GPIO.cleanup()
		ser.close()
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

