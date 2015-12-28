# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startup.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoadDialog(object):
    def setupUi(self, LoadDialog):
        LoadDialog.setObjectName("LoadDialog")
        LoadDialog.resize(599, 160)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/oce.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoadDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoadDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setObjectName("grid_layout")
        self.songdir_label = QtWidgets.QLabel(LoadDialog)
        self.songdir_label.setObjectName("songdir_label")
        self.grid_layout.addWidget(self.songdir_label, 1, 0, 1, 1)
        self.collection_label = QtWidgets.QLabel(LoadDialog)
        self.collection_label.setObjectName("collection_label")
        self.grid_layout.addWidget(self.collection_label, 2, 0, 1, 1)
        self.songdir_edit = QtWidgets.QLineEdit(LoadDialog)
        self.songdir_edit.setObjectName("songdir_edit")
        self.grid_layout.addWidget(self.songdir_edit, 1, 1, 1, 1)
        self.collectionfile_edit = QtWidgets.QLineEdit(LoadDialog)
        self.collectionfile_edit.setObjectName("collectionfile_edit")
        self.grid_layout.addWidget(self.collectionfile_edit, 2, 1, 1, 1)
        self.songdir_button = QtWidgets.QPushButton(LoadDialog)
        self.songdir_button.setStatusTip("")
        self.songdir_button.setObjectName("songdir_button")
        self.grid_layout.addWidget(self.songdir_button, 1, 2, 1, 1)
        self.collectionfile_button = QtWidgets.QPushButton(LoadDialog)
        self.collectionfile_button.setStatusTip("")
        self.collectionfile_button.setObjectName("collectionfile_button")
        self.grid_layout.addWidget(self.collectionfile_button, 2, 2, 1, 1)
        self.help_label = QtWidgets.QLabel(LoadDialog)
        self.help_label.setTextFormat(QtCore.Qt.PlainText)
        self.help_label.setScaledContents(False)
        self.help_label.setAlignment(QtCore.Qt.AlignCenter)
        self.help_label.setWordWrap(True)
        self.help_label.setObjectName("help_label")
        self.grid_layout.addWidget(self.help_label, 0, 0, 1, 3)
        self.verticalLayout.addLayout(self.grid_layout)
        self.button_box = QtWidgets.QDialogButtonBox(LoadDialog)
        self.button_box.setStatusTip("")
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(LoadDialog)
        self.button_box.accepted.connect(LoadDialog.accept)
        self.button_box.rejected.connect(LoadDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LoadDialog)

    def retranslateUi(self, LoadDialog):
        _translate = QtCore.QCoreApplication.translate
        LoadDialog.setWindowTitle(_translate("LoadDialog", "Open collection"))
        self.songdir_label.setText(_translate("LoadDialog", "Songs directory"))
        self.collection_label.setText(_translate("LoadDialog", "collection.db"))
        self.songdir_button.setText(_translate("LoadDialog", "Browse"))
        self.collectionfile_button.setText(_translate("LoadDialog", "Browse"))
        self.help_label.setText(_translate("LoadDialog", "Please locate your osu! Songs directory and the collection.db file you wish to edit."))

