#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
import sys, serial, os, time
import RPi.GPIO as GPIO
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from tcs import Ui_TCS
import TEMP as temp #HP sensor routine
import low_p_temp_boards as lowp
from pexpect import pxssh
import numpy as np
import PID

ser=serial.Serial(port='/dev/serial0',baudrate=115200,bytesize=serial.EIGHTBITS,timeout=0)

#Relay:GPIO pin
relay={1:29,2:31,3:32,4:33,5:36,6:37,7:38,8:11,9:12,10:13,11:15,12:16,13:18,14:22,
	15:29,16:31,17:32,18:33,19:36,20:37,27:35,28:40}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

lnk = pxssh.pxssh()
hn = '10.212.212.70'
us = 'fhire'
pw = 'WIROfhire17'
lnk.login(hn,us,pw)
lnk.sendline('python Desktop/FHiRE-TCS/relay_feed.py')
#lnk.prompt()
print('SSH set up with tcsP2. Relay_feed.py running.')


def GPIO_setup(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin,GPIO.HIGH)
	print "%s pin setup" %pin

def blockPrint():
	sys.stdout = open(os.devnull,'w')
def enablePrint():
	sys.stdout = sys.__stdout__

#Update parameters according to the configuration file (option to change PID parameters w/out restarting script):
def readConfig():
	global targetT
	with open ('/tmp/pid.conf','r') as f:
		config=f.readline().split(',')
		pid.SetPoint=float(config[0]) #capability to change target temp.
		targetT=pid.SetPoint
		pid.setKp=float(config[1])
		pid.setKi=float(config[2])
		pid.setKd=float(config[3])

def createConfig():
	if not os.path.isfile('/tmp/pid.conf'):
		with open ('/tmp/pid.conf','w') as f:
			f.write('%s,%s,%s,%s' %(targetT,P,I,D))

hp = temp.TEMP() #TEMP class of HP sensors 
lp = lowp.LP() #LP class for LP boards

for key, value in relay.items():
	if key <= 6:
		GPIO_setup(value)		

