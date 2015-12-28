# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoadingDialog(object):
    def setupUi(self, LoadingDialog):
        LoadingDialog.setObjectName("LoadingDialog")
        LoadingDialog.resize(424, 83)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/oce.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoadingDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoadingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.loading_label = QtWidgets.QLabel(LoadingDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.loading_label.setFont(font)
        self.loading_label.setObjectName("loading_label")
        self.verticalLayout.addWidget(self.loading_label)
        self.loading_current_label = QtWidgets.QLabel(LoadingDialog)
        self.loading_current_label.setObjectName("loading_current_label")
        self.verticalLayout.addWidget(self.loading_current_label)
        self.progressbar = QtWidgets.QProgressBar(LoadingDialog)
        self.progressbar.setProperty("value", 0)
        self.progressbar.setObjectName("progressbar")
        self.verticalLayout.addWidget(self.progressbar)

        self.retranslateUi(LoadingDialog)
        QtCore.QMetaObject.connectSlotsByName(LoadingDialog)

    def retranslateUi(self, LoadingDialog):
        _translate = QtCore.QCoreApplication.translate
        LoadingDialog.setWindowTitle(_translate("LoadingDialog", "Loading..."))
        self.loading_label.setText(_translate("LoadingDialog", "Loading loading dialog..."))
        self.loading_current_label.setText(_translate("LoadingDialog", "..."))

