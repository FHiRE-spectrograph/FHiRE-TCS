#TCS_GUI.py
#last updated: 06/11/2021

import sys, serial, os, time, datetime, pytz
import matplotlib.dates as mdates
import RPi.GPIO as GPIO
from pexpect import pxssh
import numpy as np
import threading

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from tcs import Ui_TCS

import TEMP as temp  # HP sensor routine
import low_p_temp_boards as lowp  # LP sensor routine
import PID

# Setup interface's graph.
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

############################################################
# Setup
############################################################

# Setup communication with RPi2 in order to have access to its relays.
# ** Sometimes causes issues toggling RPi2 relays when using pxssh to 
#    run relay_feed.py. **\
# ^^^ Does it still though? 
print('Interface will load shortly. Logging into RPi2 ...')
lnk = pxssh.pxssh()
hn = '10.212.212.79'
us = 'fhire'
pw = 'WIROfhire17'
lnk.login(hn, us, pw)
lnk.sendline('python Desktop/FHiRE-TCS/relay_feed.py')
lnk.prompt()
print('Admin: SSH set up with RPi2. relay_feed.py running.')
ser = serial.Serial(port='/dev/serial0', baudrate=115200, 
		    bytesize=serial.EIGHTBITS, timeout=0)

# frequency for RPi1/LPboard PWM (0.1 = cycle every 10 sec).
# ** RPi2 freq needs to be changed manually in its script relay_feed.py. **
frequency = 1./60

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Setup relays on RPi1.
def GPIO_setup(pin):
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
	print "Relay: %s pin setup" %pin

# Relay number:GPIO pin on RPi1.
relay = {1:29, 2:31, 3:32, 4:33, 5:36, 6:37}  

for key, value in relay.items():
	if key <= 6:
		GPIO_setup(value)

# Used to remove byte messages during UART comm.
def blockPrint():
	sys.stdout = open(os.devnull, 'w')
def enablePrint():
	sys.stdout = sys.__stdout__

hp = temp.TEMP()  # TEMP class for reading HP sensors 
lp = lowp.LP()  # LP class for reading LP boards

start = time.time()		

# Main PyQt5 window.
class MainWindow(QtWidgets.QMainWindow, Ui_TCS):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)
		
		# Currently, not working? See thread below.
		# It's not important to run anyways.
		#self.rpthread = Rpi2Thread()
		#self.rpthread.start()

		self.pidthread = PIDThread(self)
		self.pidthread.signal.connect(self.LP_pause)

		self.hpthread = HPSensorThread()
		self.hpthread.start()

		self.lpthread = LPSensorThread()
		self.lpthread.start()
		self.lpthread.signal.connect(self.PID_update_start)
		self.lpthread.signal2.connect(self.timer_update)

		# Show HP sensors 2,7,10 as off.
		self.cb_hp2.setText("off") 
		self.cb_hp2.setStyleSheet('background-color: lightgrey')

		self.cb_hp7.setText("off")
		self.cb_hp7.setStyleSheet('background-color: lightgrey')

		self.cb_hp10.setText("off")
		self.cb_hp10.setStyleSheet('background-color: lightgrey')

		# Setup plot widgets.
		self.pb_graph.pressed.connect(self.graph)
		self.lay = QtWidgets.QVBoxLayout(self.graphWidget)
		self.lay.setContentsMargins(0, 0, 0, 0)

		# Setup plot and toolbar.
		self.fig, self.ax1 = plt.subplots()
		self.plotWidget = FigureCanvas(self.fig)
		self.lay.addWidget(self.plotWidget)
		self.addToolBar(QtCore.Qt.TopToolBarArea, 
				NavigationToolbar(self.plotWidget, self))
		
		# Sensor - combo box widget pairings.
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

		# **Need to add combo boxes for the external 
		# sensors in QtCreator. There's no way to 
		# plot external sensors from the TCS GUI right now.**
		# I've been using temp-to-voltage.py script to 
		# manually graph external sensors.
		self.lp_sensors = {
			0: self.cb_lp1_top,  # TopDiode-01
			1: self.cb_lp2_top,  # TopResistor-02
			2: self.cb_lp3_top,  # TD-03
			3: self.cb_lp4_top,  # TR-04
			4: self.cb_lp5_top,  # TD-05
			5: self.cb_lp6_top,  # TR-06
			6: self.cb_lp7_top,  # TD-07
			7: self.cb_lp8_top,  # TD-08
			8: self.cb_lp9_top,  # TR-09
			9: self.cb_lp10_top,  # TD-10
			10: self.cb_lp11_top,  # TR-11
			11: self.cb_lp12_top,  # TD-12
			12: self.cb_lp13_top,  # TR-13
			13: self.cb_lp14_top,  # TD-14
			14: self.cb_lp15_top,  # TD-15
			15: self.cb_lp16_top,  # TR-16
			16: self.cb_lp17_top,  # TD-17
			17: self.cb_lp18_top,  # TR-18
			18: self.cb_lp19_top,  # TD-19
			19: self.cb_lp20_top,  # TR-20
			20: self.cb_lp21_top_2,  # TD-21

			21: self.cb_lp1_btm,  # BottomDiode-22
			22: self.cb_lp2_btm,  # BR-23
			23: self.cb_lp3_btm,  # BD-24
			24: self.cb_lp4_btm,  # BR-25
			25: self.cb_lp5_btm,  # BD-26
		
			#26: ,  # ExternalDiode-1
			#27: ,  # ED-2
			#28: ,  # ED-3

			29: self.cb_lp6_btm,  # BR-30
			30: self.cb_lp7_btm,  # BD-31
			31: self.cb_lp8_btm,  # BR-32
			32: self.cb_lp9_btm,  # BD-33
			33: self.cb_lp10_btm,  # BD-34
			34: self.cb_lp11_btm,  # BR-35
			35: self.cb_lp12_btm,  # BD-36
			36: self.cb_lp13_btm,  # BR-37
			37: self.cb_lp14_btm,  # BD-38
			38: self.cb_lp15_btm,  # BR-39
			39: self.cb_lp16_btm,  # BD-40
			40: self.cb_lp17_btm,  # BD-41
			41: self.cb_lp18_btm,  # BR-42
			42: self.cb_lp19_btm,  # BD-43
			43: self.cb_lp20_btm,  # BR-44
			44: self.cb_lp21_btm,  # BD-45
			45: self.cb_lp22_btm,  # BR-46
			46: self.cb_lp23_btm,  # BD-47
			47: self.cb_lp24_btm,  # BR-48
			48: self.cb_lp25_btm,  # BD-49
			49: self.cb_lp26_btm,  # BR-50
			50: self.cb_lp27_btm,  # BD-51
			51: self.cb_lp28_btm,  # BR-52
			52: self.cb_lp29_btm,  # BR-53
			53: self.cb_lp30_btm,  # BD-54
			54: self.cb_lp31_btm}  # BR-55

			#55: ,  # ED-4
			#56: ,  # ED-5
			#57: ,  # ED-6
			#58: ,  # ED-7
			#59: ,  # ED-8
			#60: }  # ED-9


	# Updates countdown between sensor updates.
	def timer_update(self, time):
		try:
			self.timer.setText('%.2f %%\n' %(time[1] + time[0]))
		except:
			self.timer.setText(time)

