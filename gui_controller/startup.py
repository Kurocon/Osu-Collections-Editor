import logging

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

        # Set default values from settings
        self.ui.loadfrom_dropdown.setCurrentIndex(self.settings.get_setting("default_loadfrom"))
        self.ui.osudb_edit.setText(self.settings.get_setting("default_osudb"))
        self.ui.songfolder_edit.setText(self.settings.get_setting("default_songs_folder"))
        self.ui.collectiondb_edit.setText(self.settings.get_setting("default_collectiondb"))

        self.loadfrom = self.settings.get_setting("default_loadfrom")
        self.osudb = self.settings.get_setting("default_osudb")
        self.songfolder = self.settings.get_setting("default_songs_folder")
        self.collectiondb = self.settings.get_setting("default_collectiondb")

        # Setup handlers for buttons
        self.ui.osudb_button.clicked.connect(self.browse_osudb)
        self.ui.songfolder_button.clicked.connect(self.browse_songfolder)
        self.ui.collectiondb_button.clicked.connect(self.browse_collectiondb)

        self.ui.osudb_edit.textChanged.connect(self.osudb_text_changed)
        self.ui.songfolder_edit.textChanged.connect(self.songfolder_text_changed)
        self.ui.collectiondb_edit.textChanged.connect(self.collectiondb_text_changed)

        # Connect on_dropdown_changed function to dropdown's currentIndexChanged signal
        self.ui.loadfrom_dropdown.currentIndexChanged.connect(self.on_dropdown_changed)

        # Hide unneeded UI elements based on dropdown value
        if self.ui.loadfrom_dropdown.currentIndex() == 0:
            # Hide songfolder selector
            self.ui.songsfolder_label.setVisible(False)
            self.ui.songfolder_edit.setVisible(False)
            self.ui.songfolder_button.setVisible(False)
        else:
            # Hide osudb selector
            self.ui.osudb_label.setVisible(False)
            self.ui.osudb_edit.setVisible(False)
            self.ui.osudb_button.setVisible(False)

    def on_dropdown_changed(self, index):
        self.loadfrom = index
        # Hide unneeded UI elements based on new dropdown value
        if index == 0:
            # Hide songfolder selector
            self.ui.songsfolder_label.setVisible(False)
            self.ui.songfolder_edit.setVisible(False)
            self.ui.songfolder_button.setVisible(False)
            # Show osudb selector
            self.ui.osudb_label.setVisible(True)
            self.ui.osudb_edit.setVisible(True)
            self.ui.osudb_button.setVisible(True)
        else:
            # Hide osudb selector
            self.ui.osudb_label.setVisible(False)
            self.ui.osudb_edit.setVisible(False)
            self.ui.osudb_button.setVisible(False)
            # Show songfolder selector
            self.ui.songsfolder_label.setVisible(True)
            self.ui.songfolder_edit.setVisible(True)
            self.ui.songfolder_button.setVisible(True)

    def osudb_text_changed(self, text):
        self.log.debug("New osudb: {}".format(text))
        self.osudb = text

    def songfolder_text_changed(self, text):
        self.log.debug("New songfolder: {}".format(text))
        self.songfolder = text

    def collectiondb_text_changed(self, text):
        self.log.debug("New collectiondb: {}".format(text))
        self.collectiondb = text

    def browse_osudb(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Pick your osu!.db file", self.ui.osudb_edit.text(), "osu!.db (osu!.db);;All files (*)")

        if file:
            self.ui.osudb_edit.setText(file[0])
            self.osudb = file[0]

        self.log.debug("New osudb: {}".format(self.ui.osudb_edit.text()))

    def browse_songfolder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Pick your osu! Song folder",
                                                               self.ui.songfolder_edit.text())

        if directory:
            self.ui.songfolder_edit.setText(directory)
            self.songfolder = directory

        self.log.debug("New songfolder: {}".format(self.ui.songfolder_edit.text()))

    def browse_collectiondb(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Pick your collection.db file", self.ui.collectiondb_edit.text(), "collection.db (collection.db);;All files (*)")

        if file:
            self.ui.collectiondb_edit.setText(file[0])
            self.collectiondb = file[0]

        self.log.debug("New collectiondb: {}".format(self.ui.collectiondb_edit.text()))
