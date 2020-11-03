import sys, serial, os, time, datetime, pytz
import RPi.GPIO as GPIO
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from tcs import Ui_TCS
import TEMP as temp #HP sensor routine
import low_p_temp_boards as lowp
from pexpect import pxssh
import numpy as np
import PID

import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

############################################################
# Setup
############################################################

ser=serial.Serial(port='/dev/serial0',baudrate=115200,bytesize=serial.EIGHTBITS,timeout=0)

#Relay:GPIO pin
#relay={1:29,2:31,3:32,4:33,5:36,6:37,7:38,8:11,9:12,10:13,11:15,12:16,13:18,14:22,
#	15:29,16:31,17:32,18:33,19:36,20:37,27:35,28:40}

relay={1:29,2:31,3:32,4:33,5:36,6:37,7:7,8:11,9:12,10:13,11:15,12:16,13:18,14:22,
	15:29,16:31,17:32,18:33,19:36,20:37,27:35,28:40}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#Setup communication with RPi2 in order to have access to its relays
lnk = pxssh.pxssh()
hn = '10.212.212.70'
us = 'fhire'
pw = 'WIROfhire17'
lnk.login(hn,us,pw)
lnk.sendline('python Desktop/FHiRE-TCS/relay_feed.py')
lnk.prompt()
print('SSH set up with tcsP2. Relay_feed.py running.')

#Used to remove byte messages during UART comm.
def blockPrint():
	sys.stdout = open(os.devnull,'w')
def enablePrint():
	sys.stdout = sys.__stdout__

hp = temp.TEMP() #TEMP class for reading HP sensors 
lp = lowp.LP() #LP class for reading LP boards

#Setup relays on RPi1
def GPIO_setup(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin,GPIO.HIGH)
	print "%s pin setup" %pin

for key, value in relay.items():
	if key <= 6:
		GPIO_setup(value)

start = time.time()		

