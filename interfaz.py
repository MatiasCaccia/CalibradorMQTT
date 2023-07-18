from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Pantalla Principal
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 990, 590))
        self.groupBox.setObjectName("groupBox")

        # Sensor 1
        self.lcdPresion1 = QtWidgets.QLCDNumber(10, self.groupBox)
        self.lcdPresion1.setGeometry(QtCore.QRect(200, 20, 300, 41))
        self.lcdPresion1.setObjectName("lcdPresion1")
        self.lcdTemperatura1 = QtWidgets.QLCDNumber(10, self.groupBox)
        self.lcdTemperatura1.setGeometry(QtCore.QRect(200, 80, 300, 41))
        self.lcdTemperatura1.setObjectName("lcdPTemperatura1")
        '''
        self.lcdNumberCur = QtWidgets.QLCDNumber(self.groupBox)
        
        self.lcdNumberCur = QtWidgets.QLCDNumber(self.groupBox)
        '''
        
        # Sensor 2 presión
        self.lcdPresion2 = QtWidgets.QLCDNumber(10, self.groupBox)
        self.lcdPresion2.setGeometry(QtCore.QRect(200, 200, 300, 41))
        self.lcdPresion2.setObjectName("lcdPresion2")
        self.lcdTemperatura2 = QtWidgets.QLCDNumber(10, self.groupBox)
        self.lcdTemperatura2.setGeometry(QtCore.QRect(200, 260, 300, 41))
        self.lcdTemperatura2.setObjectName("lcdPTemperatura2")
        #self.lcdNumberCur2 = QtWidgets.QLCDNumber(self.groupBox)

        # Timestamp
        self.lcdTimestamp = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdTimestamp.setGeometry(QtCore.QRect(800, 310, 151, 41))
        self.lcdTimestamp.setObjectName("lcdTimestamp")

        # Texto a la izquierda del display
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 50, 150, 50))
        self.label.setObjectName("label")

        # Texto a la izquierda del display para Sensor 1
        self.labelPresion1 = QtWidgets.QLabel(self.groupBox)
        self.labelPresion1.setGeometry(QtCore.QRect(15, 10, 150, 50))
        self.labelPresion1.setObjectName("labelPresion1")
        self.labelTemperatura1 = QtWidgets.QLabel(self.groupBox)
        self.labelTemperatura1.setGeometry(QtCore.QRect(15, 75, 160, 50))
        self.labelTemperatura1.setObjectName("labelTemperatura1")

        # Texto a la izquierda del display para Sensor 2
        self.labelPresion2 = QtWidgets.QLabel(self.groupBox)
        self.labelPresion2.setGeometry(QtCore.QRect(15, 195, 150, 50))
        self.labelPresion2.setObjectName("labelPresion2")
        self.labelTemperatura2 = QtWidgets.QLabel(self.groupBox)
        self.labelTemperatura2.setGeometry(QtCore.QRect(15, 260, 160, 50))
        self.labelTemperatura2.setObjectName("labelTemperatura2")

        self.labelMin = QtWidgets.QLabel(self.groupBox)
        self.labelMin.setGeometry(QtCore.QRect(20, 95, 150, 50))
        self.labelMin.setObjectName("labelMin")
        
        # Boton de envio de sincronia
        self.pushButton = QtWidgets.QPushButton("pushButton", self.groupBox) 
        self.pushButton.setGeometry(QtCore.QRect(100, 500, 100, 50))
        self.pushButton.setObjectName("pushButton")

        # Boton de envio de STOP
        self.pushButton_stop = QtWidgets.QPushButton("pushButton_stop", self.groupBox) 
        self.pushButton_stop.setGeometry(QtCore.QRect(750, 500, 100, 50))
        self.pushButton_stop.setObjectName("pushButton_stop")

        # Entrada de texto para la presión de referencia
        self.ei = QtWidgets.QLineEdit(self.groupBox)
        self.ei.setGeometry(QtCore.QRect(600, 20, 300, 41))
        self.ei.setObjectName("ValorReferencia")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calibración BMP280"))
        #self.groupBox.setTitle(_translate("MainWindow", "Datos Tiempo Real"))
        self.labelPresion1.setText(_translate("MainWindow", "Presion Sensor 1 [Pa]"))
        self.labelTemperatura1.setText(_translate("MainWindow", "Temperatura Sensor 1 [°C]"))
        self.labelPresion2.setText(_translate("MainWindow", "Presion Sensor 2 [Pa]"))
        self.labelTemperatura2.setText(_translate("MainWindow", "Temperatura Sensor 2 [°C]"))
        self.pushButton.setText(_translate("MainWindow", "Comenzar"))
        self.pushButton_stop.setText(_translate("MainWindow", "STOP"))
        self.ei.setText(_translate("MainWundow", ""))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())