#######################################################################
# HP and LP Temperature Methods
#######################################################################

	#
	# Graphing options:
	# -Graph HP/LP temperatures via checking respective combo boxes
	# -Graph PID average temperatures via typing respective PID numbers 
	#  into the sensor line edit
	#	-Format: 1 3 4
	# -Display RMS of all individual HP/LP sensors as color spectrum via 
	#  typing "all" into the sensor line edit
	#	-Make sure to erase text to graph temperatures
	# -Graph temperatures for given sensors for range specified by initial 
	#  and final times
	#	-Time format: Y-m-d H:M:S (** Remove time option? You have a 
	#        toolbar to zoom. **)
	#		-** Currently wrong format? Using elapsed 
	#		    time at the moment. **
	#	-Graph all measurements by keeping initial and final 
	#        times unspecified
	# **Add option to calculate RMS over a specific time range?
	#
	def graph(self):
		Averaging_monitor()
		Averaging_control()

		# File setup --------------------------------------------
		hp_file = 'tempLog.dat'
		lpr_file = 'LPresistorsLog.dat'
		lpd_file = 'LPdiodesLog.dat'
		avg_file = 'controlTemp.dat'
		avg_file2 = 'monitoringTemp.dat'  # Averaged resistors

		hp = np.loadtxt(hp_file, unpack=True, skiprows=1)
		lpr = np.loadtxt(lpr_file, unpack=True, skiprows=1)
		lpd = np.loadtxt(lpd_file, unpack=True, skiprows=1)
		avgT = np.loadtxt(avg_file, unpack=True, skiprows=1)
		avgT2 = np.loadtxt(avg_file2, unpack=True, skiprows=1)

		# Sensor number:column in dat file
		diode_column = {
			1:1,   3:2,   5:3,   7:4,   8:5,   10:6,  12:7,  14:8,  15:9, 
			17:10, 19:11, 21:12, 22:13, 24:14, 26:15, 27:16, 28:17, 29:18, 
			31:19, 33:20, 34:21, 36:22, 38:23, 40:24, 41:25, 43:26, 45:27, 
			47:28, 49:29, 51:30, 54:31, 55:31, 56:32, 57:33, 58:34, 59:35, 
			60:36, 61:37}
		resistor_column = {
			2:1,   4:2,   6:3,   9:4,   11:5,  13:6,  16:7,  18:8,  20:9, 
			23:10, 25:11, 30:12, 32:13, 35:14, 37:15, 39:16, 42:17, 44:18, 
			46:19, 48:20, 50:21, 52:22, 53:23, 55:24}

		hp_column =  {1:1, 3:2, 4:3, 5:4, 6:5, 8:6, 9:7} 

		#------------------------------------------------------------
		#
		# Display RMS of each sensor as part of a color spectrum. Not
		# really an important function any more. This was used for testing
		# when we were troubleshooting high RMS issues with the LP sensors.
		#
		if self.ln_sensor.text() == 'all':
			red = 'background-color: #ff9999'
			orange = 'background-color: #ffcc99'
			yellow = 'background-color: #ffff99'
			lightgreen = 'background-color: #ccff99'
			green = 'background-color: #99ff99'

			for x in self.lp_sensors.keys():
				x += 1
				if x in diode_column.keys():
					y = lpd[diode_column.get(x), :]
				elif x in resistor_column.keys():
					y = lpr[resistor_column.get(x), :]

				avg = np.nanmean(y)
				rms = np.sqrt(np.nanmean((y - avg) ** 2))
				rms = rms * 10 ** 3
			
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
				elif rms == 0 or np.isnan(rms) == True:
					style = 'background-color: lightgrey'

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
				elif rms == 0 or np.isnan(rms) == True:
					style = 'background-color: lightgrey'

				self.hp_sensors[x][0].setStyleSheet(style)
			return

		self.ax1.cla()  # clear plot

		# Plot PID average control (diode) temperatures.
		avg_sensors = [int(n) for n in self.ln_sensor.text().split()]
		for x in range(28):
			x += 1
			x2 = avgT[0, :]/3600
			y = avgT[x, :]
			avg = np.nanmean(y)
			rms = np.sqrt(np.nanmean((y - avg) ** 2))
			rms = rms*10**3

			#print('PID %s: %.2fC (RMS:%.2fmK)' %(x, avg, rms))
			if x in avg_sensors:
				self.ax1.plot(x2, y, label="cPID%s:"
					      "RMS=%.2fmK (%.2f)" %(x, rms, avg))	

		# Plot PID average monitoring (resistors) temperatures.
		for x in range(28):
			x += 29
			x2 = avgT2[0, :]/3600
			y = avgT2[x-28, :]
			avg = np.nanmean(y)
			rms = np.sqrt(np.nanmean((y - avg) ** 2))
			rms = rms*10**3

			#print('PID %s: %.2fC (RMS:%.2fmK)' %(x,avg,rms))
			if x in avg_sensors:
				self.ax1.plot(x2, y, label="mPID%s:"
					      "RMS=%.2fmK (%.2f)" %(x - 28, rms, avg))
 		#-------------------------------------------------------------------

		#
		# Option to set range of times -- doesn't really work anymore. 
		# Written for utc, not elapsed time.
		# Keep initial/final time line edits empty in the mean time.
		#
		try:
			utc = hp[0, :]

		except:
			print "Not enough values recorded (>1)."
			return

		try:
			utcr = lpr[0, :]
			utcd = lpd[0, :]	
		except:
			print "Not enough values recorded (>1)."
			return		

		self.time_initial = self.ln_to.text()
		self.time_final = self.ln_tf.text()

		# Plot all times if no initial/final time specified.
		if not self.time_initial and not self.time_final:
			hp_index1 = lpr_index1 = lpd_index1 = 0 
			hp_index2 = lpr_index2 = lpd_index2 = None

		if self.time_initial:
			# Convert given date & time to local epoch seconds.
			to = self.time_initial.split()
			date1 = to[0].split("-")
			time1 = to[1].split(":")
			for x in range(len(date1)):
				date1[x] = int(date1[x])
			for x in range(len(time1)):
				time1[x] = int(time1[x])
			try:
				utc1 = datetime.datetime(
					date1[0], date1[1], date1[2],
					time1[0], time1[1], 
					time1[2]).strftime("%s")  # Local time 
			except:
				#print("Improper initial time.")
				pass
			utc1 = float(utc1)
			
			# Find closest time in tempLog.dat and get index.
			hp_index1 = min(range(len(utc)), 
					 key=lambda i: abs(utc[i] - utc1))
			lpr_index1 = min(range(len(utcr)), 
					 key=lambda i: abs(utcr[i] - utc1))
			lpd_index1 = min(range(len(utcd)), 
					 key=lambda i: abs(utcd[i] - utc1))

		if self.time_final:
			tf = self.time_final.split()
			date2 = tf[0].split("-")
			time2 = tf[1].split(":")
			for x in range(len(date2)):
				date2[x] = int(date2[x])
			for x in range(len(time2)):
				time2[x] = int(time2[x])
			try:
				# Local time
				utc2 = datetime.datetime(date2[0], 
							 date2[1], 
							 date2[2], 
							 time2[0], 
							 time2[1], 
							 time2[2]).strftime("%s") 
			except:
				#print("Improper final time.")
				pass
			utc2 = float(utc2)

			hp_index2 = min(range(len(utc)), 
					key=lambda i: abs(utc[i] - utc2))
			lpr_index2 = min(range(len(utcr)), 
					 key=lambda i: abs(utcr[i] - utc2))
			lpd_index2 = min(range(len(utcd)), 
					 key=lambda i: abs(utcd[i] - utc2))

		# Plot individual HP/LP sensor temperatures based on checked
		# combo boxes.
		lp_checked = []; hp_checked = []
		for x in self.lp_sensors.keys():
			if self.lp_sensors[x].isChecked():
				lp_checked.append(x + 1)
				
		for x in self.hp_sensors.keys():
			if self.hp_sensors[x][0].isChecked():
				hp_checked.append(self.hp_sensors[x][1])

		hp_col = []; lpr_col = []; lpd_col = []
		lpr_checked = []; lpd_checked = []
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

		if hp_col:
			for i in range(len(hp_col)):
				x = utc[hp_index1: hp_index2] / 3600
				y =  hp[hp_col[i], hp_index1: hp_index2]
				avg = np.nanmean(y)
				rms = np.sqrt(np.nanmean((y - avg) ** 2))
				rms = rms * 10 ** 3  # rms in mK
				self.ax1.plot(x, y, color='gray',
					      label="HP%s:RMS=%.2fmK" 
					      %(hp_checked[i], rms))
		if lpr_col:
			for i in range(len(lpr_col)):
				x = utcr[lpr_index1: lpr_index2] / 3600
				y =  lpr[lpr_col[i], lpr_index1: lpr_index2]
				avg = np.nanmean(y)
				rms = np.sqrt(np.nanmean((y - avg) ** 2))
				rms = rms*10**3  # rms in mK
				self.ax1.plot(x, y, 
					      label="LP%s:RMS=%.2fmK" 
					      %(lpr_checked[i], rms))

		config = np.loadtxt('pid.conf', unpack=True, skiprows=1, 
				    usecols=(0,1,2,3,4))

		LPHeating = {
			1:[15],  2:[8],   3:[1],   4:[17],  5:[10],  6:[3],   7:[19], 
			8:[12],  9:[5],   10:[21], 11:[14], 12:[7],  13:[51], 14:[22], 
			15:[34], 16:[41], 17:[24], 18:[36], 19:[43], 20:[26], 21:[38], 
			22:[45], 23:[31], 24:[40], 25:[47], 26:[33], 27:[49], 28:[54]}
	
		colors = ['red', 'darkorange', 'green', 'blue', 'dodgerblue', 
			'purple', 'black', 'turquoise', 'brown', 'violet']

		if lpd_col:
			for i in range(len(lpd_col)):
				# Graph horizontal line for PID setpoints.
				for key, value in LPHeating.iteritems():
					if value[0] == lpd_checked[i]:
						pid_col = key - 1
				set_temp = config[1, pid_col]

				x = utcd[lpd_index1: lpd_index2] / 3600
				y =  lpd[lpd_col[i], lpd_index1: lpd_index2]
				avg = np.nanmean(y)
				rms = np.sqrt(np.nanmean((y - avg) ** 2))
				rms = rms * 10 ** 3  # rms in mK
				self.ax1.plot(x, y, color=colors[i],
					      label="LP%s:RMS=%.2fmK" 
					      %(lpd_checked[i], rms))
				self.ax1.axhline(set_temp, color=colors[i],
 						 linestyle='--')

		self.fig.canvas.draw_idle()
		self.ax1.grid()
		self.ax1.set_xlabel("Time (h)")
		self.ax1.set_ylabel("Temperature [C]")
		self.ax1.legend(loc="lower right", prop={"size":9})

	# Start PID thread.
	def PID_update_start(self, status):
		self.pid_status = status
		self.pidthread.start()

	# Signal from LP relay pwm thread to pause/start LP temp. readings.
	def LP_pause(self, status_list):
		self.lpthread.signal3.emit(status_list)

	def closeEvent(self, event):
		reply = QtWidgets.QMessageBox.question(self, 'Window Close', 
				'Are you sure you want to close the window?', 
				QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, 
				QtWidgets.QMessageBox.No)

		if reply == QtWidgets.QMessageBox.Yes:
			# Close all running threads.
			self.lpthread.stop() 
			self.hpthread.stop()
			self.pidthread.stop()

			#self.rpthread.stop()
			plt.close('all')
			GPIO.cleanup()
			event.accept()
			print 'Window Closed'
		else:
			event.ignore()

