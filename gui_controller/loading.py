from logging.config import logging
from PyQt5 import QtWidgets, QtCore, QtGui
import gui.loading
import settings
import util.collections_parser as cp
import util.osu_parser as op

class Loading(QtWidgets.QDialog):
    progress = QtCore.pyqtSignal(int)
    current = QtCore.pyqtSignal(str)
    text = QtCore.pyqtSignal(str)
    done = QtCore.pyqtSignal()

    def __init__(self, collectionfile, songdir):
        super(Loading, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.loading.Ui_LoadingDialog()
        self.ui.setupUi(self)

        self.collections = None
        self.songs = None
        self.collection_file = collectionfile
        self.song_directory = songdir

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

    def exec_(self):
        w = LoadTask(self.collection_file, self.song_directory, self)
        w.moveToThread(self.thread)
        self.thread.started.connect(w.work)
        self.thread.start()
        super(Loading, self).exec_()

    def dismiss(self):
        self.hide()


class LoadTask(QtCore.QObject):
    def __init__(self, cf, sd, dialog):
        super(LoadTask, self).__init__()
        self.collection_file = cf
        self.song_directory = sd
        self.dialog = dialog
        self.settings = settings.Settings.get_instance()
        self.log = logging.getLogger(__name__)

    def work(self):
        # Load collections from file
        self.log.debug("Loading collections...")
        self.dialog.text.emit("Loading collections...")
        self.dialog.collections = cp.parse_collections_gui(self.collection_file, self.dialog)

        # Load songs from dir
        self.log.debug("Loading songs...")
        self.dialog.text.emit("Loading songs...")
        self.dialog.songs = op.load_songs_from_dir_gui(self.song_directory, self.dialog)

        # Notify we're done.
        self.dialog.done.emit()
