from logging.config import logging

from PyQt5 import QtWidgets
import gui.startup
import settings


class Startup(QtWidgets.QDialog):
    def __init__(self):
        super(Startup, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.startup.Ui_LoadDialog()
        self.ui.setupUi(self)

        # Get settings instance
        self.settings = settings.Settings.get_instance()

        # Set default songdir and collection file from settings
        self.ui.songdir_edit.setText(self.settings.get_setting("default_songs_dir"))
        self.ui.collectionfile_edit.setText(self.settings.get_setting("default_collection_file"))

        self.songdir = self.settings.get_setting("default_songs_dir")
        self.collectionfile = self.settings.get_setting("default_collection_file")

        # Setup handlers for buttons
        self.ui.songdir_button.clicked.connect(self.browse_osudir)
        self.ui.collectionfile_button.clicked.connect(self.browse_collectionfile)

    def browse_osudir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Pick your osu! Song folder", self.ui.songdir_edit.text())

        if directory:
            self.ui.songdir_edit.setText(directory)
            self.songdir = directory

        self.log.debug("New dir: {}".format(self.ui.songdir_edit.text()))

    def browse_collectionfile(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Pick your osu! collection.db file", self.ui.collectionfile_edit.text(), "Osu Collections (collection.db);;All files (*)")

        if file:
            self.ui.collectionfile_edit.setText(file[0])
            self.collectionfile = file[0]

        self.log.debug("New file: {}".format(self.ui.collectionfile_edit.text()))