# Pair diodes with their respective heating pad/PID loop
# and save to a file. File is accessed by PID methods below.
def Averaging_control():
	lpd_file = 'LPdiodesLog.dat'
	lpd = np.loadtxt(lpd_file, unpack=True, skiprows=1)

	check = np.loadtxt('monitoringTemp.dat', unpack=True, skiprows=1)

	diode_column = {
		1:1,   3:2,   5:3,   7:4,   8:5,   10:6,  12:7,  14:8,  15:9,  17:10, 
		19:11, 21:12, 22:13, 24:14, 26:15, 31:19, 33:20, 34:21, 36:22, 38:23, 
		40:24, 41:25, 43:26, 45:27, 47:28, 49:29, 51:30, 54:31}
	
	LPHeating = {
		1:[15],  2:[8],   3:[1],   4:[17],  5:[10],  6:[3],   7:[19],  8:[12], 
		9:[5], 	 10:[21], 11:[14], 12:[7],  13:[51], 14:[22], 15:[34], 16:[41], 
		17:[24], 18:[36], 19:[43], 20:[26], 21:[38], 22:[45], 23:[31], 24:[40], 
		25:[47], 26:[33], 27:[49], 28:[54]}

	utc = lpd[0]

	final = []
	for x in LPHeating:
		y = LPHeating[x][0]
		# Simple attempt at replacing a diode reading with averaged
		# resistor readings for a PID loop. Didn't work properly.
		#if x == 9:
		#	val_1 = lpd[diode_column.get(y)]
		#	val_2 = check[9]
		#	val = np.vstack((val_1, val_2))
		#	val = np.mean(val, axis=0)
		#else:			
		#	val = lpd[diode_column.get(y)]

		val = lpd[diode_column.get(y)]
		if x == 1:
			final = val
		else:
			final = np.vstack((final, val))
			

	with open('controlTemp.dat', 'a') as avgTemp:
		avgTemp.seek(0,1)
		avgTemp.truncate(112)
		
		for x in range(len(final[0])):
			try:
				avgTemp.write('%.0f		' %utc[x])
			except:
				avgTemp.write('%.0f		' %utc)
			for item in final[:, x]:
				avgTemp.write('%.4f ' %item)
			avgTemp.write('\n')
			
