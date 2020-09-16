import serial, time
import RPi.GPIO as GPIO
import sys,os

ser=serial.Serial(port='/dev/serial0',baudrate=115200, bytesize=serial.EIGHTBITS, timeout=0)

#relay#:[GPIO,index]
relay = {7:[38,0],8:[11,1],9:[12,2],10:[13,3],11:[15,4],12:[16,5],13:[18,6],
	14:[22,7],15:[29,8],16:[31,9],17:[32,10],18:[33,11],19:[36,12],
	20:[37,13],27:[35,14],28:[40,15]}

GPIO.setmode(GPIO.BOARD)

#Setup PWM for RPi2 relays
pwm = []
for key, value in relay.items():
	GPIO.setup(value[0],GPIO.OUT)
	GPIO.output(value[0],GPIO.HIGH)
	pwm.append(GPIO.PWM(value[0],0.5))

for x in range(len(pwm)):
	pwm[x].start(100)

def main():
	while True:
		#Read message from RPi1 via UART comm.
		pin=ser.read()
		time.sleep(0.1)	
		r=ser.inWaiting()
		pin += ser.read(r)
			
		if pin:
			back = pin.split()
			
			#Stop all PWM comm. and cleanup GPIO pins - exit
			if pin == '1111 1':
				for x in range(len(pwm)):
					pwm[x].stop()
				GPIO.cleanup()
				sys.exit()
			
			#Update PWM with new duty cycle
			elif int(back[0]) in relay:
				loop = relay[int(back[0])][1]
				control = int(back[1])
				pwm[loop].ChangeDutyCycle(100-control)	
		else:
			pass

if __name__=='__main__':
	main()

