from logging.config import logging
from PyQt5 import QtWidgets, QtCore, QtGui
import gui.loading
import settings
import util.collections_parser as cp
import util.osu_parser as op


class LoadingAddSong(QtWidgets.QDialog):
    progress = QtCore.pyqtSignal(int)
    current = QtCore.pyqtSignal(str)
    text = QtCore.pyqtSignal(str)
    done = QtCore.pyqtSignal()

    def __init__(self):
        super(LoadingAddSong, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.loading.Ui_LoadingDialog()
        self.ui.setupUi(self)

        self.setModal(True)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)

        self.progress.connect(self.update_precentage)
        self.current.connect(self.update_current)
        self.text.connect(self.update_text)
        self.done.connect(self.dismiss)

        self.ui.progressbar.setRange(0, 100)

        self.thread = QtCore.QThread()

    def update_precentage(self, percentage):
        self.ui.progressbar.setValue(percentage)
        QtWidgets.qApp.processEvents()

    def update_text(self, text):
        if len(text) > 33:
            text = text[:30] + "..."
        self.ui.loading_label.setText(text)

    def update_current(self, text):
        if len(text) > 33:
            text = text[:30] + "..."
        self.ui.loading_current_label.setText(text)

    def open(self):
        super(LoadingAddSong, self).open()

    def dismiss(self):
        self.hide()