#
# Averages LP resistors around each diode to monitor and catch unreasonable 
# diode temperatures. **Need to create method that replaces diode readings 
# with resistors for PID loops if diode fails.**
#
def Averaging_monitor():
	lpr_file = 'LPresistorsLog.dat'
	lpr = np.loadtxt(lpr_file, unpack=True, skiprows=1)
	resistor_column = {
		2:1,   4:2,   6:3,   9:4,   11:5,  13:6,  16:7,  18:8,  20:9, 
		23:10, 25:11, 30:12, 32:13, 35:14, 37:15, 39:16, 42:17, 44:18, 
		46:19, 48:20, 50:21, 52:22, 53:23, 55:24}	
	LPHeating = {
		1:[16,9], 
		2:[9,16,2], 
		3:[2,9], 
		4:[16,18,9,11], 
		5:[9,11,16,18,2,4], 
		6:[2,4,9,11], 
		7:[18,20,11,13], 
		8:[11,13,18,20,4,6], 
		9:[4,6,11,13], 
		10:[20,13], 
		11:[13,20,6], 
		12:[6,13], 
		13:[50,52], 
		14:[23], 
		15:[23,42,35], 
		16:[42], 
		17:[23,35,25], 
		18:[35,25,44,37],
		19:[42,35,44], 
		20:[25,30,37], 
		21:[37,39,46,30], 
		22:[44,46,37], 
		23:[30,32,39],
		24:[39,32,48], 
		25:[46,39,48], 
		26:[32], 
		27:[48], 
		28:[53,55]}

	utc = lpr[0]

	final = []
	for x in LPHeating:
		stack = []
		for y in LPHeating[x]:
			if y in resistor_column.keys():
				val = lpr[resistor_column.get(y)]
			if y == LPHeating[x][0]:
				stack = val
			else:
				stack = np.vstack((stack, val))
		try:
			if len(stack[0]):
				stack = np.nanmean(stack, axis=0)
		except:
			pass

		if x == 1:
			final = stack
		else:
			final = np.vstack((final, stack))

	with open('monitoringTemp.dat', 'a') as mTemp:
		mTemp.seek(0,1)
		mTemp.truncate(112)

		for x in range(len(final[0])):
			mTemp.write('%.0f		' %utc[x])
			for item in final[:, x]:
				mTemp.write('%.4f ' %item)
			mTemp.write('\n')
