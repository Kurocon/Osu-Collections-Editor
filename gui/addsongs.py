# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addsongs.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddSongs(object):
    def setupUi(self, AddSongs):
        AddSongs.setObjectName("AddSongs")
        AddSongs.resize(1004, 483)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/oce.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AddSongs.setWindowIcon(icon)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(AddSongs)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.global_layout = QtWidgets.QVBoxLayout()
        self.global_layout.setObjectName("global_layout")
        self.inner_layout = QtWidgets.QHBoxLayout()
        self.inner_layout.setObjectName("inner_layout")
        self.allsongs_groupbox = QtWidgets.QGroupBox(AddSongs)
        self.allsongs_groupbox.setObjectName("allsongs_groupbox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.allsongs_groupbox)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.allsongs_scrollarea = QtWidgets.QScrollArea(self.allsongs_groupbox)
        self.allsongs_scrollarea.setWidgetResizable(True)
        self.allsongs_scrollarea.setObjectName("allsongs_scrollarea")
        self.allsongs_scrollarea_contents = QtWidgets.QWidget()
        self.allsongs_scrollarea_contents.setGeometry(QtCore.QRect(0, 0, 441, 364))
        self.allsongs_scrollarea_contents.setObjectName("allsongs_scrollarea_contents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.allsongs_scrollarea_contents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.allsongs_list = QtWidgets.QTreeWidget(self.allsongs_scrollarea_contents)
        self.allsongs_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.allsongs_list.setObjectName("allsongs_list")
        self.allsongs_list.headerItem().setText(0, "1")
        self.allsongs_list.header().setVisible(False)
        self.verticalLayout_3.addWidget(self.allsongs_list)
        self.allsongs_scrollarea.setWidget(self.allsongs_scrollarea_contents)
        self.verticalLayout.addWidget(self.allsongs_scrollarea)
        self.allsongs_search_layout = QtWidgets.QHBoxLayout()
        self.allsongs_search_layout.setObjectName("allsongs_search_layout")
        self.allsongs_search_label = QtWidgets.QLabel(self.allsongs_groupbox)
        self.allsongs_search_label.setObjectName("allsongs_search_label")
        self.allsongs_search_layout.addWidget(self.allsongs_search_label)
        self.allsongs_search_field = QtWidgets.QLineEdit(self.allsongs_groupbox)
        self.allsongs_search_field.setObjectName("allsongs_search_field")
        self.allsongs_search_layout.addWidget(self.allsongs_search_field)
        self.verticalLayout.addLayout(self.allsongs_search_layout)
        self.inner_layout.addWidget(self.allsongs_groupbox)
        self.button_layout = QtWidgets.QVBoxLayout()
        self.button_layout.setObjectName("button_layout")
        self.add_mapset_button = QtWidgets.QToolButton(AddSongs)
        self.add_mapset_button.setEnabled(False)
        self.add_mapset_button.setStatusTip("")
        self.add_mapset_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/add_mapset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_mapset_button.setIcon(icon1)
        self.add_mapset_button.setObjectName("add_mapset_button")
        self.button_layout.addWidget(self.add_mapset_button)
        self.add_beatmap_button = QtWidgets.QToolButton(AddSongs)
        self.add_beatmap_button.setEnabled(False)
        self.add_beatmap_button.setStatusTip("")
        self.add_beatmap_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/add_map.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_beatmap_button.setIcon(icon2)
        self.add_beatmap_button.setObjectName("add_beatmap_button")
        self.button_layout.addWidget(self.add_beatmap_button)
        self.remove_beatmap_button = QtWidgets.QToolButton(AddSongs)
        self.remove_beatmap_button.setEnabled(False)
        self.remove_beatmap_button.setStatusTip("")
        self.remove_beatmap_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/remove_map.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.remove_beatmap_button.setIcon(icon3)
        self.remove_beatmap_button.setObjectName("remove_beatmap_button")
        self.button_layout.addWidget(self.remove_beatmap_button)
        self.remove_mapset_button = QtWidgets.QToolButton(AddSongs)
        self.remove_mapset_button.setEnabled(False)
        self.remove_mapset_button.setStatusTip("")
        self.remove_mapset_button.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/remove_mapset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.remove_mapset_button.setIcon(icon4)
        self.remove_mapset_button.setObjectName("remove_mapset_button")
        self.button_layout.addWidget(self.remove_mapset_button)
        self.inner_layout.addLayout(self.button_layout)
        self.addsongs_groupbox = QtWidgets.QGroupBox(AddSongs)
        self.addsongs_groupbox.setObjectName("addsongs_groupbox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.addsongs_groupbox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.addsongs_scrollarea = QtWidgets.QScrollArea(self.addsongs_groupbox)
        self.addsongs_scrollarea.setWidgetResizable(True)
        self.addsongs_scrollarea.setObjectName("addsongs_scrollarea")
        self.addsongs_scrollarea_contents = QtWidgets.QWidget()
        self.addsongs_scrollarea_contents.setGeometry(QtCore.QRect(0, 0, 441, 391))
        self.addsongs_scrollarea_contents.setObjectName("addsongs_scrollarea_contents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.addsongs_scrollarea_contents)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.addsongs_list = QtWidgets.QTreeWidget(self.addsongs_scrollarea_contents)
        self.addsongs_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.addsongs_list.setObjectName("addsongs_list")
        self.addsongs_list.headerItem().setText(0, "1")
        self.addsongs_list.header().setVisible(False)
        self.verticalLayout_5.addWidget(self.addsongs_list)
        self.addsongs_scrollarea.setWidget(self.addsongs_scrollarea_contents)
        self.verticalLayout_4.addWidget(self.addsongs_scrollarea)
        self.inner_layout.addWidget(self.addsongs_groupbox)
        self.global_layout.addLayout(self.inner_layout)
        self.confirmation_buttons = QtWidgets.QDialogButtonBox(AddSongs)
        self.confirmation_buttons.setOrientation(QtCore.Qt.Horizontal)
        self.confirmation_buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirmation_buttons.setObjectName("confirmation_buttons")
        self.global_layout.addWidget(self.confirmation_buttons)
        self.verticalLayout_6.addLayout(self.global_layout)

        self.retranslateUi(AddSongs)
        self.confirmation_buttons.accepted.connect(AddSongs.accept)
        self.confirmation_buttons.rejected.connect(AddSongs.reject)
        QtCore.QMetaObject.connectSlotsByName(AddSongs)

    def retranslateUi(self, AddSongs):
        _translate = QtCore.QCoreApplication.translate
        AddSongs.setWindowTitle(_translate("AddSongs", "Add songs to collection"))
        self.allsongs_groupbox.setTitle(_translate("AddSongs", "All songs in your songs folder"))
        self.allsongs_search_label.setText(_translate("AddSongs", "Search"))
        self.add_mapset_button.setToolTip(_translate("AddSongs", "Add all maps in the mapset of selected map."))
        self.add_beatmap_button.setToolTip(_translate("AddSongs", "Add selected beatmap or mapset."))
        self.remove_beatmap_button.setToolTip(_translate("AddSongs", "Remove selected beatmap or mapset."))
        self.remove_mapset_button.setToolTip(_translate("AddSongs", "Remove all maps in the mapset of selected map."))
        self.addsongs_groupbox.setTitle(_translate("AddSongs", "Songs to add to collection"))

