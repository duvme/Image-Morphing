# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(30, 10, 180, 30))
        self.btn_start.setObjectName("btn_start")
        self.btn_end = QtWidgets.QPushButton(self.centralwidget)
        self.btn_end.setGeometry(QtCore.QRect(480, 10, 180, 30))
        self.btn_end.setObjectName("btn_end")
        self.box_end = QtWidgets.QGraphicsView(self.centralwidget)
        self.box_end.setGeometry(QtCore.QRect(480, 50, 360, 270))
        self.box_end.setObjectName("box_end")
        self.box_start = QtWidgets.QGraphicsView(self.centralwidget)
        self.box_start.setGeometry(QtCore.QRect(30, 50, 360, 270))
        self.box_start.setObjectName("box_start")
        self.Starting_Text = QtWidgets.QLabel(self.centralwidget)
        self.Starting_Text.setGeometry(QtCore.QRect(110, 330, 160, 30))
        self.Starting_Text.setObjectName("Starting_Text")
        self.Ending_Text = QtWidgets.QLabel(self.centralwidget)
        self.Ending_Text.setGeometry(QtCore.QRect(580, 330, 160, 30))
        self.Ending_Text.setObjectName("Ending_Text")
        self.check_triangles = QtWidgets.QCheckBox(self.centralwidget)
        self.check_triangles.setGeometry(QtCore.QRect(370, 340, 140, 30))
        self.check_triangles.setObjectName("check_triangles")
        self.slide_bar = QtWidgets.QSlider(self.centralwidget)
        self.slide_bar.setEnabled(True)
        self.slide_bar.setGeometry(QtCore.QRect(90, 370, 700, 20))
        self.slide_bar.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.slide_bar.setMouseTracking(False)
        self.slide_bar.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slide_bar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.slide_bar.setAcceptDrops(False)
        self.slide_bar.setMaximum(100)
        self.slide_bar.setSingleStep(5)
        self.slide_bar.setPageStep(5)
        self.slide_bar.setProperty("value", 0)
        self.slide_bar.setSliderPosition(0)
        self.slide_bar.setTracking(True)
        self.slide_bar.setOrientation(QtCore.Qt.Horizontal)
        self.slide_bar.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slide_bar.setTickInterval(10)
        self.slide_bar.setObjectName("slide_bar")
        self.label_alpha = QtWidgets.QLabel(self.centralwidget)
        self.label_alpha.setGeometry(QtCore.QRect(40, 370, 40, 20))
        self.label_alpha.setObjectName("label_alpha")
        self.label_left = QtWidgets.QLabel(self.centralwidget)
        self.label_left.setGeometry(QtCore.QRect(90, 390, 20, 20))
        self.label_left.setObjectName("label_left")
        self.label_right = QtWidgets.QLabel(self.centralwidget)
        self.label_right.setGeometry(QtCore.QRect(760, 390, 20, 20))
        self.label_right.setObjectName("label_right")
        self.edit_alpha = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_alpha.setGeometry(QtCore.QRect(790, 370, 60, 20))
        self.edit_alpha.setObjectName("edit_alpha")
        self.box_result = QtWidgets.QGraphicsView(self.centralwidget)
        self.box_result.setGeometry(QtCore.QRect(260, 420, 360, 270))
        self.box_result.setObjectName("box_result")
        self.label_blend = QtWidgets.QLabel(self.centralwidget)
        self.label_blend.setGeometry(QtCore.QRect(360, 700, 160, 30))
        self.label_blend.setObjectName("label_blend")
        self.btn_blend = QtWidgets.QPushButton(self.centralwidget)
        self.btn_blend.setGeometry(QtCore.QRect(360, 750, 160, 30))
        self.btn_blend.setObjectName("btn_blend")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_start.setText(_translate("MainWindow", "Load Starting Image ..."))
        self.btn_end.setText(_translate("MainWindow", "Load Ending Image ..."))
        self.Starting_Text.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Starting Image</span></p></body></html>"))
        self.Ending_Text.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Ending Image</span></p></body></html>"))
        self.check_triangles.setText(_translate("MainWindow", "Show Triangles"))
        self.label_alpha.setText(_translate("MainWindow", "Alpha"))
        self.label_left.setText(_translate("MainWindow", "0.0"))
        self.label_right.setText(_translate("MainWindow", "1.0"))
        self.label_blend.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Blending Result</span></p></body></html>"))
        self.btn_blend.setText(_translate("MainWindow", "Blend"))