#
# Compare monitoring and control readings for each PID loop to check
# that each diode is measuring properly. Still a work in progress.
# Not sure how useful it would be now. The resistors' averaged RMS
# is still large and our calibration of them is poor. 
#
def compare():
	monitor = np.loadtxt("monitoringTemp.dat", unpack=True, skiprows=1)
	control = np.loadtxt("controlTemp.dat", unpack=True, skiprows=1)

	
################################################################################
#  QThread Classes
################################################################################
			
# QThread for reading HP sensor temperatures from TEMP.py.
class HPSensorThread(QThread):

	def __init__(self):
		QThread.__init__(self)
		self.j = 0
	
	def run(self):
		while True:
			hptemp = []
			tic = time.time()
			elapsed = 0; i = 0

			# Set total time in seconds between temp/duty cycle updates.
			total = 15  

			while elapsed < total:
				elapsed = time.time() - tic

				averaging = []
				for s in range(7): 
					try:
						hpboard = hp.getTemp(s)
						#print("HP %s: %.5s C" 
						#      %(s+2,hpboard))
					except:
						print("Error reading HP "
						      "sensor %s" %s)
						hpboard = 11111

					if hpboard >= 26 or hpboard <= 20:
						hpboard = hp.getTemp(s)

					if hpboard >= 26 or hpboard <= 20:
						hpboard = np.nan
	
					averaging.append(hpboard)

				if i == 0:
					hptemp = averaging
					i += 1
				else:
					hptemp = np.vstack((hptemp, averaging))
				time.sleep(1)

			hpstd = np.std(hptemp, axis=0)
			hptemp = np.nanmean(hptemp, axis=0)

			total_elapsed = time.time() - start

			with open('tempLog.dat', 'a') as tempLog:
				current_time = mdates.date2num(datetime.datetime.now())
				if self.j == 0:
					tempLog.seek(0,1)
					tempLog.truncate(61)
					self.j += 1
					tempLog.write('%.0f		' 
							%(current_time))
				else:
					tempLog.write('\n%.0f		'
							%(current_time))
				for item in hptemp:
					tempLog.write("%.6s " %item)

			wait = 1.5
			if wait * 60 > total:
				time.sleep((wait * 60) - total)  # reading intervals 
			total_elapsed = time.time() - start

	def stop(self):
		self.terminate()

