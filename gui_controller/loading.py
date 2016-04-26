from logging.config import logging
from PyQt5 import QtWidgets, QtCore, QtGui
import gui.loading
import settings
import os
import util.collections_parser as cp
import util.osu_parser as op
import util.osudb_parser as odp


class Loading(QtWidgets.QDialog):
    progress = QtCore.pyqtSignal(int)
    current = QtCore.pyqtSignal(str)
    text = QtCore.pyqtSignal(str)
    done = QtCore.pyqtSignal()

    def __init__(self, collectionfile, songdb):
        super(Loading, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.loading.Ui_LoadingDialog()
        self.ui.setupUi(self)

        self.setModal(True)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)

        self.collections = None
        self.songs = None
        self.collection_file = collectionfile
        self.song_db = songdb
        self.db_is_directory = os.path.isdir(self.song_db)

        self.log.debug("Loading songdb {}{} and collectiondb {}".format(self.song_db, " (dir)" if self.db_is_directory else "", self.collection_file))

        self.progress.connect(self.update_precentage)
        self.current.connect(self.update_current)
        self.text.connect(self.update_text)
        self.done.connect(self.dismiss)

        self.ui.progressbar.setRange(0, 100)

        self.thread = QtCore.QThread()

    def keyPressEvent(self, event):
        if event.key() not in [QtCore.Qt.Key_Escape, QtCore.Qt.Key_Alt, QtCore.Qt.Key_AltGr, QtCore.Qt.Key_F4]:
            super(Loading, self).keyPressEvent(event)

    def update_precentage(self, percentage):
        self.ui.progressbar.setValue(percentage)
        QtWidgets.qApp.processEvents()

    def update_text(self, text):
        if len(text) > 33:
            text = text[:40] + "..."
        self.ui.loading_label.setText(text)

    def update_current(self, text):
        if len(text) > 33:
            text = text[:40] + "..."
        self.ui.loading_current_label.setText(text)

    def exec_(self):
        w = LoadTask(self.collection_file, self.song_db, self.db_is_directory, self)
        w.moveToThread(self.thread)
        self.thread.started.connect(w.work)
        self.thread.start()
        super(Loading, self).exec_()

    def dismiss(self):
        self.hide()


class LoadTask(QtCore.QObject):
    def __init__(self, cf, sd, sd_isdir, dialog):
        super(LoadTask, self).__init__()
        self.collection_file = cf
        self.song_db = sd
        self.db_is_directory = sd_isdir
        self.dialog = dialog
        self.settings = settings.Settings.get_instance()
        self.log = logging.getLogger(__name__)

    def work(self):
        # Load collections from file
        self.log.debug("Loading collections...")
        self.dialog.text.emit("Loading collections...")
        try:
            self.dialog.collections = cp.parse_collections_gui(self.collection_file, self.dialog)
        except Exception as e:
            self.log.error("Error while parsing collections.db: {}".format(e))
            import traceback
            traceback.print_exc()
            self.dialog.collections = None

        # Load songs from dir
        self.log.debug("Loading songs...")
        self.dialog.text.emit("Loading songs...")
        if self.db_is_directory:
            try:
                self.dialog.songs = op.load_songs_from_dir_gui(self.song_db, self.dialog)
            except Exception as e:
                self.log.error("Error while parsing Song folder: {}".format(e))
                import traceback
                traceback.print_exc()
                self.dialog.songs = None
        else:
            try:
                self.dialog.songs = odp.load_osudb_gui(self.song_db, self.dialog)
            except Exception as e:
                self.log.error("Error while parsing osu!.db: {}".format(e))
                import traceback
                traceback.print_exc()
                self.dialog.songs = None

        # Notify we're done.
        self.dialog.done.emit()
