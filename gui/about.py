# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.setEnabled(True)
        AboutDialog.resize(427, 160)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/oce.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.app_title = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.app_title.setFont(font)
        self.app_title.setAlignment(QtCore.Qt.AlignCenter)
        self.app_title.setObjectName("app_title")
        self.verticalLayout.addWidget(self.app_title)
        self.license_text = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.license_text.setFont(font)
        self.license_text.setAlignment(QtCore.Qt.AlignCenter)
        self.license_text.setOpenExternalLinks(True)
        self.license_text.setObjectName("license_text")
        self.verticalLayout.addWidget(self.license_text)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem)
        self.developer_text = QtWidgets.QLabel(AboutDialog)
        self.developer_text.setAlignment(QtCore.Qt.AlignCenter)
        self.developer_text.setOpenExternalLinks(True)
        self.developer_text.setObjectName("developer_text")
        self.verticalLayout.addWidget(self.developer_text)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem1)
        self.version_text = QtWidgets.QLabel(AboutDialog)
        self.version_text.setObjectName("version_text")
        self.verticalLayout.addWidget(self.version_text)
        self.button_box = QtWidgets.QDialogButtonBox(AboutDialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(AboutDialog)
        self.button_box.accepted.connect(AboutDialog.accept)
        self.button_box.rejected.connect(AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About osu! Collection Editor"))
        self.app_title.setText(_translate("AboutDialog", "osu! Collection Editor"))
        self.license_text.setText(_translate("AboutDialog", "<p>Distributed under the <a href=\"http://www.gnu.org/licenses/gpl-3.0.en.html\"><span style=\" text-decoration: underline; color:#0000ff;\">GNU General Public License Version 3</span></a></p>"))
        self.developer_text.setText(_translate("AboutDialog", "<p>Created by <a href=\"http://www.kevinalberts.nl/\"><span style=\" text-decoration: underline; color:#0000ff;\">Kevin Alberts</span></a> (<a href=\"http://osu.ppy.sh/u/Kurocon\"><span style=\" text-decoration: underline; color:#0000ff;\">Kurocon</span></a>)<br />Source on <a href=\"http://github.com/Kurocon/Osu-Collections-Editor\"><span style=\" text-decoration: underline; color:#0000ff;\">GitLab</span></a></p>"))
        self.developer_text.setText(_translate("AboutDialog", "<p>Created by <a href=\"http://www.kevinalberts.nl/\"><span style=\" text-decoration: underline; color:#0000ff;\">Kevin Alberts</span></a> (<a href=\"http://osu.ppy.sh/u/Kurocon\"><span style=\" text-decoration: underline; color:#0000ff;\">Kurocon</span></a>)<br />Source on <a href=\"http://github.com/Kurocon/Osu-Collections-Editor\"><span style=\" text-decoration: underline; color:#0000ff;\">GitLab</span></a></p>"))
        self.version_text.setText(_translate("AboutDialog", "Version 0.1.dev1, Build 1"))

