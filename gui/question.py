# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'question.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QuestionDialog(object):
    def setupUi(self, QuestionDialog):
        QuestionDialog.setObjectName("QuestionDialog")
        QuestionDialog.resize(400, 100)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/oce.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QuestionDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(QuestionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(QuestionDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(QuestionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QuestionDialog)
        self.buttonBox.accepted.connect(QuestionDialog.accept)
        self.buttonBox.rejected.connect(QuestionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(QuestionDialog)

    def retranslateUi(self, QuestionDialog):
        _translate = QtCore.QCoreApplication.translate
        QuestionDialog.setWindowTitle(_translate("QuestionDialog", "Question"))
        self.label.setText(_translate("QuestionDialog", "Would you like to do something?"))