class MainWindow(QtWidgets.QMainWindow, Ui_TCS):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)
		
		self.hpthread = HPSensorThread()
		self.hpthread.start()
		self.hpthread.signal.connect(self.hp_update)

		self.lpthread = LPSensorThread()
		self.lpthread.start()
		self.lpthread.signal.connect(self.lp_update)

		self.pwmthread = []
		for x in range(6):
			self.pwmthread.append(LPpwmThread(x+21,0.1,0))
			self.pwmthread[x].start()

		self.cb_hp2.setText("off")
		self.cb_hp7.setText("off")
		self.cb_hp10.setText("off")

		self.PWM_setup()
		self.PID_setup()

	def PWM_setup(self):
		self.pwm = []
		for x in range(28):
			x +=1
			if x <= 5 or x == 7:
				self.pwm.append(GPIO.PWM(relay[x],0.1)) #update every 10 sec
				if x == 7:
					x = 6
				self.pwm[x-1].start(100)
			elif 8 <= x <= 20 or x in [6,27,28]:
				pass #PWM setup in relay_feed.py
			elif 21 <= x <= 26:
				pass #PWM setup in LPpwmThread

	def PID_setup(self):
		targetT = 26
		P = 10
		I = 1
		D = 1

		self.pid = []
		for x in range(28):
			self.pid.append(PID.PID(P,I,D))
			self.pid[x].SetPoint = targetT
			self.pid[x].setSampleTime(1)

	def hp_update(self, data):
		objects = {
			0: self.cb_hp1,
			1: self.cb_hp3, 
			2: self.cb_hp4,
			3: self.cb_hp5,
			4: self.cb_hp6,
			5: self.cb_hp8,
			6: self.cb_hp9} 
			#7: self.cb_hp8.setText("%.2f C" %data[1]),
			#8: self.cb_hp9.setText("%.2f C" %data[1]),
			#9: self.cb_hp10.setText("%.2f C" %data[1])} 
		if data[0] in objects.keys():
			pre = objects[data[0]].text()
			pre = pre.split(':')[0]
			time.sleep(0.01)
			objects[data[0]].setText(pre+": %.2f C" %data[1])

	def lp_update(self, data):
		#Rstatus = data[2]
		data = data[0:2]

		objects = {
			0: self.cb_lp1_top,
			1: self.cb_lp2_top, 
			2: self.cb_lp3_top,
			3: self.cb_lp4_top,
			4: self.cb_lp5_top,
			5: self.cb_lp6_top,
			6: self.cb_lp7_top,
			7: self.cb_lp8_top,
			8: self.cb_lp9_top, 
			9: self.cb_lp10_top,
			10: self.cb_lp11_top,
			11: self.cb_lp12_top,
			12: self.cb_lp13_top,
			13: self.cb_lp14_top,
			14: self.cb_lp15_top,
			15: self.cb_lp16_top,
			16: self.cb_lp17_top, 
			17: self.cb_lp18_top,
			18: self.cb_lp19_top,
			19: self.cb_lp20_top,
			20: self.cb_lp21_top_2,

			21: self.cb_lp1_btm,
			22: self.cb_lp2_btm,
			23: self.cb_lp3_btm,
			24: self.cb_lp4_btm,
			25: self.cb_lp5_btm,
		
			#26: ,
			#27: , 
			#28: ,

			29: self.cb_lp6_btm,
			30: self.cb_lp7_btm,
			31: self.cb_lp8_btm,
			32: self.cb_lp9_btm,
			33: self.cb_lp10_btm,
			34: self.cb_lp11_btm,
			35: self.cb_lp12_btm,
			36: self.cb_lp13_btm,
			37: self.cb_lp14_btm,
			38: self.cb_lp15_btm, 
			39: self.cb_lp16_btm,
			40: self.cb_lp17_btm,
			41: self.cb_lp18_btm,
			42: self.cb_lp19_btm,
			43: self.cb_lp20_btm,
			44: self.cb_lp21_btm,
			45: self.cb_lp22_btm,
			46: self.cb_lp23_btm,
			47: self.cb_lp24_btm, 
			48: self.cb_lp25_btm,
			49: self.cb_lp26_btm,
			50: self.cb_lp27_btm,
			51: self.cb_lp28_btm,
			52: self.cb_lp29_btm,
			53: self.cb_lp30_btm,
			54: self.cb_lp31_btm}

			#55: ,
			#56: , 
			#57: ,
			#58: ,
			#59: ,
			#60: }

		#LP diodes matched with heating pads and PID loops
		LPHeating = {0:[3,0],2:[6,1],4:[9,2],6:[12,3],7:[2,4],9:[5,5],11:[8,6],
			13:[11,7],14:[1,8],16:[4,9],18:[7,10],20:[10,11],21:[14,12],
			23:[17,13],25:[20,14],30:[23,15],32:[26,16],33:[15,17],35:[18,18],
			37:[21,19],39:[24,20],40:[16,21],42:[19,22],44:[22,23],46:[25,24],
			48:[27,25],50:[13,26],53:[28,27]}

		relay = {1:self.lb_h1_top,2:self.lb_h2_top,3:self.lb_h3_top,4:self.lb_h4_top,
			5:self.lb_h5_top,6:self.lb_h6_top,7:self.lb_h7_top,8:self.lb_h8_top,
			9:self.lb_h9_top,10:self.lb_h10_top,11:self.lb_h11_top,12:self.lb_h12_top,
			13:self.lb_h1,14:self.lb_h2,15:self.lb_h3,16:self.lb_h4,17:self.lb_h5,
			18:self.lb_h6,19:self.lb_h7,20:self.lb_h8,21:self.lb_h9,22:self.lb_h10,
			23:self.lb_h11,24:self.lb_h12,25:self.lb_h13,26:self.lb_h14,27:self.lb_h15,
			28:self.lb_h16}

		
		#if data[0] in objects.keys() and objects[data[0]].isChecked() == True:
		if data[0] in objects.keys():
			pre = objects[data[0]].text()
			pre = pre.split(':')[0]
			time.sleep(0.01)
			if data[1] == 11111:
				objects[data[0]].setText("N/C")
			else:
				objects[data[0]].setText(pre+": %.2f C" %data[1])

		
		if data[0] in LPHeating.keys():
			loop = LPHeating[data[0]][1]
			heat = LPHeating[data[0]][0]
			self.pid[loop].update(data[1])
			control = self.pid[loop].output
			control = max(min(int(control),100),0)
			relay[heat].setText(str(control)+chr(37))

			if 8 <= heat <= 20 or heat in [6,27,28]:
				blockPrint()
				ser.write(str(heat)+" "+str(control))
				enablePrint()
			elif heat <= 5 or heat == 7:
				self.pwm[loop].ChangeDutyCycle(100-control)
			elif 21 <= heat <=26:
				self.pwmthread[heat-21].signal.emit([heat,0.1,control])
				#print 'LP PWM INITIATE! %s' %control

	def closeEvent(self,event):
		reply = QtWidgets.QMessageBox.question(self,'Window Close', 'Are you sure you want to close the window?',
			QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.Yes:
			self.lpthread.stop(); self.hpthread.stop()
			for x in range(28):
				x += 1
				if x <= 6:
					self.pwm[x-1].stop()
				elif x == 7:
					blockPrint()
					ser.write('1111 1')
					enablePrint()
				elif 21 <= x <= 26:
					self.pwmthread[x-21].stop()
			GPIO.cleanup()
			event.accept()
			print 'Window Closed'
		else:
			event.ignore()
		
			

class HPSensorThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self):
		QThread.__init__(self)
	
	def run(self):
		while True:
			for s in range(7):
				hptemp = hp.getTemp(s)
				self.signal.emit([s,hptemp])
				time.sleep(1)
	def stop(self):
		self.terminate()

class LPSensorThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self):
		QThread.__init__(self)

	def run(self):
		for s in range(61): #9 LP outside (sensor#27-29,56-61)
			if s in [26,27,28,55,56,57,58,59,60]:
				pass
			else:
				lpboard = lp.getTemp(s)
				time.sleep(0.01)

		while True:
			for s in range(61): #9 LP outside (sensor#27-29,56-61)
				if s in [26,27,28,55,56,57,58,59,60]:
					pass
				else:
					lptemp = []		
					for x in range(10):
						lpboard = lp.getTemp(s)
						lptemp.append(lpboard)
						time.sleep(0.01)
					lptemp = np.average(lptemp)
					#print 'Sensor %s: %.5s' %(s,lptemp)
					self.signal.emit([s,lptemp])
					time.sleep(0.1)	
	def stop(self):
		self.terminate()

class LPpwmThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	
	def __init__(self,sensor,freq,control):
		QThread.__init__(self)
		self.sensor = sensor
		self.freq = freq
		self.timeON = control/(100*freq)
		self.timeOFF = (100-control)/(100*freq)
		print 'PWM thread created: %s' %[sensor,freq,control]

	def run(self):
		while True:
			tic = time.clock()

			self.signal.connect(self.update)
			time.sleep(0.1)

			if self.timeON > 0:
				lp.Relay_ON(self.sensor)
				elapsed = time.clock() - tic
				print 'Relay %s ON: %s' %(self.sensor, self.timeON - elapsed)
				time.sleep(self.timeON - elapsed)
	
			tic = time.clock()

			if self.timeOFF > 0:
				lp.Relay_OFF(self.sensor)
				elapsed = time.clock() - tic
				print 'Relay %s OFF: %s' %(self.sensor, self.timeOFF - elapsed)
				time.sleep(self.timeOFF - elapsed)

	def stop(self):
		lp.Relay_OFF(self.sensor)
		self.terminate()

	def update(self,data):
		self.sensor = data[0]
		self.freq = data[1]
		control = data[2]
		self.timeON = control/(100*self.freq)
		self.timeOFF = (100-control)/(100*self.freq)
		time.sleep(0.1)				

#PID loop will operate automatically and toggle relays. For now, just have the functionallity to manually toggle relays?
def main():
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())

if __name__=='__main__':
	main()