# QThread for reading LP sensor temperatures from low_p_temp_boards.py.
class LPSensorThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	signal2 = pyqtSignal('PyQt_PyObject')
	signal3 = pyqtSignal('PyQt_PyObject')

	def __init__(self):
		QThread.__init__(self)

		self.diodes = [
			1,  3,  5,  7,  8,  10, 12, 14, 15, 17, 19, 21, 22, 24,
			26, 27, 28, 29, 31, 33, 34, 36, 38, 40, 41, 43, 45, 47, 
			49, 51, 54, 56, 57, 58, 59, 60, 61] 
		self.resistors = [
			2,  4,  6,  9,  11, 13, 16, 18, 20, 23, 25, 30,
			32, 35, 37, 39, 42, 44, 46, 48, 50, 52, 53, 55] 
		self.j = 0; self.k = 0; self.m = 0

		# Used for keeping the LP thread paused while LP relays are toggling
		# to avoid interference.
		self.pause = [False, False, False, False, False, False]
		self.signal3.connect(self.LP_pause)

	def run(self):
		print("Starting thread")
		time.sleep(0.05)
		total_minutes = 0
		total = 4  # total PWM periods (period = 60sec) between measurements

		while True:
			if total_minutes == 0:
				tic = time.time()

			self.pause = [False, False, False, False, False, False]

			while any(x == False for x in self.pause) == True:
				time.sleep(0.5)

			if total_minutes == 0:
				time.sleep(1)
				self.measureTemp()

			total_minutes += 1

			statement = "%s/%s minutes" %(total_minutes, total)
			self.signal2.emit(statement)
			print(statement)

			if total_minutes == total:
				total_minutes = 0

	def measureTemp(self):
		lptemp = []
		i = 0; n = 0
		print("========== New Data Point ==========")
		#
		# Currently, can only fit one rotation of temperature readings
		# within about 50 seconds. Improve the readout speed to add more
		# rotations to average. 
		#
		while n < 1:
			averaging = []
			for s in range(61): 
				s = s + 1

				try:
					lpboard = lp.getTemp(s)
					time.sleep(0.01)
				except:
					print("Error reading sensor %s" %(s + 1))
					lpboard = 11111

				#
				# The 9 external LP sensors (27-29, 56-61)
				# need to be calibrated properly, so they're exempt
				# from the temperature cutoffs.
				#
				if lpboard >= 26 or lpboard <= 22 \
				   and s not in [27,28,29,56,57,58,59,60,61]:
					lpboard = lp.getTemp(s)

				if lpboard >= 26 or lpboard <= 22 \
				   and s not in [27,28,29,56,57,58,59,60,61]:
					lpboard = np.nan
						
				averaging.append(lpboard)
				time.sleep(0.01)

			if i == 0:
				lptemp = averaging
				i += 1
			else:
				lptemp = np.vstack((lptemp, averaging))

			time.sleep(0.01)
			n += 1

		try:
			if len(lptemp[1]):
				lpstd = np.std(lptemp, axis=0)
				lptemp = np.nanmean(lptemp, axis=0)
		except:
			pass

		print("---------------------------------")

		lptempD = []
		for s in self.diodes:
			lptempD.append(lptemp[s - 1])

		lptempR = []; lpstdR = []
		for s in self.resistors:
			lptempR.append(lptemp[s - 1])

		total_elapsed = time.time() - start	
		current_time = mdates.date2num(datetime.datetime.now())
		print("Time elapsed: %.8s seconds" %total_elapsed)

		with open('LPdiodesLog.dat', 'a') as tempLog:
			if self.j == 0:
				tempLog.seek(0,1)
				tempLog.truncate(273)
				self.j += 1
				tempLog.write('%.0f		' %(current_time))
			else:
				tempLog.write('\n%.0f		'%(current_time))
			for item in lptempD:
				if item == np.nan:
					tempLog.write("%s    " %item)
				else:
					tempLog.write("%s " %item)

		with open('LPresistorsLog.dat', 'a') as tempLog:
			if self.k == 0:
				tempLog.seek(0,1)
				tempLog.truncate(176)
				self.k += 1
				tempLog.write('%.0f		' %(current_time))
			else:
				tempLog.write('\n%.0f		'%(current_time))
			for item in lptempR:
				if item == np.nan:
					tempLog.write("%s    " %item)
				else:
					tempLog.write("%s " %item)

		#
		# Allows the user to take a baseline measurement to determine 
		# individual set points for each PID loop. Only necessary because
		# each sensor was calibrated in its current location instead of 
		# referenced to an ice bath, so gradient temperature changes in 
		# the enclosure will have affected calibration.
		#
 
		baseline_hour = 0.15
		if total_elapsed > baseline_hour*3600:  # baseline = 3 data points
			pid = True  # start PID loops
		else:
			pid = False  # take baseline measurements
		#pid = True
		#pid = False

		self.signal.emit(pid)
	
	def LP_pause(self,status_list):
		self.pause[status_list[1] - 21] = status_list[0]
					
	def stop(self):
		self.terminate()

