import threading
from logging.config import logging
import time
from PyQt5 import QtWidgets, QtCore
import gui.main
import settings
from gui_controller.loading import Loading
from gui_controller.startup import Startup

import util.song_collection_matcher as scm

class MainWindow(QtWidgets.QMainWindow):
    """
    Main application window

    :type log: Logger
    :type ui: Ui_MainWindow
    :type song_directory: str
    :type collection_file: str
    :type collections: util.collections_parser.Collections
    :type songs: util.osu_parser.Songs
    :type current_collection: util.collections_parser.Collection
    :type settings: settings.Settings
    """

    do_load = QtCore.pyqtSignal()
    do_match = QtCore.pyqtSignal()
    load_done = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.main.Ui_MainWindow()
        self.ui.setupUi(self)

        self.song_directory = ""
        self.collection_file = ""
        self.collections = None
        self.songs = None
        self.current_collection = None

        # Get settings instance
        self.settings = settings.Settings.get_instance()

        # Menu action handlers
        self.ui.action_open.triggered.connect(self.open)
        self.ui.action_exit.triggered.connect(self.close)
        self.ui.action_about.triggered.connect(self.about)

        # Button action handlers
        self.ui.add_collection_button.clicked.connect(self.add_collection)
        self.ui.remove_collection_button.clicked.connect(self.remove_collection)
        self.ui.options_collection_button.clicked.connect(self.options_collection)
        self.ui.up_collection_button.clicked.connect(self.up_collection)
        self.ui.down_collection_button.clicked.connect(self.down_collection)

        self.ui.songs_add_button.clicked.connect(self.add_song)
        self.ui.songs_remove_button.clicked.connect(self.remove_song)
        self.ui.songs_options_button.clicked.connect(self.options_song)
        self.ui.songs_up_button.clicked.connect(self.up_song)
        self.ui.songs_down_button.clicked.connect(self.down_song)

        # Setup list onclick handlers
        self.ui.collection_list.itemClicked.connect(self.collection_list_clicked)
        self.ui.songs_list.itemClicked.connect(self.songs_list_clicked)

        # Setup event handlers
        self.do_load.connect(self._do_load)
        self.do_match.connect(self._do_match)
        self.load_done.connect(self._load_done)

        # Show nothing loaded message in statusbar
        self.ui.statusbar.showMessage("Nothing loaded. Open something from the 'File' menu.")

    def open(self):
        u = Startup()
        if u.exec_():  # True if dialog is accepted
            self.song_directory = u.songdir
            self.collection_file = u.collectionfile
            self.do_load.emit()

    def _do_load(self):
        self.log.debug("Opening collection {}...".format(self.collection_file))

        # Create loading dialog
        l = Loading(self.collection_file, self.song_directory)
        l.exec_()

        # Get result from dialog
        self.log.debug("Dialog returned. Getting results")
        self.songs = l.songs
        self.collections = l.collections
        self.do_match.emit()

    def _do_match(self):
        # Match songs to collections
        cols, matched_c, unmatched_c, unmatched_m = scm.match_songs_to_collections(self.songs, self.collections)
        self.collections = cols

        # Notify if there are unmatched maps, to look them up online
        if unmatched_c != 0:
            self.log.debug("There are {} unmatched maps. Asking if they need to be looked up".format(unmatched_c))
            if self.settings.get_setting("osu_api_key"):
                search_online = False
                reply = QtWidgets.QMessageBox.question(self, 'Unmatched maps found',
                                           "{} beatmaps could not be matched. Would you like me to try to find their details using the osu! API?".format(unmatched_c),
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

                if reply == QtWidgets.QMessageBox.Yes:
                    search_online = True

                if search_online:
                    self.log.info("Looking up beatmaps")
                    QtWidgets.QMessageBox.information(self, 'Notification',
                                                      "Beatmaps loaded from the osu! API will be indicated with [ONLINE]")
                else:
                    self.log.info("NOT looking up beatmaps")
                    QtWidgets.QMessageBox.information(self, 'Notification',
                                                      "Unmatched beatmaps will be indicated with [UNMATCHED]")

            else:
                QtWidgets.QMessageBox.warning(self, 'Unmatched maps found',
                                              "{} beatmaps could not be matched. I could find their details via the osu! API, but you don't have your API key filled in in the settings.".format(unmatched_c))

        self.load_done.emit()

    def _load_done(self):
        # Clear the collection and songs lists
        self.ui.collection_list.clear()
        self.ui.songs_list.clear()

        # Add the collections to the left list
        for col in self.collections.collections:
            item = QtWidgets.QListWidgetItem(col.name)
            self.ui.collection_list.addItem(item)

        self.ui.collection_label.setText(self.collection_file)
        self.ui.statusbar.showMessage(
            "Loaded {} collections and {} songs.".format(self.collections.collection_count, len(self.songs.songs)))

    def closeEvent(self, event):
        self.log.info("Quitting")
        reply = QtWidgets.QMessageBox.question(self, 'Closing program',
                                               "Are you sure you want to quit?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def collection_list_clicked(self, item):
        # Find out which collection was clicked
        self.log.debug("User clicked on collection {}".format(item.text()))

        self.current_collection = self.collections.get_collection(item.text())

        # Clear the songs list
        self.ui.songs_list.clear()

        # Update the song list label
        self.ui.songs_label.setText(item.text())

        # Add the songs to the songs list
        for song in self.current_collection.beatmaps:
            if song.difficulty:
                name = song.difficulty.name
                if song.from_api:
                    name += " [ONLINE]"
            else:
                name = "{} [UNMATCHED]".format(song.hash)

            item = QtWidgets.QListWidgetItem(name)
            self.ui.songs_list.addItem(item)


    def songs_list_clicked(self, item):
        self.log.info("UNIMPLEMENTED: Songs_List_Clicked {}".format(item.text()))

    def add_collection(self):
        self.log.info("UNIMPLEMENTED: Add_Collection")

    def remove_collection(self):
        self.log.info("UNIMPLEMENTED: Remove_Collection")

    def options_collection(self):
        self.log.info("UNIMPLEMENTED: Options_Collection")

    def up_collection(self):
        self.log.info("UNIMPLEMENTED: Up_Collection")

    def down_collection(self):
        self.log.info("UNIMPLEMENTED: Down_Collection")

    def add_song(self):
        self.log.info("UNIMPLEMENTED: Add_Song")

    def remove_song(self):
        self.log.info("UNIMPLEMENTED: Remove_Song")

    def options_song(self):
        self.log.info("UNIMPLEMENTED: Options_Song")

    def up_song(self):
        self.log.info("UNIMPLEMENTED: Up_Song")

    def down_song(self):
        self.log.info("UNIMPLEMENTED: Down_Song")

    def about(self):
        self.log.critical("ABOUT")
