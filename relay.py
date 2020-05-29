import RPi.GPIO as GPIO
import sys,os

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.OUT) #HR1
GPIO.output(29,GPIO.HIGH)

GPIO.setup(31,GPIO.OUT) #HR2
GPIO.output(31,GPIO.HIGH)

GPIO.setup(33,GPIO.OUT) #HR3
GPIO.output(33,GPIO.HIGH)

GPIO.setup(36,GPIO.OUT) #HR4
GPIO.output(36,GPIO.HIGH)

GPIO.setup(37,GPIO.OUT) #HR5
GPIO.output(37,GPIO.HIGH)

GPIO.setup(32,GPIO.OUT) #HR7
GPIO.output(32,GPIO.HIGH)

def main():
	while True:
		command=raw_input("Turn relay on/off[N]: ")
		if command=="on1": 
			GPIO.output(29,GPIO.LOW)
			print("Relay 1 turned ON")
		elif command=="off1":
			GPIO.output(29,GPIO.HIGH)
			print("Relay 1 turned OFF")
		elif command=="on2":
			GPIO.output(31,GPIO.LOW)
			print("Relay 2 turned ON")
		elif command=="off2":
			GPIO.output(31,GPIO.HIGH)
			print("Relay 2 turned OFF")
		elif command=="on3":
			GPIO.output(33,GPIO.LOW)
			print("Relay 3 turned ON")
		elif command=="off3":
			GPIO.output(33,GPIO.HIGH)
			print("Relay 3 turned OFF")
		elif command=="on4":
			GPIO.output(36,GPIO.LOW)
			print("Relay 4 turned ON")
		elif command=="off4":
			GPIO.output(36,GPIO.HIGH)
			print("Relay 4 turned OFF")
		elif command=="on5":
			GPIO.output(37,GPIO.LOW)
			print("Relay 5 turned ON")
		elif command=="off5":
			GPIO.output(37,GPIO.HIGH)
			print("Relay 5 turned OFF")
		elif command=="on7":
			GPIO.output(32,GPIO.LOW)
			print("Relay 7 turned ON")
		elif command=="off7":
			GPIO.output(32,GPIO.HIGH)
			print("Relay 7 turned OFF")
		else:
			GPIO.cleanup()
			print("ERROR: Ending program")
			break

if __name__=='__main__':
	try:
		main()
	except KeyboardInterrupt:
		print(" *Interrupted*")
		GPIO.cleanup()
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