#
# **Currently not in use because pxssh/relay_feed.py need to be running 
# before temperature threads. Setting up pxssh as a thread vs at top of 
# script removes loading time for GUI display.**
#
class Rpi2Thread(QThread):
	def __init__(self):
		QThread.__init__(self)
	def run(self):
		# Setup communication with RPi2 in order to have 
		# access to its relays.
		print('Logging into RPi2 ...')
		lnk = pxssh.pxssh()
		hn = '10.212.212.70'
		us = 'fhire'
		pw = 'WIROfhire17'
		lnk.login(hn, us, pw)
		lnk.sendline('python Desktop/FHiRE-TCS/relay_feed.py')
		lnk.prompt()
		print('SSH set up with tcsP2. Relay_feed.py running.')
	def stop(self):
		self.terminate()

class PIDThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self, main):
		self.main = main	
	
		self.pwmthread = []
		for x in range(6):
			self.pwmthread.append(LPpwmThread(x + 21, frequency, 0))
			self.pwmthread[x].start()
			self.pwmthread[x].signalpwm.connect(self.LP_pause)
		
		self.PWM_setup()
		self.PID_setup()
		self.first = True
		print('Initialization complete')

		# Why is this not at the beginning of __init__?
		super(PIDThread, self).__init__(main)  

	def run(self):
		if self.main.pid_status == True:
			print('PID update thread')
			self.PID_update()
			print('PID update start complete')

	def LP_pause(self, status_list):
		self.signal.emit(status_list)

	# Setup PWM controls for relays (mainly RPi1 relays)
	def PWM_setup(self):
		self.pwm = []
		for x in range(28):
			x += 1
			if x <= 6:
				self.pwm.append(GPIO.PWM(relay[x], frequency))
				self.pwm[x - 1].start(100)
			elif 7 <= x <= 20 or x in [27,28]:
				pass  # PWM setup in relay_feed.py on RPi2
			elif 21 <= x <= 26:
				pass  # PWM setup in LPpwmThread

	# Setup PID loops for each heating pad.
	def PID_setup(self):
		self.pid = []
		for x in range(28):
			self.pid.append(PID.PID())
			self.readConfig(x) 
			self.pid[x].setSampleTime(1)

	def calculate_baseline(self):
		try:
			if len(self.avgT[0]): 
				baseline = np.nanmean(self.avgT, axis=0)
		except:
			baseline = self.avgT

		baseline = baseline[1:30]
		config = np.loadtxt('pid.conf', unpack=True, skiprows=1, 
				    usecols=(0,1,2,3,4))
		config[1,:] = baseline + 1.0
		#config[1,:] = config[1,:] + 0.5
		with open('pid.conf','a') as config_file:
			config_file.seek(0,1)
			config_file.truncate(21)

			for x in range(np.shape(config)[1]):
				config_file.write(
					'%.0f	%.2f	%s	%s	%s\n' %(
					config[0,x], config[1,x], config[2,x],
					config[3,x], config[4,x]))

	# Update PID loops and PWM of heaters.
	def PID_update(self):
		tic = time.time()
		Averaging_monitor()
		Averaging_control()

		time.sleep(0.1)
		avg_file = 'controlTemp.dat'
		self.avgT = np.loadtxt(avg_file, unpack=True, skiprows=1)
		self.avgT = np.transpose(self.avgT)

		if self.first == True:
			# Uncomment when a baseline has been measured beforehand.
			self.calculate_baseline()
			self.first = False
			print('################################')
			print('Begin PID loop control')

		try:
			self.avgT = self.avgT[-1,1: 29]
		except IndexError:  # When there's only one line of data
			self.avgT = self.avgT[1: 29]

		relay = {
			1:self.main.lb_h1_top, 
			2:self.main.lb_h2_top,
			3:self.main.lb_h3_top,
			4:self.main.lb_h4_top,
			5:self.main.lb_h5_top,
			6:self.main.lb_h6_top,
			7:self.main.lb_h7_top,
			8:self.main.lb_h8_top,
			9:self.main.lb_h9_top,
			10:self.main.lb_h10_top,
			11:self.main.lb_h11_top,
			12:self.main.lb_h12_top,
			13:self.main.lb_h1,
			14:self.main.lb_h2,
			15:self.main.lb_h3,
			16:self.main.lb_h4,
			17:self.main.lb_h5,
			18:self.main.lb_h6,
			19:self.main.lb_h7,
			20:self.main.lb_h8,
			21:self.main.lb_h9,
			22:self.main.lb_h10,
			23:self.main.lb_h11,
			24:self.main.lb_h12,
			25:self.main.lb_h13,
			26:self.main.lb_h14,
			27:self.main.lb_h15,
			28:self.main.lb_h16}
	
		for x in range(len(self.avgT)):
			heat = x + 1
		
			# Get new Duty Cycle values from PID loops based on 
			# most recent PID average temperatures.
			self.pid[x].update(self.avgT[x])
			control = self.pid[x].output
			control = max(min(float(control), 8), 0)  # 3% limit
			relay[x + 1].setText('%.2f%%' %control)
			if np.isnan(control) == True:
				control = 0
				print("PID %s: NAN ... setting DC = 0%%" %heat)

			# Update PWM Duty Cycle.
			if 7 <= heat <= 20 or heat in [27, 28]:  # Rpi 2
				print('PID %s: %.2f%% (%.2fs)' %(
					heat, control, (control / (100.0 * frequency))))

				blockPrint()
				ser.write(str(heat) + " " + str(control))
				enablePrint()
				time.sleep(0.1)

			elif heat <= 6:  # Rpi 1
				print('PID %s: %.2f%% (%.2fs)' %(
					heat, control, (control / (100.0 * frequency))))

				self.pwm[heat - 1].ChangeDutyCycle(100 - control)
				time.sleep(0.1)

			elif 21 <= heat <= 26:  # LP boards
				#
				# Decrease frequency of PWM if the control is 
				# low enough to be less than the response time 
				# of the RPi.
				#
				if control / (100.0 * frequency) < 0.0006 \
				   and control > 0:
					freq2 = control / (100.0 * 0.0006)
					print("New freq for PID %s: %s" %(heat, freq2))
					print('PID %s: %.2f%% (%.2fs)' %(
						heat, control, (control /
	 							(100.0 * freq2))))

					self.pwmthread[heat - 21].update(
							[heat, freq2, control])
				else:
					print('PID %s: %.2f%% (%.2fs)' %(
						heat, control, (control /
								(100.0 * frequency))))

					self.pwmthread[heat - 21].update(
							[heat, frequency ,control])
				time.sleep(0.1)

			self.readConfig(x)
			time.sleep(0.5)

		elapsed = time.time() - tic
		print('%.4f' %elapsed)
		print('===================')

	def readConfig(self, ind):
		config = np.loadtxt('pid.conf', unpack=True, skiprows=1, 
				    usecols=(0,1,2,3,4))
		self.pid[ind].SetPoint = float(config[1, ind])
		self.pid[ind].Kp = float(config[2, ind])
		self.pid[ind].Ki = float(config[3, ind])
		self.pid[ind].Kd = float(config[4, ind])

	def stop(self):			
		for x in range(28):
			x += 1
			if x <= 6:
				self.pwm[x - 1].stop()
			elif x == 7:
				blockPrint()
				# Sends unique string to RPi1 to signify it 
				# to stop its PWM.
				ser.write('1111 1')  
				enablePrint()
			elif 21 <= x <= 26:
				self.pwmthread[x - 21].stop()
		self.terminate()

