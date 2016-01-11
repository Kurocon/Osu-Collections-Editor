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
        self.unmatched_maps = None
        self.songs = None
        self.current_collection = None

        # Get settings instance
        self.settings = settings.Settings.get_instance()

        # Menu action handlers
        self.ui.action_open.triggered.connect(self.open)
        self.ui.action_save.triggered.connect(self.save)
        self.ui.action_close.triggered.connect(self.close)
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

        # Setup selectionChanged handlers
        self.ui.songs_list.itemSelectionChanged.connect(self.songs_list_selection_changed)

        # Collection list right click menu
        self.ui.collection_list.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # Create actions
        self.action_collection_list_add = QtWidgets.QAction("Add new collection", self.ui.collection_list)
        self.action_collection_list_remove = QtWidgets.QAction("Remove collection", self.ui.collection_list)
        self.action_collection_list_rename = QtWidgets.QAction("Rename collection", self.ui.collection_list)
        self.action_collection_list_moveup = QtWidgets.QAction("Move collection up", self.ui.collection_list)
        self.action_collection_list_movedown = QtWidgets.QAction("Move collection down", self.ui.collection_list)
        # Add actions to menu
        self.ui.collection_list.addAction(self.action_collection_list_add)
        self.ui.collection_list.addAction(self.action_collection_list_remove)
        self.ui.collection_list.addAction(self.action_collection_list_rename)
        self.ui.collection_list.addAction(self.action_collection_list_moveup)
        self.ui.collection_list.addAction(self.action_collection_list_movedown)
        # Connect to handlers
        self.action_collection_list_add.triggered.connect(self.add_collection)
        self.action_collection_list_remove.triggered.connect(self.remove_collection)
        self.action_collection_list_rename.triggered.connect(self.rename_collection)
        self.action_collection_list_moveup.triggered.connect(self.up_collection)
        self.action_collection_list_movedown.triggered.connect(self.down_collection)

        # Songs list right click menu
        self.ui.songs_list.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # Create actions
        self.action_song_list_add = QtWidgets.QAction("Add map/mapset", self.ui.songs_list)
        self.action_song_list_remove = QtWidgets.QAction("Remove map", self.ui.songs_list)
        self.action_song_list_remove_set = QtWidgets.QAction("Remove mapset", self.ui.songs_list)
        # Add actions to menu
        self.ui.songs_list.addAction(self.action_song_list_add)
        self.ui.songs_list.addAction(self.action_song_list_remove)
        self.ui.songs_list.addAction(self.action_song_list_remove_set)
        # Connect to handlers
        self.action_song_list_add.triggered.connect(self.add_song)
        self.action_song_list_remove.triggered.connect(self.remove_song)
        self.action_song_list_remove_set.triggered.connect(self.remove_set_song)

        # Add menu for collection list options button
        self.collection_options = QtWidgets.QMenu()
        # Create actions
        self.action_collection_options_add = QtWidgets.QAction("Add new collection", self.collection_options)
        self.action_collection_options_remove = QtWidgets.QAction("Remove collection", self.collection_options)
        self.action_collection_options_rename = QtWidgets.QAction("Rename collection", self.collection_options)
        self.action_collection_options_moveup = QtWidgets.QAction("Move collection up", self.collection_options)
        self.action_collection_options_movedown = QtWidgets.QAction("Move collection down", self.collection_options)
        # Add actions to menu
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
        # Connect to handlers
        self.action_collection_options_add.triggered.connect(self.add_collection)
        self.action_collection_options_remove.triggered.connect(self.remove_collection)
        self.action_collection_options_rename.triggered.connect(self.rename_collection)
        self.action_collection_options_moveup.triggered.connect(self.up_collection)
        self.action_collection_options_movedown.triggered.connect(self.down_collection)

        # Add menu for song list options button
        self.songs_options = QtWidgets.QMenu()
        # Create actions
        self.action_song_options_add = QtWidgets.QAction("Add map/mapset", self.songs_options)
        self.action_song_options_remove = QtWidgets.QAction("Remove map", self.songs_options)
        self.action_song_options_remove_set = QtWidgets.QAction("Remove mapset", self.songs_options)
        # Add actions to menu
        self.songs_options.addAction(self.action_song_options_add)
        self.songs_options.addAction(self.action_song_options_remove)
        self.songs_options.addAction(self.action_song_options_remove_set)
        self.ui.songs_options_button.setMenu(self.songs_options)
        self.ui.songs_options_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        # Remove the little menu arrow
        self.ui.songs_options_button.setStyleSheet('QToolButton::menu-indicator { image: none; }')
        # Connect to handlers
        self.action_song_options_add.triggered.connect(self.add_song)
        self.action_song_options_remove.triggered.connect(self.remove_song)
        self.action_song_options_remove_set.triggered.connect(self.remove_set_song)

        # Remove the column header from the song list
        self.ui.songs_list.header().close()

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

    def save(self):
        self.log.info("UNIMPLEMENTED: Save")

    def close(self):
        self.log.info("UNIMPLEMENTED: Close")

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
        self.unmatched_maps = unmatched_m

        # Notify if there are unmatched maps, to look them up online
        if unmatched_c != 0:
            self.log.debug("There are {} unmatched maps. Asking if they need to be looked up".format(unmatched_c))
            if self.settings.get_setting("osu_api_key"):
                reply = QtWidgets.QMessageBox.question(self, 'Unmatched maps found',
                                           "{} beatmaps could not be matched. Would you like me to try to find their details using the osu! API?".format(unmatched_c),
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

                search_online = reply == QtWidgets.QMessageBox.Yes

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

        # Enable the "Save" and "Close" buttons in the "File" menu
        for a in [self.ui.action_save, self.ui.action_close]:
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
        for song in self.current_collection.mapsets:
            tli = QtWidgets.QTreeWidgetItem()
            tli.setText(0, "{} - {} ({}) ({} maps)".format(song.difficulties[0].artist, song.difficulties[0].name,
                                                           song.difficulties[0].mapper, len(song.difficulties)))

            for diff in song.difficulties:
                # Create BeatmapItem
                bmi = BeatmapItem(diff)

                if diff:
                    bmi.set_name(diff.name, diff.artist)
                    bmi.set_artist(diff.mapper)
                    bmi.set_difficulty(diff.difficulty)
                    bmi.set_stars("AR{}, CS{}, HP{}, OD{}".format(diff.ar, diff.cs, diff.hp, diff.od))
                else:
                    bmi.set_name(diff.hash)
                    bmi.set_artist("?")
                    bmi.set_difficulty("?")
                    bmi.set_stars("AR?, CS?, HP?, OD?")

                # Set icon
                if not diff:
                    bmi.set_unmatched()
                elif diff.from_api:
                    bmi.set_from_internet()
                else:
                    bmi.set_local()

                # Create QListWidgetItem
                i = QtWidgets.QTreeWidgetItem()

                # Add item to top level item
                tli.addChild(i)
                self.ui.songs_list.setItemWidget(i, 0, bmi)

            self.ui.songs_list.addTopLevelItem(tli)

        # Add the unmatched beatmaps
        if self.current_collection.unmatched:
            umtli = QtWidgets.QTreeWidgetItem()
            umtli.setText(0, "Unmatched maps")

            for m in self.current_collection.unmatched:
                bmi = BeatmapItem(m)
                bmi.set_name(m.hash)
                bmi.set_artist("?")
                bmi.set_difficulty("?")
                bmi.set_stars("AR?, CS?, HP?, OD?")
                bmi.set_unmatched()
                i = QtWidgets.QTreeWidgetItem()
                umtli.addChild(i)
                self.ui.songs_list.setItemWidget(i, 0, bmi)

            self.ui.songs_list.addTopLevelItem(umtli)

    def songs_list_clicked(self, item):
        # Determine item type
        widget = self.ui.songs_list.itemWidget(item, 0)

        if isinstance(widget, BeatmapItem):
            self.log.debug("User clicked on beatmap {}".format(widget.ui.name_label.text()))

            # Activate remove map buttons and deactivate remove set buttons
            map_button_status = True
            set_button_status = True

        else:
            self.log.debug("User clicked on mapset {}".format(item.text(0)))

            # Deactivate remove map buttons and activate remove set buttons
            map_button_status = False
            set_button_status = True

        # Change remove map buttons status
        for a in [self.ui.songs_remove_button,
                  self.action_song_list_remove,
                  self.action_song_options_remove]:
            a.setEnabled(map_button_status)

        # Change remove set buttons status
        for a in [self.ui.songs_remove_set_button,
                  self.action_song_list_remove_set,
                  self.action_song_options_remove_set]:
            a.setEnabled(set_button_status)

    def songs_list_selection_changed(self):
        selected = self.ui.songs_list.selectedItems()

        # If nothing is selected, disable the remove buttons
        if not selected:
            # Change remove map buttons status
            for a in [self.ui.songs_remove_button,
                      self.action_song_list_remove,
                      self.action_song_options_remove]:
                a.setEnabled(False)

            # Change remove set buttons status
            for a in [self.ui.songs_remove_set_button,
                      self.action_song_list_remove_set,
                      self.action_song_options_remove_set]:
                a.setEnabled(False)

        # If something is selected, then we need to find out what is selected in order to enable the right buttons
        else:
            beatmaps_selected = False
            for i in selected:
                widget = self.ui.songs_list.itemWidget(i, 0)
                if isinstance(widget, BeatmapItem):
                    beatmaps_selected = True
                    break

            # Enable remove map buttons if there are beatmaps selected
            for a in [self.ui.songs_remove_button,
                      self.action_song_list_remove,
                      self.action_song_options_remove]:
                a.setEnabled(beatmaps_selected)

            # Enable the set remove buttons always
            for a in [self.ui.songs_remove_set_button,
                      self.action_song_list_remove_set,
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
            self.log.info("Added collection {}".format(name))

    def remove_collection(self):
        current_collection = self.ui.collection_list.currentItem()
        oldname = current_collection.text()

        # TODO: Add setting to disable confirmation dialog
        reply = QtWidgets.QMessageBox.question(self, 'Really remove this collection?',
                                               "Do you really want to delete the collection \"{}\"? This can only be undone by reloading the collection.".format(oldname),
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            # Remove collection from backend
            col = self.collections.get_collection(oldname)
            self.collections.collections.remove(col)

            # Remove collection from frontend
            position = self.ui.collection_list.row(current_collection)
            self.ui.collection_list.takeItem(position)
            del self.current_collection
            self.current_collection = None
            self.ui.statusbar.showMessage("Removed collection {}".format(oldname))
            self.log.info("Removed collection {}".format(oldname))

            # Clear the songs list
            self.ui.songs_list.clear()

            # Update the song list label
            self.ui.songs_label.setText("No collection selected.")

            # Disable collection remove/rename/up/down buttons
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
                a.setEnabled(False)

            # Disable remove map/mapset buttons
            for a in [self.ui.songs_remove_button,
                      self.ui.songs_remove_set_button,
                      self.action_song_list_remove,
                      self.action_song_list_remove_set,
                      self.action_song_options_remove,
                      self.action_song_options_remove_set]:
                a.setEnabled(False)

            # Disable songs add/option buttons
            for a in [self.ui.songs_add_button,
                      self.ui.songs_options_button,
                      self.action_song_list_add,
                      self.action_song_options_add]:
                a.setEnabled(False)

            # Load the currently selected collection into the songs list
            item = self.ui.collection_list.item(position) if self.ui.collection_list.item(position) else self.ui.collection_list.item(position-1)
            if item:
                self.log.debug("Simlating click on {} to load it into the songs list".format(item.text()))
                self.collection_list_clicked(item)

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
            self.log.info("Renamed collection from {} to {}".format(oldname, name))

    def up_collection(self):
        current_collection = self.ui.collection_list.currentItem()

        # Get current position
        position = self.ui.collection_list.row(current_collection)

        if position != 0:
            # Remove item from current position
            self.ui.collection_list.takeItem(position)
            # Re-insert item into position-1
            self.ui.collection_list.insertItem(position-1, current_collection)
            self.ui.collection_list.setCurrentRow(position-1)
            self.ui.statusbar.showMessage("Moved collection \"{}\" up.".format(current_collection.text()))
            self.log.info("Moved collection \"{}\" up.".format(current_collection.text()))
        else:
            self.ui.statusbar.showMessage("Collection is on the top, cannot move up.")
            self.log.info("Collection is on the top, cannot move up.")

    def down_collection(self):
        current_collection = self.ui.collection_list.currentItem()

        # Get current position
        position = self.ui.collection_list.row(current_collection)

        if position != self.ui.collection_list.count()-1:
            # Remove item from current position
            self.ui.collection_list.takeItem(position)
            # Re-insert item into position-1
            self.ui.collection_list.insertItem(position+1, current_collection)
            self.ui.collection_list.setCurrentRow(position+1)
            self.ui.statusbar.showMessage("Moved collection \"{}\" down.".format(current_collection.text()))
            self.log.info("Moved collection \"{}\" down.".format(current_collection.text()))
        else:
            self.ui.statusbar.showMessage("Collection is on the bottom, cannot move down.")
            self.log.info("Collection is on the bottom, cannot move down.")

    def add_song(self):
        self.log.info("UNIMPLEMENTED: Add_Song")

    def remove_song(self):
        selected_items = self.ui.songs_list.selectedItems()
        songs_to_remove = []

        # Add all songs we need to remove based on the selections
        if selected_items:
            for item in selected_items:
                widget = self.ui.songs_list.itemWidget(item, 0)
                if isinstance(widget, BeatmapItem):
                    # This is a beatmap, add its song to the remove list
                    thing = self.songs.get_song(widget.difficulty.hash)
                    if thing:
                        if (thing[1], item) not in songs_to_remove:
                            songs_to_remove.append((thing[1], item))
                    else:
                        self.log.debug("Could not find song for selected item {} in song database.".format(widget.ui.name_label.text()))
                        if (widget.ui.name_label.text(), item) not in songs_to_remove:
                            songs_to_remove.append((widget.ui.name_label.text(), item))

                else:
                    # This is a mapset, add all songs in it to the remove list
                    # First get all of the subitems
                    for i in range(item.childCount()):
                        child = item.child(i)

                        # Do the same as if it were an
                        widget = self.ui.songs_list.itemWidget(child, 0)
                        if isinstance(widget, BeatmapItem):
                            # This is a beatmap, add its song to the remove list
                            thing = self.songs.get_song(widget.difficulty.hash)
                            if thing:
                                if (thing[1], child) not in songs_to_remove:
                                    songs_to_remove.append((thing[1], child))
                            else:
                                self.log.debug("Could not find song for selected item {} in song database.".format(widget.ui.name_label.text()))
                                if (widget.ui.name_label.text(), child) not in songs_to_remove:
                                    songs_to_remove.append((widget.ui.name_label.text(), child))
                        else:
                            self.log.warning("Found weird TreeWidgetItem at 2 deep in the SongsList: {}".format(child))

            # TODO: Add setting to disable confirmation dialog
            reply = QtWidgets.QMessageBox.question(self, 'Really remove songs from collection?',
                                                   "<p>Do you really want to delete these songs from the collection \"{}\"? This can only be undone by reloading the collection database.</p>"
                                                   "<ul>{}</ul>".format(self.current_collection.name, "".join(["<li>{}</li>".format(i[0] if isinstance(i[0], str) else "{} - {} [{}] ({})".format(i[0].artist, i[0].name, i[0].difficulty, i[0].mapper)) for i in songs_to_remove])),
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                # Remove all of the songs from the collection
                for song in songs_to_remove:
                    # If the song is a string, it is an unmatched song
                    if isinstance(song[0], str):
                        # Remove from backend
                        unm = self.current_collection.get_unmatched_song(song[0])
                        self.current_collection.unmatched.remove(unm)

                        # Remove from frontend
                        item = song[1]
                        parent = item.parent()
                        parent.takeChild(parent.indexOfChild(item))

                        # If there are no more items in the mapset item, remove it, too.
                        if parent.childCount() == 0:
                            self.ui.songs_list.takeTopLevelItem(self.ui.songs_list.indexOfTopLevelItem(parent))

                    # Else, it is a normal song
                    else:
                        # Remove from backend
                        self.current_collection.remove_song(song[0])

                        # Remove from frontend
                        item = song[1]
                        parent = item.parent()
                        parent.takeChild(parent.indexOfChild(item))

                        # If there are no more items in the mapset item, remove it, too.
                        if parent.childCount() == 0:
                            self.ui.songs_list.takeTopLevelItem(self.ui.songs_list.indexOfTopLevelItem(parent))

                self.ui.statusbar.showMessage("Removed {} songs from {}.".format(len(songs_to_remove), self.current_collection.name))
                self.log.info("Removed {} songs from {}.".format(len(songs_to_remove), self.current_collection.name))

    def remove_set_song(self):
        selected_items = self.ui.songs_list.selectedItems()
        songs_to_remove = []
        sets_to_remove = []

        # Add all songs we need to remove based on the selections
        if selected_items:
            for item in selected_items:
                widget = self.ui.songs_list.itemWidget(item, 0)
                if isinstance(widget, BeatmapItem):
                    # This is a beatmap, add its parent to the set remove list
                    if item.parent() not in sets_to_remove:
                        sets_to_remove.append(item.parent())

                else:
                    # This is a mapset, it to the set remove list
                    if item not in sets_to_remove:
                        sets_to_remove.append(item)

            # Populate the songs_to_remove list with all songs from the sets to remove.
            for item in sets_to_remove:
                # First get all of the subitems
                for i in range(item.childCount()):
                    child = item.child(i)

                    # Do the same as if it were an
                    widget = self.ui.songs_list.itemWidget(child, 0)
                    if isinstance(widget, BeatmapItem):
                        # This is a beatmap, add its song to the remove list
                        thing = self.songs.get_song(widget.difficulty.hash)
                        if thing:
                            if (thing[1], child) not in songs_to_remove:
                                songs_to_remove.append((thing[1], child))
                        else:
                            self.log.debug("Could not find song for selected item {} in song database.".format(widget.ui.name_label.text()))
                            if (widget.ui.name_label.text(), child) not in songs_to_remove:
                                songs_to_remove.append((widget.ui.name_label.text(), child))
                    else:
                        self.log.warning("Found weird TreeWidgetItem at 2 deep in the SongsList: {}".format(child))

            # TODO: Add setting to disable confirmation dialog
            reply = QtWidgets.QMessageBox.question(self, 'Really remove songs from collection?',
                                                   "<p>Do you really want to delete these songs from the collection \"{}\"? This can only be undone by reloading the collection database.</p>"
                                                   "<ul>{}</ul>".format(self.current_collection.name, "".join(["<li>{}</li>".format(i[0] if isinstance(i[0], str) else "{} - {} [{}] ({})".format(i[0].artist, i[0].name, i[0].difficulty, i[0].mapper)) for i in songs_to_remove])),
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            # If yes, remove all songs from the remove list
            if reply == QtWidgets.QMessageBox.Yes:
                # Remove all of the songs from the collection
                for song in songs_to_remove:
                    # If the song is a string, it is an unmatched song
                    if isinstance(song[0], str):
                        # Remove from backend
                        unm = self.current_collection.get_unmatched_song(song[0])
                        self.current_collection.unmatched.remove(unm)

                        # Remove from frontend
                        item = song[1]
                        parent = item.parent()
                        parent.takeChild(parent.indexOfChild(item))

                        # If there are no more items in the mapset item, remove it, too.
                        if parent.childCount() == 0:
                            self.ui.songs_list.takeTopLevelItem(self.ui.songs_list.indexOfTopLevelItem(parent))

                    # Else, it is a normal song
                    else:
                        # Remove from backend
                        self.current_collection.remove_song(song[0])

                        # Remove from frontend
                        item = song[1]
                        parent = item.parent()
                        parent.takeChild(parent.indexOfChild(item))

                        # If there are no more items in the mapset item, remove it, too.
                        if parent.childCount() == 0:
                            self.ui.songs_list.takeTopLevelItem(self.ui.songs_list.indexOfTopLevelItem(parent))

                self.ui.statusbar.showMessage("Removed {} songs from {}.".format(len(songs_to_remove), self.current_collection.name))
                self.log.info("Removed {} songs from {}.".format(len(songs_to_remove), self.current_collection.name))

    def about(self):
        self.log.critical("ABOUT")
        QtWidgets.QMessageBox.information(self, 'About Osu! Collections Editor',
                                          "<h3>Osu! Collections Editor</h3>"
                                          "<p>OCE is created by Kurocon.</p>"
                                          "<p><a href=\"http://kevinalberts.nl/\">My website</a></p>"
                                          "<p><a href=\"https://gitlab.kurocon.nl/Kurocon/OsuCollectionsEditor/\">Source code</a></p>")
