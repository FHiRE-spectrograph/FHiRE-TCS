# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tcs.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TCS(object):
    def setupUi(self, TCS):
        TCS.setObjectName("TCS")
        TCS.resize(1320, 850)
        TCS.setMinimumSize(QtCore.QSize(1320, 850))
        TCS.setMaximumSize(QtCore.QSize(1320, 850))
        font = QtGui.QFont()
        font.setPointSize(10)
        TCS.setFont(font)
        TCS.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralWidget = QtWidgets.QWidget(TCS)
        self.centralWidget.setObjectName("centralWidget")
        self.gb_hpsensors = QtWidgets.QGroupBox(self.centralWidget)
        self.gb_hpsensors.setGeometry(QtCore.QRect(10, 0, 151, 441))
        self.gb_hpsensors.setObjectName("gb_hpsensors")
        self.cb_hp1 = QtWidgets.QCheckBox(self.gb_hpsensors)
        self.cb_hp1.setGeometry(QtCore.QRect(20, 30, 100, 20))
        self.cb_hp1.setObjectName("cb_hp1")
        self.cb_hp2 = QtWidgets.QCheckBox(self.gb_hpsensors)
        self.cb_hp2.setGeometry(QtCore.QRect(20, 70, 100, 20))
        self.cb_hp2.setObjectName("cb_hp2")
        self.cb_hp3 = QtWidgets.QCheckBox(self.gb_hpsensors)
        self.cb_hp3.setGeometry(QtCore.QRect(20, 110, 100, 20))
        self.cb_hp3.setObjectName("cb_hp3")
        self.cb_hp4 = QtWidgets.QCheckBox(self.gb_hpsensors)
        self.cb_hp4.setGeometry(QtCore.QRect(20, 150, 100, 20))
        self.cb_hp4.setObjectName("cb_hp4")
        self.cb_hp5 = QtWidgets.QCheckBox(self.gb_hpsensors)
        self.cb_hp5.setGeometry(QtCore.QRect(20, 190, 100, 20))
        self.cb_hp5.setObjectName("cb_hp5")
        self.cb_hp6 = QtWidgets.QCheckBox(self.gb_hpsensors)
        self.cb_hp6.setGeometry(QtCore.QRect(20, 230, 100, 20))
        self.cb_hp6.setObjectName("cb_hp6")
        self.cb_hp7 = QtWidgets.QCheckBox(self.gb_hpsensors)
        self.cb_hp7.setGeometry(QtCore.QRect(20, 270, 100, 20))
        self.cb_hp7.setObjectName("cb_hp7")
        self.cb_hp8 = QtWidgets.QCheckBox(self.gb_hpsensors)
        self.cb_hp8.setGeometry(QtCore.QRect(20, 310, 100, 20))
        self.cb_hp8.setObjectName("cb_hp8")
        self.cb_hp9 = QtWidgets.QCheckBox(self.gb_hpsensors)
        self.cb_hp9.setGeometry(QtCore.QRect(20, 350, 100, 20))
        self.cb_hp9.setObjectName("cb_hp9")
        self.cb_hp10 = QtWidgets.QCheckBox(self.gb_hpsensors)
        self.cb_hp10.setGeometry(QtCore.QRect(20, 390, 100, 20))
        self.cb_hp10.setObjectName("cb_hp10")
        self.gb_heaters = QtWidgets.QGroupBox(self.centralWidget)
        self.gb_heaters.setGeometry(QtCore.QRect(10, 580, 701, 221))
        self.gb_heaters.setObjectName("gb_heaters")
        self.gb_heatersbtm = QtWidgets.QGroupBox(self.gb_heaters)
        self.gb_heatersbtm.setGeometry(QtCore.QRect(10, 20, 381, 191))
        self.gb_heatersbtm.setObjectName("gb_heatersbtm")
        self.pb_h1 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h1.setGeometry(QtCore.QRect(10, 30, 30, 30))
        self.pb_h1.setObjectName("pb_h1")
        self.lb_h1 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h1.setGeometry(QtCore.QRect(40, 30, 40, 30))
        self.lb_h1.setObjectName("lb_h1")
        self.pb_h2 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h2.setGeometry(QtCore.QRect(10, 70, 30, 30))
        self.pb_h2.setObjectName("pb_h2")
        self.lb_h2 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h2.setGeometry(QtCore.QRect(40, 70, 40, 30))
        self.lb_h2.setObjectName("lb_h2")
        self.pb_h3 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h3.setGeometry(QtCore.QRect(10, 110, 30, 30))
        self.pb_h3.setObjectName("pb_h3")
        self.lb_h3 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h3.setGeometry(QtCore.QRect(40, 110, 40, 30))
        self.lb_h3.setObjectName("lb_h3")
        self.pb_h4 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h4.setGeometry(QtCore.QRect(10, 150, 30, 30))
        self.pb_h4.setObjectName("pb_h4")
        self.lb_h4 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h4.setGeometry(QtCore.QRect(40, 150, 40, 30))
        self.lb_h4.setObjectName("lb_h4")
        self.lb_h8 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h8.setGeometry(QtCore.QRect(130, 150, 40, 30))
        self.lb_h8.setObjectName("lb_h8")
        self.pb_h5 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h5.setGeometry(QtCore.QRect(100, 30, 30, 30))
        self.pb_h5.setObjectName("pb_h5")
        self.lb_h5 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h5.setGeometry(QtCore.QRect(130, 30, 40, 30))
        self.lb_h5.setObjectName("lb_h5")
        self.lb_h7 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h7.setGeometry(QtCore.QRect(130, 110, 40, 30))
        self.lb_h7.setObjectName("lb_h7")
        self.pb_h7 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h7.setGeometry(QtCore.QRect(100, 110, 30, 30))
        self.pb_h7.setObjectName("pb_h7")
        self.pb_h8 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h8.setGeometry(QtCore.QRect(100, 150, 30, 30))
        self.pb_h8.setObjectName("pb_h8")
        self.lb_h6 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h6.setGeometry(QtCore.QRect(130, 70, 40, 30))
        self.lb_h6.setObjectName("lb_h6")
        self.pb_h6 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h6.setGeometry(QtCore.QRect(100, 70, 30, 30))
        self.pb_h6.setObjectName("pb_h6")
        self.lb_h12 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h12.setGeometry(QtCore.QRect(220, 150, 40, 30))
        self.lb_h12.setObjectName("lb_h12")
        self.lb_h9 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h9.setGeometry(QtCore.QRect(220, 30, 40, 30))
        self.lb_h9.setObjectName("lb_h9")
        self.pb_h11 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h11.setGeometry(QtCore.QRect(190, 110, 30, 30))
        self.pb_h11.setObjectName("pb_h11")
        self.lb_h10 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h10.setGeometry(QtCore.QRect(220, 70, 40, 30))
        self.lb_h10.setObjectName("lb_h10")
        self.pb_h10 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h10.setGeometry(QtCore.QRect(190, 70, 30, 30))
        self.pb_h10.setObjectName("pb_h10")
        self.pb_h12 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h12.setGeometry(QtCore.QRect(190, 150, 30, 30))
        self.pb_h12.setObjectName("pb_h12")
        self.lb_h11 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h11.setGeometry(QtCore.QRect(220, 110, 40, 30))
        self.lb_h11.setObjectName("lb_h11")
        self.pb_h9 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h9.setGeometry(QtCore.QRect(190, 30, 30, 30))
        self.pb_h9.setObjectName("pb_h9")
        self.lb_h16 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h16.setGeometry(QtCore.QRect(310, 150, 40, 30))
        self.lb_h16.setObjectName("lb_h16")
        self.lb_h13 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h13.setGeometry(QtCore.QRect(310, 30, 40, 30))
        self.lb_h13.setObjectName("lb_h13")
        self.pb_h15 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h15.setGeometry(QtCore.QRect(280, 110, 30, 30))
        self.pb_h15.setObjectName("pb_h15")
        self.lb_h14 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h14.setGeometry(QtCore.QRect(310, 70, 40, 30))
        self.lb_h14.setObjectName("lb_h14")
        self.pb_h14 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h14.setGeometry(QtCore.QRect(280, 70, 30, 30))
        self.pb_h14.setObjectName("pb_h14")
        self.pb_h16 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h16.setGeometry(QtCore.QRect(280, 150, 30, 30))
        self.pb_h16.setObjectName("pb_h16")
        self.lb_h15 = QtWidgets.QLabel(self.gb_heatersbtm)
        self.lb_h15.setGeometry(QtCore.QRect(310, 110, 40, 30))
        self.lb_h15.setObjectName("lb_h15")
        self.pb_h13 = QtWidgets.QPushButton(self.gb_heatersbtm)
        self.pb_h13.setGeometry(QtCore.QRect(280, 30, 30, 30))
        self.pb_h13.setObjectName("pb_h13")
        self.gb_heaterstop = QtWidgets.QGroupBox(self.gb_heaters)
        self.gb_heaterstop.setGeometry(QtCore.QRect(400, 20, 291, 191))
        self.gb_heaterstop.setObjectName("gb_heaterstop")
        self.pb_h4_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h4_top.setGeometry(QtCore.QRect(10, 150, 30, 30))
        self.pb_h4_top.setObjectName("pb_h4_top")
        self.pb_h5_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h5_top.setGeometry(QtCore.QRect(100, 30, 30, 30))
        self.pb_h5_top.setObjectName("pb_h5_top")
        self.lb_h3_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h3_top.setGeometry(QtCore.QRect(40, 110, 40, 30))
        self.lb_h3_top.setObjectName("lb_h3_top")
        self.pb_h7_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h7_top.setGeometry(QtCore.QRect(100, 110, 30, 30))
        self.pb_h7_top.setObjectName("pb_h7_top")
        self.lb_h8_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h8_top.setGeometry(QtCore.QRect(130, 150, 40, 30))
        self.lb_h8_top.setObjectName("lb_h8_top")
        self.lb_h10_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h10_top.setGeometry(QtCore.QRect(220, 70, 40, 30))
        self.lb_h10_top.setObjectName("lb_h10_top")
        self.lb_h6_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h6_top.setGeometry(QtCore.QRect(130, 70, 40, 30))
        self.lb_h6_top.setObjectName("lb_h6_top")
        self.lb_h11_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h11_top.setGeometry(QtCore.QRect(220, 110, 40, 30))
        self.lb_h11_top.setObjectName("lb_h11_top")
        self.lb_h2_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h2_top.setGeometry(QtCore.QRect(40, 70, 40, 30))
        self.lb_h2_top.setObjectName("lb_h2_top")
        self.pb_h12_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h12_top.setGeometry(QtCore.QRect(190, 150, 30, 30))
        self.pb_h12_top.setObjectName("pb_h12_top")
        self.lb_h1_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h1_top.setGeometry(QtCore.QRect(40, 30, 40, 30))
        self.lb_h1_top.setObjectName("lb_h1_top")
        self.pb_h6_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h6_top.setGeometry(QtCore.QRect(100, 70, 30, 30))
        self.pb_h6_top.setObjectName("pb_h6_top")
        self.lb_h7_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h7_top.setGeometry(QtCore.QRect(130, 110, 40, 30))
        self.lb_h7_top.setObjectName("lb_h7_top")
        self.pb_h11_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h11_top.setGeometry(QtCore.QRect(190, 110, 30, 30))
        self.pb_h11_top.setObjectName("pb_h11_top")
        self.pb_h8_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h8_top.setGeometry(QtCore.QRect(100, 150, 30, 30))
        self.pb_h8_top.setObjectName("pb_h8_top")
        self.lb_h4_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h4_top.setGeometry(QtCore.QRect(40, 150, 40, 30))
        self.lb_h4_top.setObjectName("lb_h4_top")
        self.lb_h12_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h12_top.setGeometry(QtCore.QRect(220, 150, 40, 30))
        self.lb_h12_top.setObjectName("lb_h12_top")
        self.pb_h2_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h2_top.setGeometry(QtCore.QRect(10, 70, 30, 30))
        self.pb_h2_top.setObjectName("pb_h2_top")
        self.lb_h5_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h5_top.setGeometry(QtCore.QRect(130, 30, 40, 30))
        self.lb_h5_top.setObjectName("lb_h5_top")
        self.pb_h9_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h9_top.setGeometry(QtCore.QRect(190, 30, 30, 30))
        self.pb_h9_top.setObjectName("pb_h9_top")
        self.pb_h1_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h1_top.setGeometry(QtCore.QRect(10, 30, 30, 30))
        self.pb_h1_top.setObjectName("pb_h1_top")
        self.lb_h9_top = QtWidgets.QLabel(self.gb_heaterstop)
        self.lb_h9_top.setGeometry(QtCore.QRect(220, 30, 40, 30))
        self.lb_h9_top.setObjectName("lb_h9_top")
        self.pb_h3_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h3_top.setGeometry(QtCore.QRect(10, 110, 30, 30))
        self.pb_h3_top.setObjectName("pb_h3_top")
        self.pb_h10_top = QtWidgets.QPushButton(self.gb_heaterstop)
        self.pb_h10_top.setGeometry(QtCore.QRect(190, 70, 30, 30))
        self.pb_h10_top.setObjectName("pb_h10_top")
        self.gb_lpsensorstop = QtWidgets.QGroupBox(self.centralWidget)
        self.gb_lpsensorstop.setGeometry(QtCore.QRect(1020, 0, 291, 801))
        self.gb_lpsensorstop.setObjectName("gb_lpsensorstop")
        self.gb_resisterstop = QtWidgets.QGroupBox(self.gb_lpsensorstop)
        self.gb_resisterstop.setGeometry(QtCore.QRect(10, 20, 271, 381))
        self.gb_resisterstop.setObjectName("gb_resisterstop")
        self.cb_lp10_top = QtWidgets.QCheckBox(self.gb_resisterstop)
        self.cb_lp10_top.setGeometry(QtCore.QRect(20, 190, 105, 20))
        self.cb_lp10_top.setObjectName("cb_lp10_top")
        self.cb_lp14_top = QtWidgets.QCheckBox(self.gb_resisterstop)
        self.cb_lp14_top.setGeometry(QtCore.QRect(20, 270, 105, 20))
        self.cb_lp14_top.setObjectName("cb_lp14_top")
        self.cb_lp2_top = QtWidgets.QCheckBox(self.gb_resisterstop)
        self.cb_lp2_top.setGeometry(QtCore.QRect(20, 30, 105, 20))
        self.cb_lp2_top.setObjectName("cb_lp2_top")
        self.cb_lp6_top = QtWidgets.QCheckBox(self.gb_resisterstop)
        self.cb_lp6_top.setGeometry(QtCore.QRect(20, 110, 105, 20))
        self.cb_lp6_top.setObjectName("cb_lp6_top")
        self.cb_lp12_top = QtWidgets.QCheckBox(self.gb_resisterstop)
        self.cb_lp12_top.setGeometry(QtCore.QRect(20, 230, 105, 20))
        self.cb_lp12_top.setObjectName("cb_lp12_top")
        self.cb_lp8_top = QtWidgets.QCheckBox(self.gb_resisterstop)
        self.cb_lp8_top.setGeometry(QtCore.QRect(20, 150, 105, 20))
        self.cb_lp8_top.setObjectName("cb_lp8_top")
        self.cb_lp4_top = QtWidgets.QCheckBox(self.gb_resisterstop)
        self.cb_lp4_top.setGeometry(QtCore.QRect(20, 70, 105, 20))
        self.cb_lp4_top.setObjectName("cb_lp4_top")
        self.cb_lp16_top = QtWidgets.QCheckBox(self.gb_resisterstop)
        self.cb_lp16_top.setGeometry(QtCore.QRect(20, 310, 105, 20))
        self.cb_lp16_top.setObjectName("cb_lp16_top")
        self.cb_lp18_top = QtWidgets.QCheckBox(self.gb_resisterstop)
        self.cb_lp18_top.setGeometry(QtCore.QRect(20, 350, 105, 20))
        self.cb_lp18_top.setObjectName("cb_lp18_top")
        self.gb_diodetop = QtWidgets.QGroupBox(self.gb_lpsensorstop)
        self.gb_diodetop.setGeometry(QtCore.QRect(10, 410, 271, 381))
        self.gb_diodetop.setObjectName("gb_diodetop")
        self.cb_lp21_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp21_top.setGeometry(QtCore.QRect(140, 70, 105, 20))
        self.cb_lp21_top.setObjectName("cb_lp21_top")
        self.cb_lp23_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp23_top.setGeometry(QtCore.QRect(140, 110, 105, 20))
        self.cb_lp23_top.setObjectName("cb_lp23_top")
        self.cb_lp13_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp13_top.setGeometry(QtCore.QRect(20, 270, 105, 20))
        self.cb_lp13_top.setObjectName("cb_lp13_top")
        self.cb_lp1_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp1_top.setGeometry(QtCore.QRect(20, 30, 105, 20))
        self.cb_lp1_top.setObjectName("cb_lp1_top")
        self.cb_lp11_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp11_top.setGeometry(QtCore.QRect(20, 230, 105, 20))
        self.cb_lp11_top.setObjectName("cb_lp11_top")
        self.cb_lp9_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp9_top.setGeometry(QtCore.QRect(20, 190, 105, 20))
        self.cb_lp9_top.setObjectName("cb_lp9_top")
        self.cb_lp7_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp7_top.setGeometry(QtCore.QRect(20, 150, 105, 20))
        self.cb_lp7_top.setObjectName("cb_lp7_top")
        self.cb_lp17_btm_2 = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp17_btm_2.setGeometry(QtCore.QRect(20, 350, 105, 20))
        self.cb_lp17_btm_2.setObjectName("cb_lp17_btm_2")
        self.cb_lp5_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp5_top.setGeometry(QtCore.QRect(20, 110, 105, 20))
        self.cb_lp5_top.setObjectName("cb_lp5_top")
        self.cb_lp19_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp19_top.setGeometry(QtCore.QRect(140, 30, 105, 20))
        self.cb_lp19_top.setObjectName("cb_lp19_top")
        self.cb_lp15_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp15_top.setGeometry(QtCore.QRect(20, 310, 105, 20))
        self.cb_lp15_top.setObjectName("cb_lp15_top")
        self.cb_lp3_top = QtWidgets.QCheckBox(self.gb_diodetop)
        self.cb_lp3_top.setGeometry(QtCore.QRect(20, 70, 105, 20))
        self.cb_lp3_top.setObjectName("cb_lp3_top")
        self.gb_lpsensorsbtm = QtWidgets.QGroupBox(self.centralWidget)
        self.gb_lpsensorsbtm.setGeometry(QtCore.QRect(720, 0, 291, 801))
        self.gb_lpsensorsbtm.setObjectName("gb_lpsensorsbtm")
        self.gb_resistersbtm = QtWidgets.QGroupBox(self.gb_lpsensorsbtm)
        self.gb_resistersbtm.setGeometry(QtCore.QRect(10, 20, 271, 381))
        self.gb_resistersbtm.setObjectName("gb_resistersbtm")
        self.cb_lp10_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp10_btm.setGeometry(QtCore.QRect(20, 190, 105, 20))
        self.cb_lp10_btm.setObjectName("cb_lp10_btm")
        self.cb_lp8_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp8_btm.setGeometry(QtCore.QRect(20, 150, 105, 20))
        self.cb_lp8_btm.setObjectName("cb_lp8_btm")
        self.cb_lp18_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp18_btm.setGeometry(QtCore.QRect(20, 350, 105, 20))
        self.cb_lp18_btm.setObjectName("cb_lp18_btm")
        self.cb_lp14_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp14_btm.setGeometry(QtCore.QRect(20, 270, 105, 20))
        self.cb_lp14_btm.setObjectName("cb_lp14_btm")
        self.cb_lp2_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp2_btm.setGeometry(QtCore.QRect(20, 30, 105, 20))
        self.cb_lp2_btm.setObjectName("cb_lp2_btm")
        self.cb_lp12_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp12_btm.setGeometry(QtCore.QRect(20, 230, 105, 20))
        self.cb_lp12_btm.setObjectName("cb_lp12_btm")
        self.cb_lp4_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp4_btm.setGeometry(QtCore.QRect(20, 70, 105, 20))
        self.cb_lp4_btm.setObjectName("cb_lp4_btm")
        self.cb_lp6_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp6_btm.setGeometry(QtCore.QRect(20, 110, 105, 20))
        self.cb_lp6_btm.setObjectName("cb_lp6_btm")
        self.cb_lp16_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp16_btm.setGeometry(QtCore.QRect(20, 310, 105, 20))
        self.cb_lp16_btm.setObjectName("cb_lp16_btm")
        self.cb_lp28_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp28_btm.setGeometry(QtCore.QRect(140, 190, 105, 20))
        self.cb_lp28_btm.setObjectName("cb_lp28_btm")
        self.cb_lp20_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp20_btm.setGeometry(QtCore.QRect(140, 30, 105, 20))
        self.cb_lp20_btm.setObjectName("cb_lp20_btm")
        self.cb_lp24_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp24_btm.setGeometry(QtCore.QRect(140, 110, 105, 20))
        self.cb_lp24_btm.setObjectName("cb_lp24_btm")
        self.cb_lp30_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp30_btm.setGeometry(QtCore.QRect(140, 230, 105, 20))
        self.cb_lp30_btm.setObjectName("cb_lp30_btm")
        self.cb_lp26_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp26_btm.setGeometry(QtCore.QRect(140, 150, 105, 20))
        self.cb_lp26_btm.setObjectName("cb_lp26_btm")
        self.cb_lp22_btm = QtWidgets.QCheckBox(self.gb_resistersbtm)
        self.cb_lp22_btm.setGeometry(QtCore.QRect(140, 70, 105, 20))
        self.cb_lp22_btm.setObjectName("cb_lp22_btm")
        self.gb_diodebtm = QtWidgets.QGroupBox(self.gb_lpsensorsbtm)
        self.gb_diodebtm.setGeometry(QtCore.QRect(10, 410, 271, 381))
        self.gb_diodebtm.setObjectName("gb_diodebtm")
        self.cb_lp9_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp9_btm.setGeometry(QtCore.QRect(20, 190, 105, 20))
        self.cb_lp9_btm.setObjectName("cb_lp9_btm")
        self.cb_lp13_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp13_btm.setGeometry(QtCore.QRect(20, 270, 105, 20))
        self.cb_lp13_btm.setObjectName("cb_lp13_btm")
        self.cb_lp1_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp1_btm.setGeometry(QtCore.QRect(20, 30, 105, 20))
        self.cb_lp1_btm.setObjectName("cb_lp1_btm")
        self.cb_lp5_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp5_btm.setGeometry(QtCore.QRect(20, 110, 105, 20))
        self.cb_lp5_btm.setObjectName("cb_lp5_btm")
        self.cb_lp21_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp21_btm.setGeometry(QtCore.QRect(140, 70, 105, 20))
        self.cb_lp21_btm.setObjectName("cb_lp21_btm")
        self.cb_lp11_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp11_btm.setGeometry(QtCore.QRect(20, 230, 105, 20))
        self.cb_lp11_btm.setObjectName("cb_lp11_btm")
        self.cb_lp23_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp23_btm.setGeometry(QtCore.QRect(140, 110, 105, 20))
        self.cb_lp23_btm.setObjectName("cb_lp23_btm")
        self.cb_lp19_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp19_btm.setGeometry(QtCore.QRect(140, 30, 105, 20))
        self.cb_lp19_btm.setObjectName("cb_lp19_btm")
        self.cb_lp7_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp7_btm.setGeometry(QtCore.QRect(20, 150, 105, 20))
        self.cb_lp7_btm.setObjectName("cb_lp7_btm")
        self.cb_lp29_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp29_btm.setGeometry(QtCore.QRect(140, 230, 105, 20))
        self.cb_lp29_btm.setObjectName("cb_lp29_btm")
        self.cb_lp27_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp27_btm.setGeometry(QtCore.QRect(140, 190, 105, 20))
        self.cb_lp27_btm.setObjectName("cb_lp27_btm")
        self.cb_lp3_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp3_btm.setGeometry(QtCore.QRect(20, 70, 105, 20))
        self.cb_lp3_btm.setObjectName("cb_lp3_btm")
        self.cb_lp15_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp15_btm.setGeometry(QtCore.QRect(20, 310, 105, 20))
        self.cb_lp15_btm.setObjectName("cb_lp15_btm")
        self.cb_lp25_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp25_btm.setGeometry(QtCore.QRect(140, 150, 105, 20))
        self.cb_lp25_btm.setObjectName("cb_lp25_btm")
        self.cb_lp17_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp17_btm.setGeometry(QtCore.QRect(20, 350, 105, 20))
        self.cb_lp17_btm.setObjectName("cb_lp17_btm")
        self.cb_lp31_btm = QtWidgets.QCheckBox(self.gb_diodebtm)
        self.cb_lp31_btm.setGeometry(QtCore.QRect(140, 270, 105, 20))
        self.cb_lp31_btm.setObjectName("cb_lp31_btm")
        self.gb_graph = QtWidgets.QGroupBox(self.centralWidget)
        self.gb_graph.setGeometry(QtCore.QRect(170, 0, 541, 571))
        self.gb_graph.setObjectName("gb_graph")
        self.graphWidget = PlotWidget(self.gb_graph)
        self.graphWidget.setGeometry(QtCore.QRect(10, 30, 521, 531))
        self.graphWidget.setObjectName("graphWidget")
        self.gb_cal = QtWidgets.QGroupBox(self.centralWidget)
        self.gb_cal.setGeometry(QtCore.QRect(10, 440, 151, 131))
        self.gb_cal.setObjectName("gb_cal")
        self.lb_p = QtWidgets.QLabel(self.gb_cal)
        self.lb_p.setGeometry(QtCore.QRect(30, 40, 40, 20))
        self.lb_p.setObjectName("lb_p")
        self.lb_i = QtWidgets.QLabel(self.gb_cal)
        self.lb_i.setGeometry(QtCore.QRect(30, 70, 40, 20))
        self.lb_i.setObjectName("lb_i")
        self.lb_d = QtWidgets.QLabel(self.gb_cal)
        self.lb_d.setGeometry(QtCore.QRect(30, 100, 40, 20))
        self.lb_d.setObjectName("lb_d")
        self.ln_p = QtWidgets.QLineEdit(self.gb_cal)
        self.ln_p.setGeometry(QtCore.QRect(50, 40, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ln_p.setFont(font)
        self.ln_p.setObjectName("ln_p")
        self.ln_i = QtWidgets.QLineEdit(self.gb_cal)
        self.ln_i.setGeometry(QtCore.QRect(50, 70, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ln_i.setFont(font)
        self.ln_i.setObjectName("ln_i")
        self.ln_d = QtWidgets.QLineEdit(self.gb_cal)
        self.ln_d.setGeometry(QtCore.QRect(50, 100, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ln_d.setFont(font)
        self.ln_d.setObjectName("ln_d")
        self.pb_p = QtWidgets.QPushButton(self.gb_cal)
        self.pb_p.setGeometry(QtCore.QRect(110, 40, 20, 20))
        self.pb_p.setObjectName("pb_p")
        self.pb_i = QtWidgets.QPushButton(self.gb_cal)
        self.pb_i.setGeometry(QtCore.QRect(110, 70, 20, 20))
        self.pb_i.setObjectName("pb_i")
        self.pb_d = QtWidgets.QPushButton(self.gb_cal)
        self.pb_d.setGeometry(QtCore.QRect(110, 100, 20, 20))
        self.pb_d.setObjectName("pb_d")
        TCS.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(TCS)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1320, 17))
        self.menuBar.setObjectName("menuBar")
        TCS.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(TCS)
        self.mainToolBar.setObjectName("mainToolBar")
        TCS.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(TCS)
        self.statusBar.setObjectName("statusBar")
        TCS.setStatusBar(self.statusBar)

        self.retranslateUi(TCS)
        QtCore.QMetaObject.connectSlotsByName(TCS)

    def retranslateUi(self, TCS):
        _translate = QtCore.QCoreApplication.translate
        TCS.setWindowTitle(_translate("TCS", "TCS"))
        self.gb_hpsensors.setTitle(_translate("TCS", "HP Sensors"))
        self.cb_hp1.setText(_translate("TCS", "1: --- C"))
        self.cb_hp2.setText(_translate("TCS", "2: --- C"))
        self.cb_hp3.setText(_translate("TCS", "3: --- C"))
        self.cb_hp4.setText(_translate("TCS", "4: --- C"))
        self.cb_hp5.setText(_translate("TCS", "5: --- C"))
        self.cb_hp6.setText(_translate("TCS", "6: --- C"))
        self.cb_hp7.setText(_translate("TCS", "7: --- C"))
        self.cb_hp8.setText(_translate("TCS", "8: --- C"))
        self.cb_hp9.setText(_translate("TCS", "9: --- C"))
        self.cb_hp10.setText(_translate("TCS", "10: --- C"))
        self.gb_heaters.setTitle(_translate("TCS", "Heaters"))
        self.gb_heatersbtm.setTitle(_translate("TCS", "Bottom"))
        self.pb_h1.setText(_translate("TCS", "1"))
        self.lb_h1.setText(_translate("TCS", "10%"))
        self.pb_h2.setText(_translate("TCS", "2"))
        self.lb_h2.setText(_translate("TCS", "--%"))
        self.pb_h3.setText(_translate("TCS", "3"))
        self.lb_h3.setText(_translate("TCS", "--%"))
        self.pb_h4.setText(_translate("TCS", "4"))
        self.lb_h4.setText(_translate("TCS", "--%"))
        self.lb_h8.setText(_translate("TCS", "--%"))
        self.pb_h5.setText(_translate("TCS", "5"))
        self.lb_h5.setText(_translate("TCS", "--%"))
        self.lb_h7.setText(_translate("TCS", "--%"))
        self.pb_h7.setText(_translate("TCS", "7"))
        self.pb_h8.setText(_translate("TCS", "8"))
        self.lb_h6.setText(_translate("TCS", "--%"))
        self.pb_h6.setText(_translate("TCS", "6"))
        self.lb_h12.setText(_translate("TCS", "--%"))
        self.lb_h9.setText(_translate("TCS", "--%"))
        self.pb_h11.setText(_translate("TCS", "11"))
        self.lb_h10.setText(_translate("TCS", "--%"))
        self.pb_h10.setText(_translate("TCS", "10"))
        self.pb_h12.setText(_translate("TCS", "12"))
        self.lb_h11.setText(_translate("TCS", "--%"))
        self.pb_h9.setText(_translate("TCS", "9"))
        self.lb_h16.setText(_translate("TCS", "--%"))
        self.lb_h13.setText(_translate("TCS", "--%"))
        self.pb_h15.setText(_translate("TCS", "15"))
        self.lb_h14.setText(_translate("TCS", "--%"))
        self.pb_h14.setText(_translate("TCS", "14"))
        self.pb_h16.setText(_translate("TCS", "16"))
        self.lb_h15.setText(_translate("TCS", "--%"))
        self.pb_h13.setText(_translate("TCS", "13"))
        self.gb_heaterstop.setTitle(_translate("TCS", "Top"))
        self.pb_h4_top.setText(_translate("TCS", "4"))
        self.pb_h5_top.setText(_translate("TCS", "5"))
        self.lb_h3_top.setText(_translate("TCS", "--%"))
        self.pb_h7_top.setText(_translate("TCS", "7"))
        self.lb_h8_top.setText(_translate("TCS", "--%"))
        self.lb_h10_top.setText(_translate("TCS", "--%"))
        self.lb_h6_top.setText(_translate("TCS", "--%"))
        self.lb_h11_top.setText(_translate("TCS", "--%"))
        self.lb_h2_top.setText(_translate("TCS", "--%"))
        self.pb_h12_top.setText(_translate("TCS", "12"))
        self.lb_h1_top.setText(_translate("TCS", "10%"))
        self.pb_h6_top.setText(_translate("TCS", "6"))
        self.lb_h7_top.setText(_translate("TCS", "--%"))
        self.pb_h11_top.setText(_translate("TCS", "11"))
        self.pb_h8_top.setText(_translate("TCS", "8"))
        self.lb_h4_top.setText(_translate("TCS", "--%"))
        self.lb_h12_top.setText(_translate("TCS", "--%"))
        self.pb_h2_top.setText(_translate("TCS", "2"))
        self.lb_h5_top.setText(_translate("TCS", "--%"))
        self.pb_h9_top.setText(_translate("TCS", "9"))
        self.pb_h1_top.setText(_translate("TCS", "1"))
        self.lb_h9_top.setText(_translate("TCS", "--%"))
        self.pb_h3_top.setText(_translate("TCS", "3"))
        self.pb_h10_top.setText(_translate("TCS", "10"))
        self.gb_lpsensorstop.setTitle(_translate("TCS", "LP Sensors - Top"))
        self.gb_resisterstop.setTitle(_translate("TCS", "Resistors"))
        self.cb_lp10_top.setText(_translate("TCS", "10: --- C"))
        self.cb_lp14_top.setText(_translate("TCS", "14: --- C"))
        self.cb_lp2_top.setText(_translate("TCS", "2: --- C"))
        self.cb_lp6_top.setText(_translate("TCS", "6: --- C"))
        self.cb_lp12_top.setText(_translate("TCS", "12: --- C"))
        self.cb_lp8_top.setText(_translate("TCS", "8: --- C"))
        self.cb_lp4_top.setText(_translate("TCS", "4: --- C"))
        self.cb_lp16_top.setText(_translate("TCS", "16: --- C"))
        self.cb_lp18_top.setText(_translate("TCS", "18: --- C"))
        self.gb_diodetop.setTitle(_translate("TCS", "Diodes"))
        self.cb_lp21_top.setText(_translate("TCS", "21: --- C"))
        self.cb_lp23_top.setText(_translate("TCS", "23: --- C"))
        self.cb_lp13_top.setText(_translate("TCS", "13: --- C"))
        self.cb_lp1_top.setText(_translate("TCS", "1: --- C"))
        self.cb_lp11_top.setText(_translate("TCS", "11: --- C"))
        self.cb_lp9_top.setText(_translate("TCS", "9: --- C"))
        self.cb_lp7_top.setText(_translate("TCS", "7: --- C"))
        self.cb_lp17_btm_2.setText(_translate("TCS", "17: --- C"))
        self.cb_lp5_top.setText(_translate("TCS", "5: --- C"))
        self.cb_lp19_top.setText(_translate("TCS", "19: --- C"))
        self.cb_lp15_top.setText(_translate("TCS", "15: --- C"))
        self.cb_lp3_top.setText(_translate("TCS", "3: --- C"))
        self.gb_lpsensorsbtm.setTitle(_translate("TCS", "LP Sensors - Bottom"))
        self.gb_resistersbtm.setTitle(_translate("TCS", "Resistors"))
        self.cb_lp10_btm.setText(_translate("TCS", "10: --- C"))
        self.cb_lp8_btm.setText(_translate("TCS", "8: --- C"))
        self.cb_lp18_btm.setText(_translate("TCS", "18: --- C"))
        self.cb_lp14_btm.setText(_translate("TCS", "14: --- C"))
        self.cb_lp2_btm.setText(_translate("TCS", "2: --- C"))
        self.cb_lp12_btm.setText(_translate("TCS", "12: --- C"))
        self.cb_lp4_btm.setText(_translate("TCS", "4: --- C"))
        self.cb_lp6_btm.setText(_translate("TCS", "6: --- C"))
        self.cb_lp16_btm.setText(_translate("TCS", "16: --- C"))
        self.cb_lp28_btm.setText(_translate("TCS", "28: --- C"))
        self.cb_lp20_btm.setText(_translate("TCS", "20: --- C"))
        self.cb_lp24_btm.setText(_translate("TCS", "24: --- C"))
        self.cb_lp30_btm.setText(_translate("TCS", "30: --- C"))
        self.cb_lp26_btm.setText(_translate("TCS", "26: --- C"))
        self.cb_lp22_btm.setText(_translate("TCS", "22: --- C"))
        self.gb_diodebtm.setTitle(_translate("TCS", "Diodes"))
        self.cb_lp9_btm.setText(_translate("TCS", "9: --- C"))
        self.cb_lp13_btm.setText(_translate("TCS", "13: --- C"))
        self.cb_lp1_btm.setText(_translate("TCS", "1: --- C"))
        self.cb_lp5_btm.setText(_translate("TCS", "5: --- C"))
        self.cb_lp21_btm.setText(_translate("TCS", "21: --- C"))
        self.cb_lp11_btm.setText(_translate("TCS", "11: --- C"))
        self.cb_lp23_btm.setText(_translate("TCS", "23: --- C"))
        self.cb_lp19_btm.setText(_translate("TCS", "19: --- C"))
        self.cb_lp7_btm.setText(_translate("TCS", "7: --- C"))
        self.cb_lp29_btm.setText(_translate("TCS", "29: --- C"))
        self.cb_lp27_btm.setText(_translate("TCS", "27: --- C"))
        self.cb_lp3_btm.setText(_translate("TCS", "3: --- C"))
        self.cb_lp15_btm.setText(_translate("TCS", "15: --- C"))
        self.cb_lp25_btm.setText(_translate("TCS", "25: --- C"))
        self.cb_lp17_btm.setText(_translate("TCS", "17: --- C"))
        self.cb_lp31_btm.setText(_translate("TCS", "31: --- C"))
        self.gb_graph.setTitle(_translate("TCS", "Graph"))
        self.gb_cal.setTitle(_translate("TCS", "Calibration"))
        self.lb_p.setText(_translate("TCS", "P"))
        self.lb_i.setText(_translate("TCS", "I"))
        self.lb_d.setText(_translate("TCS", "D"))
        self.pb_p.setText(_translate("TCS", ">"))
        self.pb_i.setText(_translate("TCS", ">"))
        self.pb_d.setText(_translate("TCS", ">"))

from pyqtgraph import PlotWidget