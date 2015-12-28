# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notification.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NotificationDialog(object):
    def setupUi(self, NotificationDialog):
        NotificationDialog.setObjectName("NotificationDialog")
        NotificationDialog.resize(400, 100)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/oce.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NotificationDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(NotificationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(NotificationDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(NotificationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NotificationDialog)
        self.buttonBox.accepted.connect(NotificationDialog.accept)
        self.buttonBox.rejected.connect(NotificationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NotificationDialog)

    def retranslateUi(self, NotificationDialog):
        _translate = QtCore.QCoreApplication.translate
        NotificationDialog.setWindowTitle(_translate("NotificationDialog", "Notification"))
        self.label.setText(_translate("NotificationDialog", "Something happened."))

