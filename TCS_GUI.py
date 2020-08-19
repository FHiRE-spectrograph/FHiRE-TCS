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
	sys.stdout=open(os.devnull,'w')

#blockPrint()
hp = temp.TEMP() #TEMP class of HP sensors 
lp = lowp.LP() #LP class for LP boards

for key, value in relay.items():
	if key <= 6:
		GPIO_setup(value)		

class MainWindow(QtWidgets.QMainWindow, Ui_TCS):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)
		#QtGui.QMainWindow.__init__(self)
		#uic.loadUi('tcs.ui',self)

		#self.btnExit.clicked
		
		self.hpthread = HPSensorThread()
		self.hpthread.start()
		self.hpthread.signal.connect(self.hp_update)

		self.lpthread = LPSensorThread()
		self.lpthread.start()
		self.lpthread.signal.connect(self.lp_update)

		self.cb_hp2.setText("off")
		self.cb_hp7.setText("off")
		self.cb_hp10.setText("off")

		heater=[self.pb_h1,self.pb_h2,self.pb_h3,self.pb_h4,
			self.pb_h5,self.pb_h6,self.pb_h7,self.pb_h8,
			self.pb_h9,self.pb_h10,self.pb_h11,self.pb_h12,
			self.pb_h13,self.pb_h14,self.pb_h15,self.pb_h16,
			self.pb_h1_top,self.pb_h2_top,self.pb_h3_top,
			self.pb_h4_top,self.pb_h5_top,self.pb_h6_top,
			self.pb_h7_top,self.pb_h8_top,self.pb_h9_top,
			self.pb_h10_top,self.pb_h11_top,self.pb_h12_top]

		for h in heater:
			h.setCheckable(True)
			h.setStyleSheet("QPushButton:checked {background-color: #ADFF2F}")

		self.pb_h1.clicked.connect(lambda:self.relay(self.pb_h1,1))
		self.pb_h2.clicked.connect(lambda:self.relay(self.pb_h2,2))
		self.pb_h3.clicked.connect(lambda:self.relay(self.pb_h3,3))
		self.pb_h4.clicked.connect(lambda:self.relay(self.pb_h4,4))
		self.pb_h5.clicked.connect(lambda:self.relay(self.pb_h5,5))
		self.pb_h6.clicked.connect(lambda:self.relay(self.pb_h6,6))
		self.pb_h7.clicked.connect(lambda:self.relay(self.pb_h7,7))
		self.pb_h8.clicked.connect(lambda:self.relay(self.pb_h8,8))
		self.pb_h9.clicked.connect(lambda:self.relay(self.pb_h9,9))
		self.pb_h10.clicked.connect(lambda:self.relay(self.pb_h10,10))
		self.pb_h11.clicked.connect(lambda:self.relay(self.pb_h11,11))
		self.pb_h12.clicked.connect(lambda:self.relay(self.pb_h12,12))
		self.pb_h13.clicked.connect(lambda:self.relay(self.pb_h13,13))
		self.pb_h14.clicked.connect(lambda:self.relay(self.pb_h14,14))
		self.pb_h15.clicked.connect(lambda:self.relay(self.pb_h15,15))
		self.pb_h16.clicked.connect(lambda:self.relay(self.pb_h16,16))

		self.pb_h1_top.clicked.connect(lambda:self.relay(self.pb_h1_top,17))
		self.pb_h2_top.clicked.connect(lambda:self.relay(self.pb_h2_top,18))
		self.pb_h3_top.clicked.connect(lambda:self.relay(self.pb_h3_top,19))
		self.pb_h4_top.clicked.connect(lambda:self.relay(self.pb_h4_top,20))
		self.pb_h5_top.clicked.connect(lambda:self.relay(self.pb_h5_top,21))
		self.pb_h6_top.clicked.connect(lambda:self.relay(self.pb_h6_top,22))
		self.pb_h7_top.clicked.connect(lambda:self.relay(self.pb_h7_top,23))
		self.pb_h8_top.clicked.connect(lambda:self.relay(self.pb_h8_top,24))
		self.pb_h9_top.clicked.connect(lambda:self.relay(self.pb_h9_top,25))
		self.pb_h10_top.clicked.connect(lambda:self.relay(self.pb_h10_top,26))
		self.pb_h11_top.clicked.connect(lambda:self.relay(self.pb_h11_top,27))
		self.pb_h12_top.clicked.connect(lambda:self.relay(self.pb_h12_top,28))

	def relay(self, btn, ind):
		if ind < 16:
			ind1="btm: "+str(ind)
		elif ind >= 16:
			ind1="top: "+str(ind-16)

		if btn.isChecked():
			print 'checked'
			if ind <= 6:
				GPIO.output(relay[ind],GPIO.LOW)
			elif 7 <= ind <= 20 or ind == 27 or ind == 28:
				ser.write(str(ind).strip('\r\n'))
			elif 21 <= ind <= 26:	
				lp.Relay_ON(ind)

			print "Relay "+ind1+" ON"
		else:
			print 'not checked'
			if ind <= 6:
				GPIO.output(relay[ind],GPIO.HIGH)
			elif 7 <= ind <= 20 or ind == 27 or ind == 28:
				ser.write(str(ind*100).strip('\r\n'))
			elif 21 <= ind <= 26:	
				lp.Relay_OFF(ind)
	
			print "Relay "+ind1+" OFF"

	def relay_off(self, ind):
		if ind < 16:
			ind1="btm: "+str(ind)
		elif ind >= 16:
			ind1="top: "+str(ind-16)


		if ind <= 6:
			GPIO.output(relay[ind],GPIO.HIGH)
		elif 7 <= ind <= 20 or ind == 27 or ind == 28:
			ser.write(str(ind*100).strip('\r\n'))
		elif 21 <= ind <= 26:	
			lp.Relay_OFF(ind)
	
		print "Relay "+ind1+" OFF"
		

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
		Rstatus = data[2]
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

		if data[0] in objects.keys():
			pre = objects[data[0]].text()
			pre = pre.split(':')[0]
			time.sleep(0.01)
			objects[data[0]].setText(pre+": %.2f C" %data[1])	

		relay = {0:[self.pb_h5_top,self.pb_h6_top],1:[self.pb_h7_top,self.pb_h8_top],
			2:[self.pb_h9_top,self.pb_h10_top]}
		
		#Update relay status if not turned on/off manually 
		ind = -1
		for x in Rstatus:
			ind += 1

			if 0x330000 & x == 0x330000: #both off
				relay[ind][0].setChecked(False)
				relay[ind][1].setChecked(False)

			elif 0x230000 & x == 0x230000: #P1 on/P2 off
				relay[ind][0].setChecked(True)
				relay[ind][1].setChecked(False)

			elif 0x130000 & x == 0x130000: #P1 off/P2 on
				relay[ind][0].setChecked(False)
				relay[ind][1].setChecked(True)
			
			else: #both on
				relay[ind][0].setChecked(True)
				relay[ind][1].setChecked(True)

	def closeEvent(self,event):
		reply = QtWidgets.QMessageBox.question(self,'Window Close', 'Are you sure you want to close the window?',
			QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.Yes:
			self.lpthread.stop(); self.hpthread.stop()
			for x in range(28):
				x += 1
				self.relay_off(x)
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
		while True:
			for s in range(61): #9 LP outside (sensor#27-29,56-61)
				if s in [26,27,28,55,56,57,58,59,60]:
					pass
				elif 0 <= s <= 20:
					pass
				else:
					lpboard = lp.getTemp(s)
					lptemp = lpboard[0]
					Rstatus = lpboard[1]
					self.signal.emit([s,lptemp,Rstatus])
					time.sleep(1)	
	def stop(self):
		self.terminate()

class RelayThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self):
		QThread.__init__(self)

	def run(self):
		while True:
			Rstatus = lp.getTemp(s)[1]
					

#PID loop will operate automatically and toggle relays. For now, just have the functionallity to manually toggle relays?
def main():
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())

if __name__=='__main__':
	main()


