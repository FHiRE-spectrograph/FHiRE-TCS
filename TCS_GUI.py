#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
import sys, serial, os
import RPi.GPIO as GPIO
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from tcs import Ui_TCS
import TEMP as temp #HP sensor routine
import low_p_temp_boards as lowp

ser=serial.Serial(port='/dev/serial0',baudrate=115200,bytesize=serial.EIGHTBITS,timeout=0)

#Relay:GPIO pin
relay={1:29,2:31,3:32,4:33,5:36,6:37,7:38,8:11,9:12,10:13,11:15,12:16,13:18,14:22,
	15:29,16:31,17:32,18:33,19:36,20:37,27:35,28:40}
#Relay:[CS GPIO - board,pin]
relay2={21:[38,1],22:[38,2],23:[11,1],24:[11,2],25:[12,1],26:[12,2]}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
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
		
		self.hpthread = HPSensorThread()
		#self.hpthread.start()
		self.hpthread.signal.connect(self.hp_update)

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
			if ind <= 6:
				GPIO.output(relay[ind],GPIO.LOW)
			elif 7 <= ind <= 20 or ind == 27 or ind == 28:
				ser.write(str(ind).strip('\r\n'))
			elif 21 <= ind <= 26:	
				lp.Relay_ON(relay2[ind][0],relay2[ind][1])

			print "Relay "+ind1+" ON"
		else:
			if ind <= 6:
				GPIO.output(relay[ind],GPIO.HIGH)
			elif 7 <= ind <= 20 or ind == 27 or ind == 28:
				ser.write(str(ind+100).strip('\r\n'))
			elif 21 <= ind <= 26:	
				lp.Relay_OFF(relay2[ind][0],relay2[ind][1])
	
			print "Relay "+ind1+" OFF"

	def hp_update(self, data):
		#print "HP UPDATE"
		objects = {
			0: self.cb_hp1.setText("%.2f C" %data[1]),
			1: self.cb_hp3.setText("%.2f C" %data[1]), 
			2: self.cb_hp4.setText("%.2f C" %data[1]),
			3: self.cb_hp5.setText("%.2f C" %data[1]),
			4: self.cb_hp6.setText("%.2f C" %data[1]),
			5: self.cb_hp8.setText("%.2f C" %data[1]),
			6: self.cb_hp9.setText("%.2f C" %data[1])} 
			#7: self.cb_hp8.setText("%.2f C" %data[1]),
			#8: self.cb_hp9.setText("%.2f C" %data[1]),
			#9: self.cb_hp10.setText("%.2f C" %data[1])} 
		if data[0] in objects.keys():
			objects[data[0]]

	def lp_update(self, data):
		#print "HP UPDATE"
		objects = {
			0: self.cb_lp1_top.setText("%.2f C" %data[1]),
			1: self.cb_lp2_top.setText("%.2f C" %data[1]), 
			2: self.cb_lp3_top.setText("%.2f C" %data[1]),
			3: self.cb_lp4_top.setText("%.2f C" %data[1]),
			4: self.cb_lp5_top.setText("%.2f C" %data[1]),
			5: self.cb_lp6_top.setText("%.2f C" %data[1]),
			6: self.cb_lp7_top.setText("%.2f C" %data[1]),
			7: self.cb_lp8_top.setText("%.2f C" %data[1]),
			8: self.cb_lp9_top.setText("%.2f C" %data[1]), 
			9: self.cb_lp10_top.setText("%.2f C" %data[1]),
			10: self.cb_lp11_top.setText("%.2f C" %data[1]),
			11: self.cb_lp12_top.setText("%.2f C" %data[1]),
			12: self.cb_lp13_top.setText("%.2f C" %data[1]),
			13: self.cb_lp14_top.setText("%.2f C" %data[1]),
			14: self.cb_lp15_top.setText("%.2f C" %data[1]),
			15: self.cb_lp16_top.setText("%.2f C" %data[1]),
			16: self.cb_lp17_top.setText("%.2f C" %data[1]), 
			17: self.cb_lp18_top.setText("%.2f C" %data[1]),
			18: self.cb_lp19_top.setText("%.2f C" %data[1]),
			19: self.cb_lp20_top.setText("%.2f C" %data[1]),
			20: self.cb_lp21_top.setText("%.2f C" %data[1]),

			21: self.cb_lp1_btm.setText("%.2f C" %data[1]),
			22: self.cb_lp2_btm.setText("%.2f C" %data[1]),
			23: self.cb_lp3_btm.setText("%.2f C" %data[1]),
			24: self.cb_lp4_btm.setText("%.2f C" %data[1]),
			25: self.cb_lp5_btm.setText("%.2f C" %data[1]),

			26: pass,
			27: pass, 
			28: pass,

			29: self.cb_lp6_btm.setText("%.2f C" %data[1]),
			30: self.cb_lp7_btm.setText("%.2f C" %data[1]),
			31: self.cb_lp8_btm.setText("%.2f C" %data[1]),
			32: self.cb_lp9_btm.setText("%.2f C" %data[1]),
			33: self.cb_lp10_btm.setText("%.2f C" %data[1]),
			34: self.cb_lp11_btm.setText("%.2f C" %data[1]),
			35: self.cb_lp12_btm.setText("%.2f C" %data[1]),
			36: self.cb_lp13_btm.setText("%.2f C" %data[1]),
			37: self.cb_lp14_btm.setText("%.2f C" %data[1]),
			38: self.cb_lp15_btm.setText("%.2f C" %data[1]), 
			39: self.cb_lp16_btm.setText("%.2f C" %data[1]),
			40: self.cb_lp17_btm.setText("%.2f C" %data[1]),
			41: self.cb_lp18_btm.setText("%.2f C" %data[1]),
			42: self.cb_lp19_btm.setText("%.2f C" %data[1]),
			43: self.cb_lp20_btm.setText("%.2f C" %data[1]),
			44: self.cb_lp21_btm.setText("%.2f C" %data[1]),
			45: self.cb_lp22_btm.setText("%.2f C" %data[1]),
			46: self.cb_lp23_btm.setText("%.2f C" %data[1]),
			47: self.cb_lp24_btm.setText("%.2f C" %data[1]), 
			48: self.cb_lp25_btm.setText("%.2f C" %data[1]),
			49: self.cb_lp26_btm.setText("%.2f C" %data[1]),
			50: self.cb_lp27_btm.setText("%.2f C" %data[1]),
			51: self.cb_lp28_btm.setText("%.2f C" %data[1]),
			52: self.cb_lp29_btm.setText("%.2f C" %data[1]),
			53: self.cb_lp30_btm.setText("%.2f C" %data[1]),
			54: self.cb_lp31_btm.setText("%.2f C" %data[1]),

			55: pass,
			56: pass, 
			57: pass,
			58: pass,
			59: pass,
			60: pass}

		if data[0] in objects.keys():
			objects[data[0]]	
			

class HPSensorThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self):
		QThread.__init__(self)
	
	def run(self):
		while True:
			for s in range(7):
				hptemp = hp.getTemp(s)
				self.signal.emit([s,hptemp])

class LPSensorThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self):
		QThread.__init__(self)

	def run(self):
		while True:
			for s in range(61): #9 LP outside (sensor#27-29,56-61)
				lptemp = lp.getTemp(s)
				self.signal.emit([s,lptemp])			


#PID loop will operate automatically and toggle relays. For now, just have the functionallity to manually toggle relays?

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

