from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(328, 225)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.new_profile = QtWidgets.QPushButton(self.centralwidget)
        self.new_profile.setGeometry(QtCore.QRect(30, 110, 271, 41))
        self.new_profile.setObjectName("new_profile")
        self.log_in_profile = QtWidgets.QPushButton(self.centralwidget)
        self.log_in_profile.setGeometry(QtCore.QRect(30, 40, 271, 41))
        self.log_in_profile.setObjectName("log_in_profile")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 328, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.new_profile.setText(_translate("MainWindow", "Регистрация"))
        self.log_in_profile.setText(_translate("MainWindow", "Вход"))
