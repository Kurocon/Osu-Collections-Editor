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
        LoadDialog.resize(646, 244)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/oce.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoadDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoadDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.container = QtWidgets.QVBoxLayout()
        self.container.setObjectName("container")
        self.help_label = QtWidgets.QLabel(LoadDialog)
        self.help_label.setObjectName("help_label")
        self.container.addWidget(self.help_label)
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setHorizontalSpacing(6)
        self.form_layout.setVerticalSpacing(0)
        self.form_layout.setObjectName("form_layout")
        self.loadfrom_label = QtWidgets.QLabel(LoadDialog)
        self.loadfrom_label.setObjectName("loadfrom_label")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.loadfrom_label)
        self.loadfrom_dropdown = QtWidgets.QComboBox(LoadDialog)
        self.loadfrom_dropdown.setObjectName("loadfrom_dropdown")
        self.loadfrom_dropdown.addItem("")
        self.loadfrom_dropdown.addItem("")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.loadfrom_dropdown)
        self.osudb_label = QtWidgets.QLabel(LoadDialog)
        self.osudb_label.setObjectName("osudb_label")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.osudb_label)
        self.osudb_fields = QtWidgets.QHBoxLayout()
        self.osudb_fields.setSpacing(0)
        self.osudb_fields.setObjectName("osudb_fields")
        self.osudb_edit = QtWidgets.QLineEdit(LoadDialog)
        self.osudb_edit.setObjectName("osudb_edit")
        self.osudb_fields.addWidget(self.osudb_edit)
        self.osudb_button = QtWidgets.QPushButton(LoadDialog)
        self.osudb_button.setObjectName("osudb_button")
        self.osudb_fields.addWidget(self.osudb_button)
        self.form_layout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.osudb_fields)
        self.songsfolder_label = QtWidgets.QLabel(LoadDialog)
        self.songsfolder_label.setObjectName("songsfolder_label")
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.songsfolder_label)
        self.songfolder_fields = QtWidgets.QHBoxLayout()
        self.songfolder_fields.setSpacing(0)
        self.songfolder_fields.setObjectName("songfolder_fields")
        self.songfolder_edit = QtWidgets.QLineEdit(LoadDialog)
        self.songfolder_edit.setObjectName("songfolder_edit")
        self.songfolder_fields.addWidget(self.songfolder_edit)
        self.songfolder_button = QtWidgets.QPushButton(LoadDialog)
        self.songfolder_button.setObjectName("songfolder_button")
        self.songfolder_fields.addWidget(self.songfolder_button)
        self.form_layout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.songfolder_fields)
        self.collectiondb_label = QtWidgets.QLabel(LoadDialog)
        self.collectiondb_label.setObjectName("collectiondb_label")
        self.form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.collectiondb_label)
        self.collectiondb_fields = QtWidgets.QHBoxLayout()
        self.collectiondb_fields.setSpacing(0)
        self.collectiondb_fields.setObjectName("collectiondb_fields")
        self.collectiondb_edit = QtWidgets.QLineEdit(LoadDialog)
        self.collectiondb_edit.setObjectName("collectiondb_edit")
        self.collectiondb_fields.addWidget(self.collectiondb_edit)
        self.collectiondb_button = QtWidgets.QPushButton(LoadDialog)
        self.collectiondb_button.setObjectName("collectiondb_button")
        self.collectiondb_fields.addWidget(self.collectiondb_button)
        self.form_layout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.collectiondb_fields)
        self.container.addLayout(self.form_layout)
        self.verticalLayout.addLayout(self.container)
        self.button_box = QtWidgets.QDialogButtonBox(LoadDialog)
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
        self.help_label.setText(_translate("LoadDialog", "Osu Collections Editor can load your songs from two different places. You can load from the\n"
"osu!.db file which osu! itself also uses, or you can load directly from your Songs folder.\n"
"\n"
"Loading from the osu! database will be much faster, but loading directly from your Songs folder \n"
"can be handy if you do not have an osu!.db at the ready."))
        self.loadfrom_label.setText(_translate("LoadDialog", "Load from"))
        self.loadfrom_dropdown.setItemText(0, _translate("LoadDialog", "osu!.db file"))
        self.loadfrom_dropdown.setItemText(1, _translate("LoadDialog", "Songs folder"))
        self.osudb_label.setText(_translate("LoadDialog", "osu!.db"))
        self.osudb_button.setText(_translate("LoadDialog", "Browse"))
        self.songsfolder_label.setText(_translate("LoadDialog", "Songs folder"))
        self.songfolder_button.setText(_translate("LoadDialog", "Browse"))
        self.collectiondb_label.setText(_translate("LoadDialog", "collection.db"))
        self.collectiondb_button.setText(_translate("LoadDialog", "Browse"))