#Main PyQt5 window
class MainWindow(QtWidgets.QMainWindow, Ui_TCS):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)
		
		self.hpthread = HPSensorThread()
		self.hpthread.start()
		#self.hpthread.signal.connect(self.hp_update)
		#self.hpthread.signal2.connect(self.timer_update)

		self.lpthread = LPSensorThread()
		self.lpthread.start()
		self.lpthread.signal.connect(self.PID_update)
		self.lpthread.signal2.connect(self.timer_update)

		self.pwmthread = []
		for x in range(6):
			self.pwmthread.append(LPpwmThread(x+21,0.1,0))
			self.pwmthread[x].start()
			time.sleep(0.1)

		#Show HP sensors 2,7,10 as off
		self.cb_hp2.setText("off")
		self.cb_hp7.setText("off")
		self.cb_hp10.setText("off")

		self.PWM_setup()
		self.PID_setup()

		self.pb_graph.pressed.connect(self.graph)
		self.lay = QtWidgets.QVBoxLayout(self.graphWidget)
		self.lay.setContentsMargins(0,0,0,0)
		
		self.hp_sensors = {
			0:[self.cb_hp1,1],
			1:[self.cb_hp3,3], 
			2:[self.cb_hp4,4],
			3:[self.cb_hp5,5],
			4:[self.cb_hp6,6],
			5:[self.cb_hp8,8],
			6:[self.cb_hp9,9]} 
			#7: self.cb_hp8.setText("%.2f C" %data[1]),
			#8: self.cb_hp9.setText("%.2f C" %data[1]),
			#9: self.cb_hp10.setText("%.2f C" %data[1])} 

		self.lp_sensors = {
			0: self.cb_lp1_top, #TD-01
			1: self.cb_lp2_top, #TR-02
			2: self.cb_lp3_top, #TD-03
			3: self.cb_lp4_top, #TR-04
			4: self.cb_lp5_top, #TD-05
			5: self.cb_lp6_top, #TR-06
			6: self.cb_lp7_top, #TD-07
			7: self.cb_lp8_top, #TD-08
			8: self.cb_lp9_top, #TR-09
			9: self.cb_lp10_top, #TD-10
			10: self.cb_lp11_top, #TR-11
			11: self.cb_lp12_top, #TD-12
			12: self.cb_lp13_top, #TR-13
			13: self.cb_lp14_top, #TD-14
			14: self.cb_lp15_top, #TD-15
			15: self.cb_lp16_top, #TR-16
			16: self.cb_lp17_top, #TD-17
			17: self.cb_lp18_top, #TR-18
			18: self.cb_lp19_top, #TD-19
			19: self.cb_lp20_top, #TR-20
			20: self.cb_lp21_top_2, #TD-21

			21: self.cb_lp1_btm, #BD-22
			22: self.cb_lp2_btm, #BR-23
			23: self.cb_lp3_btm, #BD-24
			24: self.cb_lp4_btm, #BR-25
			25: self.cb_lp5_btm, #BD-26
		
			#26: ,
			#27: , 
			#28: ,

			29: self.cb_lp6_btm, #BR-30
			30: self.cb_lp7_btm, #BD-31
			31: self.cb_lp8_btm, #BR-32
			32: self.cb_lp9_btm, #BD-33
			33: self.cb_lp10_btm, #BD-34
			34: self.cb_lp11_btm, #BR-35
			35: self.cb_lp12_btm, #BD-36
			36: self.cb_lp13_btm, #BR-37
			37: self.cb_lp14_btm, #BD-38
			38: self.cb_lp15_btm, #BR-39
			39: self.cb_lp16_btm, #BD-40
			40: self.cb_lp17_btm, #BD-41
			41: self.cb_lp18_btm, #BR-42
			42: self.cb_lp19_btm, #BD-43
			43: self.cb_lp20_btm, #BR-44
			44: self.cb_lp21_btm, #BD-45
			45: self.cb_lp22_btm, #BR-46
			46: self.cb_lp23_btm, #BD-47
			47: self.cb_lp24_btm, #BR-48
			48: self.cb_lp25_btm, #BD-49
			49: self.cb_lp26_btm, #BR-50
			50: self.cb_lp27_btm, #BD-51
			51: self.cb_lp28_btm, #BR-52
			52: self.cb_lp29_btm, #BR-53
			53: self.cb_lp30_btm, #BD-54
			54: self.cb_lp31_btm} #BR-55

			#55: ,
			#56: , 
			#57: ,
			#58: ,
			#59: ,
			#60: }
		
		self.fig, self.ax1 = plt.subplots()
		self.plotWidget = FigureCanvas(self.fig)
		self.lay.addWidget(self.plotWidget)

		self.addToolBar(QtCore.Qt.TopToolBarArea,NavigationToolbar(self.plotWidget,self))

#########################################################################
# PWM and PID Loop Methods
#########################################################################

	#Setup PWM controls for relays (mainly RPi1 relays)
	def PWM_setup(self):
		self.pwm = []
		for x in range(28):
			x +=1
			#if x <= 5 or x == 7:
			if x <= 6:
				#if x == 7:
				#	x = 6
				self.pwm.append(GPIO.PWM(relay[x],0.1)) #cycle every 10 sec
				self.pwm[x-1].start(100)
			#elif 8 <= x <= 20 or x in [6,27,28]:
			elif 7 <= x <= 20 or x in [27,28]:
				pass #PWM setup in relay_feed.py on RPi2
			elif 21 <= x <= 26:
				pass #PWM setup in LPpwmThread

	#Setup PID loops for each heating pad
	def PID_setup(self):
		self.pid = []
		for x in range(28):
			self.pid.append(PID.PID())
			self.readConfig(x) 
			self.pid[x].setSampleTime(1)

	#Update PID parameters according to the configuration file (option to change PID parameters w/out restarting script):
	def readConfig(self, ind):
		config = np.loadtxt('pid.conf',unpack=True,skiprows=1,usecols=(0,1,2,3,4))
		self.pid[ind].SetPoint = float(config[1,ind])
		self.pid[ind].setKp = float(config[2,ind])
		self.pid[ind].setKi = float(config[3,ind])
		self.pid[ind].setKd = float(config[4,ind])

	#Updates countdown between sensor updates
	def timer_update(self, time):
		try:
			self.timer.setText('%.2f %%\n' %time[1] +time[0])
		except:
			self.timer.setText(time)

