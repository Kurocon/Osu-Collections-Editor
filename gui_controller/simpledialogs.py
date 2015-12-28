from logging.config import logging
from PyQt5 import QtWidgets, QtCore

import gui.question
import gui.notification


class QuestionDialog(QtWidgets.QDialog):
    done = QtCore.pyqtSignal(bool)

    def __init__(self, title, question):
        super(QuestionDialog, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.question.Ui_QuestionDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.label.setText(question)
        self.result = False

    def accept(self):
        self.result = True
        self.done.emit(True)

    def reject(self):
        self.result = False
        self.done.emit(False)


class NotificationDialog(QtWidgets.QDialog):
    done = QtCore.pyqtSignal(bool)

    def __init__(self, title, notification):
        super(NotificationDialog, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.notification.Ui_NotificationDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.label.setText(notification)

    def accept(self):
        self.done.emit(True)

    def reject(self):
        self.done.emit(False)
