#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
import sys, serial, os
import RPi.GPIO as GPIO
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from tcs import Ui_TCS
import TEMP as temp #HP sensor routine


ser=serial.Serial(port='/dev/serial0',baudrate=115200,bytesize=serial.EIGHTBITS,timeout=0)
#Relay:GPIO pin
relay={1:29,2:31,3:32,4:33,5:36,6:37,7:38,8:11,9:12,10:13,11:15,12:16,13:18,14:22,
	15:29,16:31,17:32,18:33,19:36,20:37,27:35,28:40}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
def GPIO_setup(pin):
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin,GPIO.HIGH)
	print "%s pin setup" %pin

def blockPrint():
	sys.stdout=open(os.devnull,'w')

blockPrint()
hp = temp.TEMP() #TEMP class of HP sensors *Does this initialize?*

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
			#h.clicked.connect(lambda:self.relay(h))
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
		self.pb_h10_top.clicked.connect(lambda:self.relay(self.pb_h10,26))
		self.pb_h11_top.clicked.connect(lambda:self.relay(self.pb_h11,27))
		self.pb_h12_top.clicked.connect(lambda:self.relay(self.pb_h12_top,28))

	def relay(self, btn, ind):
		if ind < 16:
			ind1="top: "+str(ind)
		elif ind >= 16:
			ind1="btm: "+str(ind-16)

		if btn.isChecked():
			if ind <= 6:
				#print relay[ind]
				GPIO.output(relay[ind],GPIO.LOW)
			elif 7 <= ind <= 20 or ind == 27 or ind == 28:
				#print ind
				ser.write(str(ind).strip('\r\n'))
			print "Relay "+ind1+" ON"
		else:
			if ind <= 6:
				GPIO.output(relay[ind],GPIO.HIGH)
			elif 7 <= ind <= 20 or ind == 27 or ind == 28:
				#print ind+100
				ser.write(str(ind+100).strip('\r\n'))
	
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
			

class HPSensorThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')

	def __init__(self):
		QThread.__init__(self)
	
	def run(self):
		while True:
			for s in range(7):
				hptemp = hp.getTemp(s)
				self.signal.emit([s,hptemp])


#PID loop will operate automatically and toggle relays. For now, just have the functionallity to manually toggle relays?

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