#######################################################################
# HP and LP Temperature Methods
#######################################################################

	#Graph temperatures for given HP sensors for range specified by initial and final times
	#Sensors format: 1 3 4
	#Time format: Y-m-d H:M:S
	#Graph all measurements by keeping initial and final times unspecified
	def graph(self):
		Averaging()

		hp_file = 'tempLog.dat'
		lpr_file = 'LPresistorsLog.dat'
		lpd_file = 'LPdiodesLog.dat'
		avg_file = 'averageTemp.dat'

		#hp_file = './runtime/tempLog_10222020_19h.dat'
		#lpr_file = './runtime/LPresistorsLog_10222020_19h.dat'
		#lpd_file = './runtime/LPdiodesLog_10222020_19h.dat'

		hp = np.loadtxt(hp_file,unpack=True,skiprows=1)
		lpr = np.loadtxt(lpr_file,unpack=True,skiprows=1)
		lpd = np.loadtxt(lpd_file,unpack=True,skiprows=1)
		avgT = np.loadtxt(avg_file,unpack=True,skiprows=1)

		try:
			utc = hp[0,:]

		except:
			print "Not enough values recorded (>1)."
			return

		try:
			utcr = lpr[0,:]
			utcd = lpd[0,:]	
		except:
			print "Not enough values recorded (>1)."
			return			

		#self.sensors = self.ln_sensor.text()
		self.time_initial = self.ln_to.text()
		self.time_final = self.ln_tf.text()

		if not self.time_initial and not self.time_final:
			hp_index1 = lpr_index1 = lpd_index1 = 0 
			hp_index2 = lpr_index2 = lpd_index2 = None

		diode_column = {1:1,3:2,5:3,7:4,8:5,10:6,12:7,14:8,15:9,17:10,19:11,21:12,
			22:13,24:14,26:15,31:16,33:17,34:18,36:19,38:20,40:21,41:22,43:23,
			45:24,47:25,49:26,51:27,54:28}
		resistor_column = {2:1,4:2,6:3,9:4,11:5,13:6,16:7,18:8,20:9,23:10,25:11,
			30:12,32:13,35:14,37:15,39:16,42:17,44:18,46:19,48:20,50:21,52:22,53:23,55:24}
		hp_column =  {1:1,3:2,4:3,5:4,6:5,8:6,9:7} #HPsensor:column
		
		if self.ln_sensor.text() == 'all':
			red = 'background-color:#ff9999'
			orange = 'background-color:#ffcc99'
			yellow = 'background-color:#ffff99'
			lightgreen = 'background-color:#ccff99'
			green = 'background-color:#99ff99'
			for x in self.lp_sensors.keys():
				x += 1
				if x in diode_column.keys():					
					y = lpd[diode_column.get(x),:]
				elif x in resistor_column.keys():
					y = lpr[resistor_column.get(x),:]

				avg = np.nanmean(y)
				rms = np.sqrt(np.nanmean((y-avg)**2))
				rms = rms*10**3
			
				if rms < 30 and rms > 0:
					style = green
				elif rms >= 30 and rms < 60:
					style = lightgreen
				elif rms >=60 and rms < 1000:
					style = yellow
				elif rms >= 1000 and rms < 2000:
					style = orange
				elif rms >= 2000:
					style = red
				elif rms == 0:
					style = 'background-color:lightgrey'

				self.lp_sensors[x-1].setStyleSheet(style)

			for x in self.hp_sensors.keys():
				s = self.hp_sensors[x][1]
				y = hp[hp_column.get(s),:]

				avg = np.nanmean(y)
				rms = np.sqrt(np.nanmean((y-avg)**2))
				rms = rms*10**3
			
				if rms < 30 and rms > 0:
					style = green
				elif rms >= 30 and rms < 60:
					style = lightgreen
				elif rms >= 60 and rms < 1000:
					style = yellow
				elif rms >= 1000 and rms < 2000:
					style = orange
				elif rms >= 2000:
					style = red
				elif rms == 0:
					style = 'background-color:lightgrey'

				self.hp_sensors[x][0].setStyleSheet(style)
			return
		self.ax1.cla()

		avg_sensors = [int(n) for n in self.ln_sensor.text().split()]

		for x in range(28):
			x += 1
			x2 = avgT[0,:]/3600
			y = avgT[x,:]
			avg = np.nanmean(y)
			rms = np.sqrt(np.nanmean((y-avg)**2))
			rms = rms*10**3

			#print('PID %s: %.2fC (RMS:%.2fmK)' %(x,avg,rms))
			if x in avg_sensors:
				self.ax1.plot(x2,y,label="PID%s:RMS=%.2fmK" %(x,rms))	


		lp_checked = []; hp_checked = []
		for x in self.lp_sensors.keys():
			if self.lp_sensors[x].isChecked():
				lp_checked.append(x+1)
				
		for x in self.hp_sensors.keys():
			if self.hp_sensors[x][0].isChecked():
				hp_checked.append(self.hp_sensors[x][1])

		hp_col = []; lpr_col = []; lpd_col = []
		lpr_checked = []; lpd_checked =[]
		if lp_checked:
			for x in lp_checked:
				if x in diode_column.keys():
					lpd_col.append(diode_column.get(x))
					lpd_checked.append(x)
					
				elif x in resistor_column.keys():
					lpr_col.append(resistor_column.get(x))
					lpr_checked.append(x)
		if hp_checked:
			for x in hp_checked:
				hp_col.append(hp_column.get(x))	
	
		if self.time_initial:
			#Convert given date & time to local epoch seconds
			to = self.time_initial.split()
			date1 = to[0].split("-")
			time1 = to[1].split(":")
			for x in range(len(date1)):
				date1[x] = int(date1[x])
			for x in range(len(time1)):
				time1[x] = int(time1[x])
			try:
				utc1 = datetime.datetime(date1[0],date1[1],date1[2],time1[0],time1[1],time1[2]).strftime("%s") #local time 
			except:
				#print "Improper initial time."
				pass
			utc1 = float(utc1)

			
			#Find closest time in tempLog.dat and get index
			hp_index1 = min(range(len(utc)), key=lambda i: abs(utc[i]-utc1))
			lpr_index1 = min(range(len(utcr)), key=lambda i: abs(utcr[i]-utc1))
			lpd_index1 = min(range(len(utcd)), key=lambda i: abs(utcd[i]-utc1))

		if self.time_final:
			tf = self.time_final.split()
			date2 = tf[0].split("-")
			time2 = tf[1].split(":")
			for x in range(len(date2)):
				date2[x] = int(date2[x])
			for x in range(len(time2)):
				time2[x] = int(time2[x])
			try:
				utc2 = datetime.datetime(date2[0],date2[1],date2[2],time2[0],time2[1],time2[2]).strftime("%s") #local time 
			except:
				#print "Improper final time."
				pass
			utc2 = float(utc2)

			hp_index2 = min(range(len(utc)), key=lambda i: abs(utc[i]-utc2))
			lpr_index2 = min(range(len(utcr)), key=lambda i: abs(utcr[i]-utc2))
			lpd_index2 = min(range(len(utcd)), key=lambda i: abs(utcd[i]-utc2))

		

		if hp_col:
			for i in range(len(hp_col)):
				x = utc[hp_index1:hp_index2]/3600
				y =  hp[hp_col[i],hp_index1:hp_index2]
				avg = np.nanmean(y)
				rms = np.sqrt(np.nanmean((y-avg)**2))
				rms = rms*10**3 #rms in mK
				self.ax1.plot(x,y,label="HP%s:RMS=%.2fmK" %(hp_checked[i],rms))
		if lpr_col:
			for i in range(len(lpr_col)):
				x = utcr[lpr_index1:lpr_index2]/3600
				y =  lpr[lpr_col[i],lpr_index1:lpr_index2]
				avg = np.nanmean(y)
				rms = np.sqrt(np.nanmean((y-avg)**2))
				rms = rms*10**3 #rms in mK
				self.ax1.plot(x,y,label="LP%s:RMS=%.2fmK" %(lpr_checked[i],rms))
		if lpd_col:
			for i in range(len(lpd_col)):
				x = utcd[lpd_index1:lpd_index2]/3600
				y =  lpd[lpd_col[i],lpd_index1:lpd_index2]
				avg = np.nanmean(y)
				rms = np.sqrt(np.nanmean((y-avg)**2))
				rms = rms*10**3 #rms in mK
				self.ax1.plot(x,y,label="LP%s:RMS=%.2fmK" %(lpd_checked[i],rms))

		self.fig.canvas.draw_idle()

		self.ax1.set_xlabel("Time (h)"); self.ax1.set_ylabel("Temperature [C]")
		self.ax1.legend(loc="upper right")

	def PID_update(self):
		Averaging()
		avg_file = 'averageTemp.dat'
		avgT = np.loadtxt(avg_file,unpack=True,skiprows=1)
		avgT = np.transpose(avgT)
		if len(avgT) == 29:
			avgT = avgT[1:29]
		else:
			avgT = avgT[-1,1:29]

		relay = {1:self.lb_h1_top,2:self.lb_h2_top,3:self.lb_h3_top,4:self.lb_h4_top,
			5:self.lb_h5_top,6:self.lb_h6_top,7:self.lb_h7_top,8:self.lb_h8_top,
			9:self.lb_h9_top,10:self.lb_h10_top,11:self.lb_h11_top,12:self.lb_h12_top,
			13:self.lb_h1,14:self.lb_h2,15:self.lb_h3,16:self.lb_h4,17:self.lb_h5,
			18:self.lb_h6,19:self.lb_h7,20:self.lb_h8,21:self.lb_h9,22:self.lb_h10,
			23:self.lb_h11,24:self.lb_h12,25:self.lb_h13,26:self.lb_h14,27:self.lb_h15,
			28:self.lb_h16}
	
		for x in range(len(avgT)):
			heat = x + 1
			self.pid[x].update(avgT[x])
			control = self.pid[x].output
			control = max(min(float(control),10),0) #10% limit -- is this low enough?
			relay[x+1].setText(str(control)+chr(37))
			control = 25


			if 7 <= heat <= 20 or heat in [27,28]: #Rpi 2
				pass
				#control = control + 2*heat
				#print('PID %s: %s%% (%ss)' %(heat,control,(control*0.1)))
				#blockPrint()
				#ser.write(str(heat)+" "+str(control))
				#enablePrint()
				
				#pin = ser.read()
				#time.sleep(0.1)
				#r = ser.inWaiting()
				#pin += ser.read(r)
				#if pin:
				#	print(pin)

			elif heat <= 6: #Rpi 1
				pass
				#print('PID %s: %s%%' %(heat,control))
				#if heat == 7:
				#	heat = 6
				#self.pwm[heat-1].ChangeDutyCycle(100-control)

			elif 21 <= heat <=26: #LP boards
				#pass
				control = control + 2*heat
				print('PID %s: %s%%' %(heat,control))
				self.pwmthread[heat-21].signal.emit([heat,0.1,control])

			self.readConfig(x) #Update PID coefficients and target temp
		

	#Terminates all QThreads, toggles all relays off, and cleans up GPIO pins
	def closeEvent(self,event):
		reply = QtWidgets.QMessageBox.question(self,'Window Close', 'Are you sure you want to close the window?',
			QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.Yes:
			self.lpthread.stop(); 
			self.hpthread.stop()
			for x in range(28):
				x += 1
				if x <= 6:
					self.pwm[x-1].stop()
				elif x == 7:
					blockPrint()
					ser.write('1111 1')
					enablePrint()
				elif 21 <= x <= 26:
				#elif 21 <= x <= 22:
					self.pwmthread[x-21].stop()
			plt.close('all')
			GPIO.cleanup()
			event.accept()
			print 'Window Closed'
		else:
			event.ignore()

def Averaging():
	lpr_file = 'LPresistorsLog.dat'
	lpd_file = 'LPdiodesLog.dat'
	lpr = np.loadtxt(lpr_file,unpack=True,skiprows=1)
	lpd = np.loadtxt(lpd_file,unpack=True,skiprows=1)

	diode_column = {1:1,3:2,5:3,7:4,8:5,10:6,12:7,14:8,15:9,17:10,19:11,21:12,
		22:13,24:14,26:15,31:16,33:17,34:18,36:19,38:20,40:21,41:22,43:23,
		45:24,47:25,49:26,51:27,54:28}
	resistor_column = {2:1,4:2,6:3,9:4,11:5,13:6,16:7,18:8,20:9,23:10,25:11,
		30:12,32:13,35:14,37:15,39:16,42:17,44:18,46:19,48:20,50:21,52:22,53:23,55:24}

	#Heating pad:[Sensors], Heating pad = PID loop(?)
	LPHeating = {1:[15,16],2:[8,9],3:[1,2],4:[16,17,18],5:[9,10,11],6:[2,3,4],7:[18,19,20],8:[11,12,13],
		9:[4,5,6],10:[20,21],11:[13,14],12:[6,7],13:[26,27,28],14:[1,2],15:[2,10,18,11],16:[17,18],
		17:[2,3,11,4],18:[11,12,4,20,13],19:[28,19,11,20],20:[4,5,6,13],21:[13,14,15,22,6],
		22:[20,21,22,13],23:[6,7,8,15],24:[15,16,8,24],25:[22,23,15,24],26:[8,9],27:[24,25],28:[29,30,31]}	

	utc = lpd[0]
	utc = np.vstack((utc,lpr[0]))

	utc = np.average(utc,axis=0)

	final = []
	for x in LPHeating:
		stack = []
		for y in LPHeating[x]:
			if y in diode_column.keys():
				val = lpd[diode_column.get(y)]
			elif y in resistor_column.keys():
				val = lpr[resistor_column.get(y)]
			if y == LPHeating[x][0]:
				stack = val
			else:
				stack = np.vstack((stack,val))

		stack = np.nanmean(stack,axis=0)
		if x == 1:
			final = stack
		else:
			final = np.vstack((final,stack))

	with open('averageTemp.dat','a') as avgTemp:
		avgTemp.seek(0,1)
		avgTemp.truncate(112)

		for x in range(len(final[0])):
			avgTemp.write('%.0f		' %utc[x])
			for item in final[:,x]:
				avgTemp.write('%.4f ' %item)
			avgTemp.write('\n')
	
################################################################################
#  QThread Classes
################################################################################
			
#QThread for reading HP sensor temperatures from TEMP.py
#*Need to implement averaging sequence for HP sensors too*
class HPSensorThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	signal2 = pyqtSignal('PyQt_PyObject')

	def __init__(self):
		QThread.__init__(self)
		self.j = 0
	
	def run(self):
		#time.sleep(5)
		for s in range(7): 
			try:
				hpboard = hp.getTemp(s)
			except:
				print("Error reading HP sensor %s" %s)

		while True:
			hptemp = []
			tic = time.time()
			elapsed = 0; i = 0
			total = 10 #total time in seconds between temp/duty cycle updates

			while elapsed < total:
				elapsed = time.time() - tic

				#update countdown label
				if elapsed < total:
					statement = '%.2f/%.2f sec' %(elapsed,total)
					percent = elapsed/total*100
					self.signal2.emit([statement,percent])
				else:
					self.signal2.emit("Updating")

				averaging = []
				for s in range(7): 
					try:
						hpboard = hp.getTemp(s)
					except:
						print("Error reading HP sensor %s" %s)
						hpboard = 11111

					if hpboard >= 35 or hpboard <= 10:
						hpboard = hp.getTemp(s)

					if hpboard >= 35 or hpboard <= 10:
						if s != 3:
							#print("Sensor %s - unreasonable reading (%sC)" %((s+1),lpboard))
							hpboard = np.nan

					averaging.append(hpboard)

				if i == 0:
					hptemp = averaging
					i += 1
				else:
					hptemp = np.vstack((hptemp,averaging))
				time.sleep(0.01)

			hpstd = np.std(hptemp,axis=0)
			hptemp = np.nanmean(hptemp,axis=0)

			total_elapsed = time.time() - start

			with open('tempLog.dat','a') as tempLog:
				#current_time = datetime.datetime.now().strftime("%s") #local time
				current_time = total_elapsed
				if self.j == 0:
					tempLog.seek(0,1)
					tempLog.truncate(61)
					self.j += 1
					tempLog.write('%.0f		' %(current_time))
				else:
					tempLog.write('\n%.0f		'%(current_time))
				for item in hptemp:
					tempLog.write("%.6s " %item)

			for s in range(7):
				self.signal.emit([s,hptemp[s],hpstd[s]])

			wait = 5
			if wait*60 > total:
				#print("Waiting %s min" %wait)
				self.signal2.emit("Waiting %s min" %wait)
				time.sleep((wait*60)-total) #reading intervals 
			total_elapsed = time.time() - start
			#print("HP: %s" %total_elapsed)
			#print("HP: %s" %time.time())

	def stop(self):
		self.terminate()

#QThread for reading LP sensor temperatures from low_p_temp_boards.py
class LPSensorThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	signal2 = pyqtSignal('PyQt_PyObject')

	def __init__(self):
		QThread.__init__(self)

		self.diodes = [1,3,5,7,8,10,12,14,15,17,19,21,22,24,
			26,31,33,34,36,38,40,41,43,45,47,49,51,54] 
		self.resistors = [2,4,6,9,11,13,16,18,20,23,25,30,
			32,35,37,39,42,44,46,48,50,52,53,55] 
		self.j = 0; self.k = 0

	def run(self):
		print("Starting thread")
		#Runs through sensors once - sensors tend to return unreasonable values first run
		for s in range(61): #9 LP outside (sensor#27-29,56-61) (not wired yet)
			if s in [26,27,28,55,56,57,58,59,60]:
				pass
			else:
				try:
					lpboard = lp.getTemp(s)
				except:
					print("Error reading LP sensor %s" %s)
					pass
				time.sleep(0.05)
		print("First run")

		while True:
			lptemp = []
			tic = time.time()
			elapsed = 0; i = 0
			total = 20 #total time in seconds between temp/duty cycle updates
			#print("1")

			while elapsed < total:
				elapsed = time.time() - tic

				#update countdown label
				if elapsed < total:
					statement = '%.2f/%.2f sec' %(elapsed,total)
					percent = elapsed/total*100
					self.signal2.emit([statement,percent])
					print("%s %.0f%%" %(statement,percent))
				else:
					self.signal2.emit("Updating")
					print("Updating")

				averaging = []
				for s in range(61): #9 LP outside (sensor#27-29,56-61)
					if s in [26,27,28,55,56,57,58,59,60]:
						averaging.append(0)
					else:
						try:
							lpboard = lp.getTemp(s)
						except:
							print("Error reading sensor %s" %(s+1))
							lpboard = 11111

						#Attempt at removing unreasonable readings
						if lpboard >= 35 or lpboard <= 10:
							lpboard = lp.getTemp(s)
							if lpboard >= 35 or lpboard <= 10:
								lpboard = lp.getTemp(s)

						if lpboard == 11111 and s != 1:
							print("Sensor %s - 11111 error" %(s+1))

						if lpboard >= 35 or lpboard <= 10:
							if s != 1:
								print("Sensor %s - unreasonable reading (%sC)" %((s+1),lpboard))
							lpboard = np.nan


						averaging.append(lpboard)
						time.sleep(0.01)

				if i == 0:
					lptemp = averaging
					i += 1
				else:
					lptemp = np.vstack((lptemp,averaging))
				time.sleep(0.01)

			lpstd = np.std(lptemp,axis=0)
			lptemp = np.nanmean(lptemp,axis=0)

			s1 = s+1
			lptempD = []; lpstdD = []
			for s1 in self.diodes:
				#print("Diode Sensor %s: %s" %(s1,lptemp[s1-1]))
				lptempD.append(lptemp[s1-1])
				lpstdD.append(lpstd[s1-1])

			lptempR = []; lpstdR = []
			for s1 in self.resistors:
				#print("Resistor Sensor %s: %s" %(s1,lptemp[s1-1]))
				lptempR.append(lptemp[s1-1])
				lpstdR.append(lpstd[s1-1])

			total_elapsed = time.time() - start	

			with open('LPdiodesLog.dat','a') as tempLog:
				#current_time = datetime.datetime.now().strftime("%s") #local time
				current_time = total_elapsed
				if self.j == 0:
					tempLog.seek(0,1)
					tempLog.truncate(204)
					self.j += 1
					tempLog.write('%.0f		' %(current_time))
				else:
					tempLog.write('\n%.0f		'%(current_time))
				for item in lptempD:
					if item == np.nan:
						tempLog.write("%.6s    " %item)
					else:
						tempLog.write("%.6s " %item)
				#tempLog.write('\nstdev	')
				#for item in lptempD:
				#	item_std = lpstdD[lptempD.index(item)]
				#	tempLog.write("%.6s " %item_std)


			with open('LPresistorsLog.dat','a') as tempLog:
				#current_time = datetime.datetime.now().strftime("%s") #local time
				current_time = total_elapsed
				if self.k == 0:
					tempLog.seek(0,1)
					tempLog.truncate(176)
					self.k += 1
					tempLog.write('%.0f		' %(current_time))
				else:
					tempLog.write('\n%.0f		'%(current_time))
				for item in lptempR:
					#item_std = lpstdR[lptempR.index(item)]
					#tempLog.write("%.5s(%.4s) " %(item,item_std))
					if item == np.nan:
						tempLog.write("%.6s    " %item)
					else:
						tempLog.write("%.6s " %item)
				#tempLog.write('\nstdev	')
				#for item in lptempR:
				#	item_std = lpstdR[lptempR.index(item)]
				#	tempLog.write("%.6s " %item_std)

			wait = 5
			if wait*60 > total:
				self.signal.emit(True)
				print("Waiting %s min" %wait)
				self.signal2.emit("Waiting %s min" %wait)
				time.sleep((wait*60)-total) #reading intervals
				#Averaging()
				
			total_elapsed = time.time() - start
			#print("LP: %s" %total_elapsed)
			#print("LP: %s" %time.time())
					
	def stop(self):
		self.terminate()

#QThread of method to emulate PWM for relays on LP boards
class LPpwmThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	
	def __init__(self,sensor,freq,control):
		QThread.__init__(self)
		self.sensor = sensor
		self.freq = freq
		self.timeON = control/(100*freq)
		self.timeOFF = (100-control)/(100*freq)
		#print 'PWM thread created: %s' %[sensor,freq,control]

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
		print('Turning off %s' %self.sensor)
		lp.Relay_OFF(self.sensor)
		self.terminate()

	#Update timeON and timeOFF based on new duty cycles
	def update(self,data):
		self.sensor = data[0]
		self.freq = data[1]
		control = data[2]
		self.timeON = control/(100*self.freq)
		self.timeOFF = (100-control)/(100*self.freq)
		time.sleep(0.1)				

def main():
	app = QtWidgets.QApplication(sys.argv)
	#app.setStyle('cleanlooks')
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())

if __name__=='__main__':
	main()


