import threading
from logging.config import logging
import time
from PyQt5 import QtWidgets, QtCore
import gui.main
import settings
from gui_controller.beatmapitem import BeatmapItem
from gui_controller.loading import Loading
from gui_controller.startup import Startup

import util.song_collection_matcher as scm
from util.collections_parser import Collection


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
        self.ui.rename_collection_button.clicked.connect(self.rename_collection)
        self.ui.up_collection_button.clicked.connect(self.up_collection)
        self.ui.down_collection_button.clicked.connect(self.down_collection)

        self.ui.songs_add_button.clicked.connect(self.add_song)
        self.ui.songs_remove_button.clicked.connect(self.remove_song)
        self.ui.songs_remove_set_button.clicked.connect(self.remove_set_song)

        # Setup list onclick handlers
        self.ui.collection_list.itemClicked.connect(self.collection_list_clicked)  # Collection list left click
        self.ui.songs_list.itemClicked.connect(self.songs_list_clicked)  # Song list left click

        # Collection list right click menu TODO: Connect to handlers
        self.ui.collection_list.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.action_collection_list_add = QtWidgets.QAction("Add new collection", self.ui.collection_list)
        self.action_collection_list_remove = QtWidgets.QAction("Remove collection", self.ui.collection_list)
        self.action_collection_list_rename = QtWidgets.QAction("Rename collection", self.ui.collection_list)
        self.action_collection_list_moveup = QtWidgets.QAction("Move collection up", self.ui.collection_list)
        self.action_collection_list_movedown = QtWidgets.QAction("Move collection down", self.ui.collection_list)
        self.ui.collection_list.addAction(self.action_collection_list_add)
        self.ui.collection_list.addAction(self.action_collection_list_remove)
        self.ui.collection_list.addAction(self.action_collection_list_rename)
        self.ui.collection_list.addAction(self.action_collection_list_moveup)
        self.ui.collection_list.addAction(self.action_collection_list_movedown)

        # Songs list right click menu TODO: Connect to handlers
        self.ui.songs_list.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.action_song_list_add = QtWidgets.QAction("Add map/mapset", self.ui.songs_list)
        self.action_song_list_remove = QtWidgets.QAction("Remove map", self.ui.songs_list)
        self.action_song_list_remove_set = QtWidgets.QAction("Remove mapset", self.ui.songs_list)
        self.ui.songs_list.addAction(self.action_song_list_add)
        self.ui.songs_list.addAction(self.action_song_list_remove)
        self.ui.songs_list.addAction(self.action_song_list_remove_set)

        # Add menu for collection list options button TODO: Connect to handlers
        self.collection_options = QtWidgets.QMenu()
        self.action_collection_options_add = QtWidgets.QAction("Add new collection", self.collection_options)
        self.action_collection_options_remove = QtWidgets.QAction("Remove collection", self.collection_options)
        self.action_collection_options_rename = QtWidgets.QAction("Rename collection", self.collection_options)
        self.action_collection_options_moveup = QtWidgets.QAction("Move collection up", self.collection_options)
        self.action_collection_options_movedown = QtWidgets.QAction("Move collection down", self.collection_options)
        self.collection_options.addAction(self.action_collection_options_add)
        self.collection_options.addSeparator()
        self.collection_options.addAction(self.action_collection_options_remove)
        self.collection_options.addAction(self.action_collection_options_rename)
        self.collection_options.addSeparator()
        self.collection_options.addAction(self.action_collection_options_moveup)
        self.collection_options.addAction(self.action_collection_options_movedown)
        self.ui.options_collection_button.setMenu(self.collection_options)
        self.ui.options_collection_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        # Remove the little menu arrow
        self.ui.options_collection_button.setStyleSheet('QToolButton::menu-indicator { image: none; }')

        # Add menu for song list options button TODO: Connect to handlers
        self.songs_options = QtWidgets.QMenu()
        self.action_song_options_add = QtWidgets.QAction("Add map/mapset", self.songs_options)
        self.action_song_options_remove = QtWidgets.QAction("Remove map", self.songs_options)
        self.action_song_options_remove_set = QtWidgets.QAction("Remove mapset", self.songs_options)
        self.songs_options.addAction(self.action_song_options_add)
        self.songs_options.addAction(self.action_song_options_remove)
        self.songs_options.addAction(self.action_song_options_remove_set)
        self.ui.songs_options_button.setMenu(self.songs_options)
        self.ui.songs_options_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        # Remove the little menu arrow
        self.ui.songs_options_button.setStyleSheet('QToolButton::menu-indicator { image: none; }')

        # Disable all actions for now.
        for a in [self.action_collection_list_add,
                  self.action_collection_list_remove,
                  self.action_collection_list_rename,
                  self.action_collection_list_moveup,
                  self.action_collection_list_movedown,
                  self.action_collection_options_add,
                  self.action_collection_options_remove,
                  self.action_collection_options_rename,
                  self.action_collection_options_moveup,
                  self.action_collection_options_movedown,
                  self.action_song_list_add,
                  self.action_song_list_remove,
                  self.action_song_list_remove_set,
                  self.action_song_options_add,
                  self.action_song_options_remove,
                  self.action_song_options_remove_set]:
            a.setEnabled(False)

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
                                                      "Beatmaps loaded from the osu! API will be indicated with a blue icon")
                else:
                    self.log.info("NOT looking up beatmaps")
                    QtWidgets.QMessageBox.information(self, 'Notification',
                                                      "Unmatched beatmaps will be indicated with a yellow icon")

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

        # Enable collection buttons and menus
        for a in [self.ui.add_collection_button,
                  self.ui.options_collection_button,
                  self.action_collection_list_add,
                  self.action_collection_options_add]:
            a.setEnabled(True)

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

        # Enable collection remove/rename/up/down buttons
        for a in [self.ui.remove_collection_button,
                  self.ui.rename_collection_button,
                  self.ui.up_collection_button,
                  self.ui.down_collection_button,
                  self.action_collection_list_remove,
                  self.action_collection_list_rename,
                  self.action_collection_list_moveup,
                  self.action_collection_list_movedown,
                  self.action_collection_options_remove,
                  self.action_collection_options_rename,
                  self.action_collection_options_moveup,
                  self.action_collection_options_movedown]:
            a.setEnabled(True)

        # Disable remove map/mapset buttons
        for a in [self.ui.songs_remove_button,
                  self.ui.songs_remove_set_button,
                  self.action_song_list_remove,
                  self.action_song_list_remove_set,
                  self.action_song_options_remove,
                  self.action_song_options_remove_set]:
            a.setEnabled(False)

        # Enable songs add/option buttons
        for a in [self.ui.songs_add_button,
                  self.ui.songs_options_button,
                  self.action_song_list_add,
                  self.action_song_options_add]:
            a.setEnabled(True)

        # Add the songs to the songs list
        for song in self.current_collection.beatmaps:
            # Create BeatmapItem
            bmi = BeatmapItem()

            if song.difficulty:
                bmi.set_name(song.difficulty.name, song.difficulty.artist)
                bmi.set_artist(song.difficulty.mapper)
                bmi.set_difficulty(song.difficulty.difficulty)
                bmi.set_stars("AR{}, CS{}, HP{}, OD{}".format(song.difficulty.ar,
                                                              song.difficulty.cs,
                                                              song.difficulty.hp,
                                                              song.difficulty.od))
            else:
                bmi.set_name(song.hash)
                bmi.set_artist("?")
                bmi.set_difficulty("?")
                bmi.set_stars("AR?, CS?, HP?, OD?")

            # Set icon
            if not song.difficulty:
                bmi.set_unmatched()
            elif song.from_api:
                bmi.set_from_internet()
            else:
                bmi.set_local()

            # Create QListWidgetItem
            item = QtWidgets.QListWidgetItem(self.ui.songs_list)
            item.setSizeHint(bmi.sizeHint())

            # Add item into songs list
            self.ui.songs_list.addItem(item)
            self.ui.songs_list.setItemWidget(item, bmi)

    # TODO: Change song list to a treeview to illustrate mapsets
    def songs_list_clicked(self):
        # Activate remove map/mapset buttons
        for a in [self.ui.songs_remove_button,
                  self.ui.songs_remove_set_button,
                  self.action_song_list_remove,
                  self.action_song_list_remove_set,
                  self.action_song_options_remove,
                  self.action_song_options_remove_set]:
            a.setEnabled(True)

    def add_collection(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'New collection', 'What will your new collection be called?')

        if ok:
            new_coll = Collection()
            new_coll.name = name
            self.collections.collections.append(new_coll)
            item = QtWidgets.QListWidgetItem(new_coll.name)
            self.ui.collection_list.addItem(item)
            self.ui.statusbar.showMessage("Added collection {}".format(name))

    def remove_collection(self):
        self.log.info("UNIMPLEMENTED: Remove_Collection")

    def rename_collection(self):
        current_collection = self.ui.collection_list.currentItem()
        oldname = current_collection.text()
        name, ok = QtWidgets.QInputDialog.getText(self, 'Rename collection',
                                                  'Enter a new name for the collection {}'.format(oldname))

        if ok:
            # Update name in backend
            self.collections.get_collection(oldname).name = name
            # Update name in frontend
            current_collection.setText(name)
            self.ui.statusbar.showMessage("Renamed collection from {} to {}".format(oldname, name))

    def up_collection(self):
        self.log.info("UNIMPLEMENTED: Up_Collection")

    def down_collection(self):
        self.log.info("UNIMPLEMENTED: Down_Collection")

    def add_song(self):
        self.log.info("UNIMPLEMENTED: Add_Song")

    def remove_song(self):
        self.log.info("UNIMPLEMENTED: Remove_Song")

    def remove_set_song(self):
        self.log.info("UNIMPLEMENTED: Remove_Set_Song")

    def about(self):
        self.log.critical("ABOUT")
        QtWidgets.QMessageBox.information(self, 'About Osu! Collections Editor',
                                          "<h3>Osu! Collections Editor</h3>"
                                          "<p>OCE is created by Kurocon.</p>")
