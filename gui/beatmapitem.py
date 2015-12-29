# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beatmapitem.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BeatmapItem(object):
    def setupUi(self, BeatmapItem):
        BeatmapItem.setObjectName("BeatmapItem")
        BeatmapItem.resize(232, 37)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/oce.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BeatmapItem.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(BeatmapItem)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.difficulty_label = QtWidgets.QLabel(BeatmapItem)
        self.difficulty_label.setObjectName("difficulty_label")
        self.horizontalLayout_2.addWidget(self.difficulty_label)
        self.star_label = QtWidgets.QLabel(BeatmapItem)
        self.star_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.star_label.setObjectName("star_label")
        self.horizontalLayout_2.addWidget(self.star_label)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name_label = QtWidgets.QLabel(BeatmapItem)
        self.name_label.setObjectName("name_label")
        self.horizontalLayout.addWidget(self.name_label)
        self.mapper_label = QtWidgets.QLabel(BeatmapItem)
        self.mapper_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mapper_label.setObjectName("mapper_label")
        self.horizontalLayout.addWidget(self.mapper_label)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.line = QtWidgets.QFrame(BeatmapItem)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        self.line.setPalette(palette)
        self.line.setAutoFillBackground(False)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.warning_label = QtWidgets.QLabel(BeatmapItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.warning_label.sizePolicy().hasHeightForWidth())
        self.warning_label.setSizePolicy(sizePolicy)
        self.warning_label.setMinimumSize(QtCore.QSize(32, 32))
        self.warning_label.setMaximumSize(QtCore.QSize(32, 32))
        self.warning_label.setText("")
        self.warning_label.setPixmap(QtGui.QPixmap("icons/internet.png"))
        self.warning_label.setAlignment(QtCore.Qt.AlignCenter)
        self.warning_label.setObjectName("warning_label")
        self.horizontalLayout_3.addWidget(self.warning_label)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 2, 1)

        self.retranslateUi(BeatmapItem)
        QtCore.QMetaObject.connectSlotsByName(BeatmapItem)

    def retranslateUi(self, BeatmapItem):
        _translate = QtCore.QCoreApplication.translate
        BeatmapItem.setWindowTitle(_translate("BeatmapItem", "BeatmapItem"))
        self.difficulty_label.setText(_translate("BeatmapItem", "Difficulty"))
        self.star_label.setText(_translate("BeatmapItem", "(AR?, CS?, HP?, OD?)"))
        self.name_label.setText(_translate("BeatmapItem", "Artist - Song"))
        self.mapper_label.setText(_translate("BeatmapItem", "(Mapper)"))
        self.warning_label.setStatusTip(_translate("BeatmapItem", "This song\'s details were loaded from the internet."))

