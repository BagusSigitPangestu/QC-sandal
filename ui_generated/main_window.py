# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialogButtonBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1356, 720)
        MainWindow.setMaximumSize(QSize(1356, 720))
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"background-color: rgb(74, 92, 106);\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color : rgb(74, 92, 106);")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.countainer = QWidget(self.centralwidget)
        self.countainer.setObjectName(u"countainer")
        self.horizontalLayout_2 = QHBoxLayout(self.countainer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_1 = QFrame(self.countainer)
        self.frame_1.setObjectName(u"frame_1")
        self.frame_1.setEnabled(True)
        self.frame_1.setMinimumSize(QSize(0, 0))
        self.frame_1.setMaximumSize(QSize(300, 16777215))
        self.frame_1.setStyleSheet(u"QFrame{\n"
"background-color: #11212D;\n"
"border-radius: 10px;\n"
"}\n"
"QGroupBox{\n"
"background-color: #253745;\n"
"border-radius: 10px;\n"
"}")
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.DetectionMode = QGroupBox(self.frame_1)
        self.DetectionMode.setObjectName(u"DetectionMode")
        self.DetectionMode.setMinimumSize(QSize(0, 250))
        self.DetectionMode.setMaximumSize(QSize(300, 250))
        self.DetectionMode.setStyleSheet(u"color : rgb(255, 255, 255);")
        self.gridLayout = QGridLayout(self.DetectionMode)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_7 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.gridLayout.addItem(self.verticalSpacer_7, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(self.DetectionMode)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(300, 250))
        self.tabWidget.setStyleSheet(u"QPushButton {\n"
"background-color: #9BA8AB;\n"
"border-radius: 5px;\n"
"color : #06141B;\n"
"}\n"
"QTabWidget{\n"
"border-radius: 10px;\n"
"}\n"
"")
        self.photoTab = QWidget()
        self.photoTab.setObjectName(u"photoTab")
        self.verticalLayout_7 = QVBoxLayout(self.photoTab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.loadImage = QPushButton(self.photoTab)
        self.loadImage.setObjectName(u"loadImage")
        self.loadImage.setMinimumSize(QSize(0, 50))

        self.verticalLayout_7.addWidget(self.loadImage)

        self.detectImage = QPushButton(self.photoTab)
        self.detectImage.setObjectName(u"detectImage")
        self.detectImage.setMinimumSize(QSize(0, 50))

        self.verticalLayout_7.addWidget(self.detectImage)

        self.verticalSpacer_2 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.photoTab, "")
        self.detectImage.raise_()
        self.loadImage.raise_()
        self.liveTab = QWidget()
        self.liveTab.setObjectName(u"liveTab")
        self.gridLayout_9 = QGridLayout(self.liveTab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.captureFrame = QPushButton(self.liveTab)
        self.captureFrame.setObjectName(u"captureFrame")
        self.captureFrame.setMinimumSize(QSize(0, 30))

        self.gridLayout_9.addWidget(self.captureFrame, 2, 1, 1, 2)

        self.cameraSettings = QGroupBox(self.liveTab)
        self.cameraSettings.setObjectName(u"cameraSettings")
        self.cameraSettings.setMaximumSize(QSize(16777215, 100))
        self.cameraSettings.setStyleSheet(u"QWidget{\n"
"color : #06141B;\n"
"background-color: #CCD0CF;\n"
"}")
        self.gridLayout_10 = QGridLayout(self.cameraSettings)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.widget_4 = QWidget(self.cameraSettings)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_9 = QVBoxLayout(self.widget_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.cameraID = QLabel(self.widget_4)
        self.cameraID.setObjectName(u"cameraID")

        self.verticalLayout_9.addWidget(self.cameraID)

        self.autoDetect = QLabel(self.widget_4)
        self.autoDetect.setObjectName(u"autoDetect")

        self.verticalLayout_9.addWidget(self.autoDetect)


        self.gridLayout_10.addWidget(self.widget_4, 1, 0, 1, 1)

        self.widget_5 = QWidget(self.cameraSettings)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_10 = QVBoxLayout(self.widget_5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.boxID = QSpinBox(self.widget_5)
        self.boxID.setObjectName(u"boxID")
        self.boxID.setValue(2)

        self.verticalLayout_10.addWidget(self.boxID)

        self.checkBox = QCheckBox(self.widget_5)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setAutoFillBackground(False)
        self.checkBox.setChecked(True)
        self.checkBox.setTristate(False)

        self.verticalLayout_10.addWidget(self.checkBox)


        self.gridLayout_10.addWidget(self.widget_5, 1, 1, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_6, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.cameraSettings, 3, 1, 1, 2)

        self.stopCamera = QPushButton(self.liveTab)
        self.stopCamera.setObjectName(u"stopCamera")
        self.stopCamera.setMinimumSize(QSize(0, 30))

        self.gridLayout_9.addWidget(self.stopCamera, 0, 2, 1, 1)

        self.startCamera = QPushButton(self.liveTab)
        self.startCamera.setObjectName(u"startCamera")
        self.startCamera.setMinimumSize(QSize(0, 30))

        self.gridLayout_9.addWidget(self.startCamera, 0, 1, 1, 1)

        self.tabWidget.addTab(self.liveTab, "")

        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_8, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.DetectionMode)

        self.groupBox_2 = QGroupBox(self.frame_1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 300))
        self.groupBox_2.setMaximumSize(QSize(16777215, 300))
        self.groupBox_2.setStyleSheet(u"QGroupBox{\n"
"color : rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"}\n"
"QWidget{\n"
"border-radius: 10px;\n"
"}\n"
"QLineEdit {\n"
"background-color: #CCD0CF;\n"
"color : rgb(0, 0, 0);\n"
"}\n"
"QLabel{\n"
"background-color : rgb(74, 92, 106);\n"
"color:rgb(255, 255, 255);\n"
"font-size: 14px;\n"
"}\n"
"\n"
"QPushButton {\n"
"background-color: #9BA8AB;\n"
"color: rgb(0, 0, 0);\n"
"}\n"
"QComboBox{\n"
"background-color: #9BA8AB;\n"
"color: rgb(0, 0, 0);\n"
"}\n"
"")
        self.gridLayout_7 = QGridLayout(self.groupBox_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.widget_7 = QWidget(self.groupBox_2)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMaximumSize(QSize(16777215, 50))
        self.widget_7.setStyleSheet(u"")
        self.gridLayout_8 = QGridLayout(self.widget_7)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.boxTipe = QComboBox(self.widget_7)
        self.boxTipe.setObjectName(u"boxTipe")
        self.boxTipe.setEditable(True)

        self.gridLayout_8.addWidget(self.boxTipe, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.widget_7, 2, 0, 1, 3)

        self.widget_2 = QWidget(self.groupBox_2)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"QLineEdit {\n"
"background-color: #CCD0CF;\n"
"border-radius: 10px;\n"
"}\n"
"")
        self.verticalLayout_4 = QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.labelMin = QLabel(self.widget_2)
        self.labelMin.setObjectName(u"labelMin")
        self.labelMin.setMaximumSize(QSize(16777215, 10))
        self.labelMin.setStyleSheet(u"font-size:13px;")
        self.labelMin.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.labelMin)

        self.min1 = QLineEdit(self.widget_2)
        self.min1.setObjectName(u"min1")

        self.verticalLayout_4.addWidget(self.min1)

        self.min2 = QLineEdit(self.widget_2)
        self.min2.setObjectName(u"min2")

        self.verticalLayout_4.addWidget(self.min2)

        self.min3 = QLineEdit(self.widget_2)
        self.min3.setObjectName(u"min3")

        self.verticalLayout_4.addWidget(self.min3)

        self.min4 = QLineEdit(self.widget_2)
        self.min4.setObjectName(u"min4")

        self.verticalLayout_4.addWidget(self.min4)

        self.min5 = QLineEdit(self.widget_2)
        self.min5.setObjectName(u"min5")

        self.verticalLayout_4.addWidget(self.min5)

        self.min6 = QLineEdit(self.widget_2)
        self.min6.setObjectName(u"min6")

        self.verticalLayout_4.addWidget(self.min6)

        self.min7 = QLineEdit(self.widget_2)
        self.min7.setObjectName(u"min7")

        self.verticalLayout_4.addWidget(self.min7)


        self.gridLayout_7.addWidget(self.widget_2, 1, 1, 1, 1)

        self.widget = QWidget(self.groupBox_2)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 23))
        self.widget.setStyleSheet(u"QRadioButton {\n"
"    color: rgb(255, 255, 255);\n"
"    font-size: 14px;\n"
"    spacing: 8px;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"    border: 2px solid #95a5a6;\n"
"    background-color: #ecf0f1;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    border: 2px solid #e67e22;\n"
"    background-color: #e67e22;\n"
"}\n"
"QWidget{\n"
"rgb(255, 255, 255)\n"
"border-radius: 10px;\n"
"}\n"
"")
        self.gridLayout_11 = QGridLayout(self.widget)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.verticalSpacer = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.gridLayout_11.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.btn3 = QRadioButton(self.widget)
        self.btn3.setObjectName(u"btn3")

        self.gridLayout_11.addWidget(self.btn3, 3, 0, 1, 1)

        self.btn2 = QRadioButton(self.widget)
        self.btn2.setObjectName(u"btn2")

        self.gridLayout_11.addWidget(self.btn2, 2, 0, 1, 1)

        self.btn4 = QRadioButton(self.widget)
        self.btn4.setObjectName(u"btn4")

        self.gridLayout_11.addWidget(self.btn4, 4, 0, 1, 1)

        self.btn5 = QRadioButton(self.widget)
        self.btn5.setObjectName(u"btn5")

        self.gridLayout_11.addWidget(self.btn5, 5, 0, 1, 1)

        self.btn1 = QRadioButton(self.widget)
        self.btn1.setObjectName(u"btn1")

        self.gridLayout_11.addWidget(self.btn1, 1, 0, 1, 1)

        self.btn6 = QRadioButton(self.widget)
        self.btn6.setObjectName(u"btn6")

        self.gridLayout_11.addWidget(self.btn6, 6, 0, 1, 1)

        self.btn7 = QRadioButton(self.widget)
        self.btn7.setObjectName(u"btn7")

        self.gridLayout_11.addWidget(self.btn7, 7, 0, 1, 1)

        self.labelSize1 = QLabel(self.widget)
        self.labelSize1.setObjectName(u"labelSize1")

        self.gridLayout_11.addWidget(self.labelSize1, 1, 1, 1, 1)

        self.labelSize2 = QLabel(self.widget)
        self.labelSize2.setObjectName(u"labelSize2")

        self.gridLayout_11.addWidget(self.labelSize2, 2, 1, 1, 1)

        self.labelSize3 = QLabel(self.widget)
        self.labelSize3.setObjectName(u"labelSize3")

        self.gridLayout_11.addWidget(self.labelSize3, 3, 1, 1, 1)

        self.labelSize4 = QLabel(self.widget)
        self.labelSize4.setObjectName(u"labelSize4")

        self.gridLayout_11.addWidget(self.labelSize4, 4, 1, 1, 1)

        self.labelSize5 = QLabel(self.widget)
        self.labelSize5.setObjectName(u"labelSize5")

        self.gridLayout_11.addWidget(self.labelSize5, 5, 1, 1, 1)

        self.labelSize6 = QLabel(self.widget)
        self.labelSize6.setObjectName(u"labelSize6")

        self.gridLayout_11.addWidget(self.labelSize6, 6, 1, 1, 1)

        self.labelSize7 = QLabel(self.widget)
        self.labelSize7.setObjectName(u"labelSize7")

        self.gridLayout_11.addWidget(self.labelSize7, 7, 1, 1, 1)


        self.gridLayout_7.addWidget(self.widget, 1, 0, 1, 1)

        self.widget_3 = QWidget(self.groupBox_2)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setStyleSheet(u"border-radius: 10px;")
        self.verticalLayout_5 = QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.labelMax = QLabel(self.widget_3)
        self.labelMax.setObjectName(u"labelMax")
        self.labelMax.setMaximumSize(QSize(16777215, 10))
        self.labelMax.setStyleSheet(u"font-size:13px;\n"
"")
        self.labelMax.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.labelMax)

        self.max1 = QLineEdit(self.widget_3)
        self.max1.setObjectName(u"max1")

        self.verticalLayout_5.addWidget(self.max1)

        self.max2 = QLineEdit(self.widget_3)
        self.max2.setObjectName(u"max2")

        self.verticalLayout_5.addWidget(self.max2)

        self.max3 = QLineEdit(self.widget_3)
        self.max3.setObjectName(u"max3")

        self.verticalLayout_5.addWidget(self.max3)

        self.max4 = QLineEdit(self.widget_3)
        self.max4.setObjectName(u"max4")

        self.verticalLayout_5.addWidget(self.max4)

        self.max5 = QLineEdit(self.widget_3)
        self.max5.setObjectName(u"max5")

        self.verticalLayout_5.addWidget(self.max5)

        self.max6 = QLineEdit(self.widget_3)
        self.max6.setObjectName(u"max6")

        self.verticalLayout_5.addWidget(self.max6)

        self.max7 = QLineEdit(self.widget_3)
        self.max7.setObjectName(u"max7")

        self.verticalLayout_5.addWidget(self.max7)

        self.labelMax.raise_()
        self.max1.raise_()
        self.max2.raise_()
        self.max3.raise_()
        self.max5.raise_()
        self.max6.raise_()
        self.max7.raise_()
        self.max4.raise_()

        self.gridLayout_7.addWidget(self.widget_3, 1, 2, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.gridLayout_7.addItem(self.verticalSpacer_5, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupExport = QGroupBox(self.frame_1)
        self.groupExport.setObjectName(u"groupExport")
        self.groupExport.setEnabled(True)
        self.groupExport.setMaximumSize(QSize(16777215, 100))
        self.groupExport.setBaseSize(QSize(0, 0))
        self.groupExport.setStyleSheet(u"QGroupBox{\n"
"color: #FFFFFF;\n"
"}\n"
"QPushButton {\n"
"background-color: #9BA8AB;\n"
"color: rgb(0, 0, 0);\n"
"}\n"
"")
        self.verticalLayout_6 = QVBoxLayout(self.groupExport)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.saveImage = QPushButton(self.groupExport)
        self.saveImage.setObjectName(u"saveImage")
        self.saveImage.setMinimumSize(QSize(0, 30))
        self.saveImage.setStyleSheet(u"border-radius:5px;")

        self.verticalLayout_6.addWidget(self.saveImage)

        self.buttonBox = QDialogButtonBox(self.groupExport)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout_6.addWidget(self.buttonBox)


        self.verticalLayout.addWidget(self.groupExport)


        self.horizontalLayout_2.addWidget(self.frame_1)

        self.frame_2 = QFrame(self.countainer)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setEnabled(True)
        self.frame_2.setMinimumSize(QSize(810, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 700))
        self.frame_2.setStyleSheet(u"border-radius:10px;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.screenImage = QLabel(self.frame_2)
        self.screenImage.setObjectName(u"screenImage")
        self.screenImage.setStyleSheet(u"font-size: 20px;\n"
"color: rgb(255, 255, 255);")
        self.screenImage.setFrameShape(QFrame.NoFrame)
        self.screenImage.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.screenImage, 0, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.countainer)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 0))
        self.frame_3.setMaximumSize(QSize(200, 16777215))
        self.frame_3.setStyleSheet(u"QFrame{\n"
"background-color: #11212D;\n"
"border-radius: 10px;\n"
"}\n"
"QGroupBox{\n"
"color : rgb(255, 255, 255);\n"
"background-color: #253745;\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QLabel{\n"
"background-color : #253745;\n"
"color:rgb(255, 255, 255);\n"
"font-size: 14px;\n"
"}")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.detectionResult = QGroupBox(self.frame_3)
        self.detectionResult.setObjectName(u"detectionResult")
        self.detectionResult.setMinimumSize(QSize(0, 150))
        self.gridLayout_5 = QGridLayout(self.detectionResult)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.statusResult = QLabel(self.detectionResult)
        self.statusResult.setObjectName(u"statusResult")
        self.statusResult.setMaximumSize(QSize(16777215, 100))
        self.statusResult.setStyleSheet(u"background-color: [bgColor];\n"
"border-radius: 25px;\n"
"font-size: 70px;\n"
"color: rgb(0, 0, 0);")
        self.statusResult.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.statusResult, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.detectionResult)

        self.dimensions = QGroupBox(self.frame_3)
        self.dimensions.setObjectName(u"dimensions")
        self.dimensions.setMinimumSize(QSize(0, 150))
        self.dimensions.setStyleSheet(u"border-radius: 10px;")
        self.gridLayout_3 = QGridLayout(self.dimensions)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.widget_6 = QWidget(self.dimensions)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setMaximumSize(QSize(200, 100))
        self.widget_6.setStyleSheet(u"QLabel{\n"
"background-color: #CCD0CF;\n"
"color : #06141B;\n"
"}\n"
"QWidget{\n"
"background-color: #CCD0CF;\n"
"border-radius: 10px;\n"
"}")
        self.gridLayout_6 = QGridLayout(self.widget_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.labelLength = QLabel(self.widget_6)
        self.labelLength.setObjectName(u"labelLength")

        self.gridLayout_6.addWidget(self.labelLength, 0, 0, 1, 1)

        self.lengthValue = QLabel(self.widget_6)
        self.lengthValue.setObjectName(u"lengthValue")

        self.gridLayout_6.addWidget(self.lengthValue, 0, 1, 1, 1)

        self.labelWidth = QLabel(self.widget_6)
        self.labelWidth.setObjectName(u"labelWidth")

        self.gridLayout_6.addWidget(self.labelWidth, 1, 0, 1, 1)

        self.widthValue = QLabel(self.widget_6)
        self.widthValue.setObjectName(u"widthValue")

        self.gridLayout_6.addWidget(self.widthValue, 1, 1, 1, 1)


        self.gridLayout_3.addWidget(self.widget_6, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.dimensions)

        self.processingInfo = QGroupBox(self.frame_3)
        self.processingInfo.setObjectName(u"processingInfo")
        self.processingInfo.setMinimumSize(QSize(0, 200))
        self.gridLayout_4 = QGridLayout(self.processingInfo)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.perimeterValue = QLabel(self.processingInfo)
        self.perimeterValue.setObjectName(u"perimeterValue")

        self.gridLayout_4.addWidget(self.perimeterValue, 2, 1, 1, 1)

        self.ratioValue = QLabel(self.processingInfo)
        self.ratioValue.setObjectName(u"ratioValue")

        self.gridLayout_4.addWidget(self.ratioValue, 3, 1, 1, 1)

        self.labelRatio = QLabel(self.processingInfo)
        self.labelRatio.setObjectName(u"labelRatio")

        self.gridLayout_4.addWidget(self.labelRatio, 3, 0, 1, 1)

        self.labelPerimeter = QLabel(self.processingInfo)
        self.labelPerimeter.setObjectName(u"labelPerimeter")

        self.gridLayout_4.addWidget(self.labelPerimeter, 2, 0, 1, 1)

        self.labelArea = QLabel(self.processingInfo)
        self.labelArea.setObjectName(u"labelArea")

        self.gridLayout_4.addWidget(self.labelArea, 1, 0, 1, 1)

        self.areaValue = QLabel(self.processingInfo)
        self.areaValue.setObjectName(u"areaValue")

        self.gridLayout_4.addWidget(self.areaValue, 1, 1, 1, 1)

        self.markersValue = QLabel(self.processingInfo)
        self.markersValue.setObjectName(u"markersValue")

        self.gridLayout_4.addWidget(self.markersValue, 4, 1, 1, 1)

        self.labelMarkers = QLabel(self.processingInfo)
        self.labelMarkers.setObjectName(u"labelMarkers")

        self.gridLayout_4.addWidget(self.labelMarkers, 4, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 0, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 0, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.processingInfo)

        self.label_logo = QLabel(self.frame_3)
        self.label_logo.setObjectName(u"label_logo")
        self.label_logo.setMaximumSize(QSize(16777215, 100))
        self.label_logo.setPixmap(QPixmap(u"../assets/sandal_white.png"))
        self.label_logo.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.label_logo)

        self.label_IoT = QLabel(self.frame_3)
        self.label_IoT.setObjectName(u"label_IoT")
        self.label_IoT.setMaximumSize(QSize(16777215, 100))
        self.label_IoT.setStyleSheet(u"font-size: 11px;\n"
"font-weight: bold;")
        self.label_IoT.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_IoT)


        self.horizontalLayout_2.addWidget(self.frame_3)


        self.horizontalLayout.addWidget(self.countainer)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.tabWidget, self.loadImage)
        QWidget.setTabOrder(self.loadImage, self.detectImage)
        QWidget.setTabOrder(self.detectImage, self.captureFrame)
        QWidget.setTabOrder(self.captureFrame, self.boxID)
        QWidget.setTabOrder(self.boxID, self.checkBox)
        QWidget.setTabOrder(self.checkBox, self.stopCamera)
        QWidget.setTabOrder(self.stopCamera, self.startCamera)
        QWidget.setTabOrder(self.startCamera, self.boxTipe)
        QWidget.setTabOrder(self.boxTipe, self.min1)
        QWidget.setTabOrder(self.min1, self.min2)
        QWidget.setTabOrder(self.min2, self.min3)
        QWidget.setTabOrder(self.min3, self.min4)
        QWidget.setTabOrder(self.min4, self.min5)
        QWidget.setTabOrder(self.min5, self.min6)
        QWidget.setTabOrder(self.min6, self.min7)
        QWidget.setTabOrder(self.min7, self.btn3)
        QWidget.setTabOrder(self.btn3, self.btn2)
        QWidget.setTabOrder(self.btn2, self.btn4)
        QWidget.setTabOrder(self.btn4, self.btn5)
        QWidget.setTabOrder(self.btn5, self.btn1)
        QWidget.setTabOrder(self.btn1, self.btn6)
        QWidget.setTabOrder(self.btn6, self.btn7)
        QWidget.setTabOrder(self.btn7, self.max1)
        QWidget.setTabOrder(self.max1, self.max2)
        QWidget.setTabOrder(self.max2, self.max3)
        QWidget.setTabOrder(self.max3, self.max4)
        QWidget.setTabOrder(self.max4, self.max5)
        QWidget.setTabOrder(self.max5, self.max6)
        QWidget.setTabOrder(self.max6, self.max7)
        QWidget.setTabOrder(self.max7, self.saveImage)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sandal Dimension Detector v2.0", None))
        self.DetectionMode.setTitle(QCoreApplication.translate("MainWindow", u"Detection Mode", None))
        self.loadImage.setText(QCoreApplication.translate("MainWindow", u"Load Image", None))
        self.detectImage.setText(QCoreApplication.translate("MainWindow", u"Detect Image", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.photoTab), QCoreApplication.translate("MainWindow", u"PHOTO", None))
        self.captureFrame.setText(QCoreApplication.translate("MainWindow", u"Capture Frame", None))
        self.cameraSettings.setTitle(QCoreApplication.translate("MainWindow", u"Camera Settings", None))
        self.cameraID.setText(QCoreApplication.translate("MainWindow", u"Camera ID:", None))
        self.autoDetect.setText(QCoreApplication.translate("MainWindow", u"Auto Detect:", None))
        self.checkBox.setText("")
        self.stopCamera.setText(QCoreApplication.translate("MainWindow", u"Stop Camera", None))
        self.startCamera.setText(QCoreApplication.translate("MainWindow", u"Start Camera", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.liveTab), QCoreApplication.translate("MainWindow", u"LIVE", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Size input", None))
        self.labelMin.setText(QCoreApplication.translate("MainWindow", u"MIN (mm)", None))
        self.btn3.setText("")
        self.btn2.setText("")
        self.btn4.setText("")
        self.btn5.setText("")
        self.btn1.setText("")
        self.btn6.setText("")
        self.btn7.setText("")
        self.labelSize1.setText(QCoreApplication.translate("MainWindow", u"XS", None))
        self.labelSize2.setText(QCoreApplication.translate("MainWindow", u"S", None))
        self.labelSize3.setText(QCoreApplication.translate("MainWindow", u"M", None))
        self.labelSize4.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.labelSize5.setText(QCoreApplication.translate("MainWindow", u"XL", None))
        self.labelSize6.setText(QCoreApplication.translate("MainWindow", u"2XL", None))
        self.labelSize7.setText(QCoreApplication.translate("MainWindow", u"3XL", None))
        self.labelMax.setText(QCoreApplication.translate("MainWindow", u"MAX (mm)", None))
        self.groupExport.setTitle(QCoreApplication.translate("MainWindow", u"Size Settings", None))
        self.saveImage.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.screenImage.setText(QCoreApplication.translate("MainWindow", u"Load an image or start camera\n"
"to begin detection", None))
        self.detectionResult.setTitle(QCoreApplication.translate("MainWindow", u"Size Result", None))
        self.statusResult.setText("")
        self.dimensions.setTitle(QCoreApplication.translate("MainWindow", u"Dimensions", None))
        self.labelLength.setText(QCoreApplication.translate("MainWindow", u"Length :", None))
        self.lengthValue.setText("")
        self.labelWidth.setText(QCoreApplication.translate("MainWindow", u"Width :", None))
        self.widthValue.setText("")
        self.processingInfo.setTitle(QCoreApplication.translate("MainWindow", u"Processing Info", None))
        self.perimeterValue.setText("")
        self.ratioValue.setText("")
        self.labelRatio.setText(QCoreApplication.translate("MainWindow", u"Ratio :", None))
        self.labelPerimeter.setText(QCoreApplication.translate("MainWindow", u"Perimeter :", None))
        self.labelArea.setText(QCoreApplication.translate("MainWindow", u"Area :", None))
        self.areaValue.setText("")
        self.markersValue.setText("")
        self.labelMarkers.setText(QCoreApplication.translate("MainWindow", u"Markers :", None))
        self.label_logo.setText("")
        self.label_IoT.setText(QCoreApplication.translate("MainWindow", u"Created By IoT Engineering", None))
    # retranslateUi