# QThread of method to emulate PWM for relays on LP boards.
class LPpwmThread(QThread):
	signalpwm = pyqtSignal('PyQt_PyObject')
	
	def __init__(self, sensor, freq, control):
		QThread.__init__(self)
		self.sensor = sensor
		self.freq = freq
		self.timeON = control / (100 * freq)
		self.timeOFF = (100 - control) / (100 * freq)
		self.ON = False

	def run(self):
		while True:
			tic = time.clock()

			if self.timeON > 0:
				time.sleep(0.01)
				lp.Relay_ON(self.sensor)

				elapsed = time.clock() - tic
				print '*Relay %s ON: %.3f' %(
					self.sensor, self.timeON - elapsed)

				if self.timeON > elapsed:  # When timeOn > 0.0006sec
					time.sleep(self.timeON - elapsed)
	
			tic = time.clock()
			if self.timeOFF > 0:
				time.sleep(0.01)
				lp.Relay_OFF(self.sensor)

				self.signalpwm.emit([True, self.sensor])

				elapsed = time.clock() - tic
				print '*Relay %s OFF: %.3f' %(
					self.sensor, self.timeOFF - elapsed)

				if self.timeOFF > elapsed:
					time.sleep(self.timeOFF - elapsed)
			
	def stop(self):
		print('Turning off %s' %self.sensor)
		lp.Relay_OFF(self.sensor)
		self.terminate()

	# Update timeON and timeOFF based on new duty cycles.
	def update(self, data):
		self.sensor = data[0]
		self.freq = data[1]
		control = data[2]
		self.timeON = control / (100 * self.freq)
		self.timeOFF = (100 - control) / (100 * self.freq)
		time.sleep(0.1)		
		

def main():
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())

if __name__=='__main__':
	try:
		main()

	except KeyboardInterrupt:
		# ** Doesn't work **
		# So try not to keyboard interrupt TCS_GUI.py!
		print("*Interrupted")
		main.lpthread.stop() 
		main.hpthread.stop()
		for x in range(28):
			x += 1
			if x <= 6:
				main.pwm[x - 1].stop()
			elif x == 7:
				blockPrint()
				ser.write('1111 1')
				enablePrint()
			elif 21 <= x <= 26:
				main.pwmthread[x - 21].stop()
		#main.rpthread.stop()
		plt.close('all')
		GPIO.cleanup()
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)


