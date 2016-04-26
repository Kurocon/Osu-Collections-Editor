import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
import gui.addsongs
import settings
from gui_controller.beatmapitem import BeatmapItem
from gui_controller.loading_addsong import LoadingAddSong

from util.oce_models import Songs


class AddSongs(QtWidgets.QMainWindow):
    opened = pyqtSignal()
    closed = pyqtSignal()

    def __init__(self, collectionname, songs):
        """
        :type collectionname: str
        :type songs: Songs
        """
        super(AddSongs, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.addsongs.Ui_AddSongs()
        self.ui.setupUi(self)

        # Setup loading dialog
        loading_dialog = LoadingAddSong()
        loading_dialog.open()
        loading_dialog.text.emit("Loading song list...")

        # Get settings instance
        self.settings = settings.Settings.get_instance()

        self.collectionname = collectionname
        self.songs = songs

        # Set strings correctly
        self.setWindowTitle("Add songs to {}".format(collectionname))
        self.ui.addsongs_groupbox.setTitle("Songs to add to {}".format(collectionname))

        # Clear the left list
        self.ui.allsongs_list.clear()

        # Progress bar
        progress = 0
        total_progress = len(self.songs.songs)
        bar_progress = 0

        # Create backup list of top level items
        self.allsongs_toplevel_items = []
        self.previous_search = ""

        # Add songs to left tree
        for song in self.songs.songs:
            if len(song.difficulties) > 0:
                if bar_progress < int((progress / total_progress) * 100):
                    bar_progress = int((progress / total_progress) * 100)
                    loading_dialog.progress.emit(int((progress / total_progress) * 100))
                    loading_dialog.current.emit(
                        "({}/{}) {} - {} ({}) ({} maps)".format(progress, total_progress, song.difficulties[0].artist,
                                                                song.difficulties[0].name, song.difficulties[0].mapper,
                                                                len(song.difficulties)))
                progress += 1

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
                    self.ui.allsongs_list.setItemWidget(i, 0, bmi)

                self.ui.allsongs_list.addTopLevelItem(tli)
                self.allsongs_toplevel_items.append(tli)

        # Activate the buttonz
        for a in [self.ui.add_beatmap_button, self.ui.add_mapset_button,
                  self.ui.remove_beatmap_button, self.ui.remove_mapset_button]:
            a.setEnabled(True)

        # Attach button handlers
        self.ui.add_beatmap_button.clicked.connect(self.add_beatmap)
        self.ui.add_mapset_button.clicked.connect(self.add_mapset)
        self.ui.remove_beatmap_button.clicked.connect(self.remove_beatmap)
        self.ui.remove_mapset_button.clicked.connect(self.remove_mapset)
        self.ui.allsongs_search_field.textChanged.connect(self.searchbar_updated)

        # Attach cancel and ok buttons signals to the appropriate function
        self.ui.confirmation_buttons.accepted.connect(self.accept)
        self.ui.confirmation_buttons.rejected.connect(self.reject)

        loading_dialog.done.emit()

    def closeEvent(self, *args, **kwargs):
        self.closed.emit()
        super(AddSongs, self).closeEvent(*args, **kwargs)

    def show(self):
        # Re-set strings correctly
        self.setWindowTitle("Add songs to {}".format(self.collectionname))
        self.ui.addsongs_groupbox.setTitle("Songs to add to {}".format(self.collectionname))
        self.ui.allsongs_search_field.setText("")
        self.searchbar_updated("")
        self.opened.emit()
        super(AddSongs, self).show()
    
    def hide(self):
        self.closed.emit()
        super(AddSongs, self).hide()

    def accept(self):
        self.hide()

    def reject(self):
        self.hide()

    def add_beatmap(self):
        selected_items = self.ui.allsongs_list.selectedItems()
        songs_to_add = []

        # Add all songs we need to remove based on the selections
        if selected_items:
            for item in selected_items:
                widget = self.ui.allsongs_list.itemWidget(item, 0)
                if isinstance(widget, BeatmapItem):
                    # This is a beatmap, add it to the songs list if it is not already in there
                    if item not in songs_to_add:
                        songs_to_add.append(item)

                else:
                    # This is a mapset, add all songs in it to the remove list
                    # First get all of the subitems
                    for i in range(item.childCount()):
                        child = item.child(i)

                        # Do the same as if it were an
                        widget = self.ui.allsongs_list.itemWidget(child, 0)
                        if isinstance(widget, BeatmapItem):
                            # This is a beatmap, add it to the songs list if it is not already in there
                            if item not in songs_to_add:
                                songs_to_add.append(child)
                        else:
                            self.log.warning("Found weird TreeWidgetItem at 2 deep in the SongsList: {}".format(child))

            tlis = [self.ui.addsongs_list.topLevelItem(t) for t in range(self.ui.addsongs_list.topLevelItemCount())]
            # Add all of the songs to the left list
            for song in songs_to_add:
                tli = None

                # Find toplevelitem
                for t in tlis:
                    if t.text(0) == song.parent().text(0):
                        tli = t
                        break

                if not tli:
                    tli = QtWidgets.QTreeWidgetItem()
                    tli.setText(0, song.parent().text(0))
                    tlis.append(tli)
                    self.ui.addsongs_list.addTopLevelItem(tli)

                # Add item to top level item
                diff = self.ui.allsongs_list.itemWidget(song, 0).difficulty

                continue_add = True

                for t in tlis:
                    for c in [t.child(i) for i in range(t.childCount())]:
                        if diff == self.ui.addsongs_list.itemWidget(c, 0).difficulty:
                            continue_add = False
                            break

                if continue_add:
                    # Create BeatmapItem
                    bmi = BeatmapItem(diff)
                    bmi.set_name(diff.name, diff.artist)
                    bmi.set_artist(diff.mapper)
                    bmi.set_difficulty(diff.difficulty)
                    bmi.set_stars("AR{}, CS{}, HP{}, OD{}".format(diff.ar, diff.cs, diff.hp, diff.od))
                    bmi.set_local()

                    # Create QListWidgetItem
                    i = QtWidgets.QTreeWidgetItem()

                    # Add item to top level item
                    tli.addChild(i)
                    self.ui.addsongs_list.setItemWidget(i, 0, bmi)

    def add_mapset(self):
        selected_items = self.ui.allsongs_list.selectedItems()
        songs_to_add = []

        # Add all songs we need to remove based on the selections
        if selected_items:
            for item in selected_items:
                widget = self.ui.allsongs_list.itemWidget(item, 0)
                if isinstance(widget, BeatmapItem):
                    # This is a beatmap, get its parent and add all of its children
                    parent = item.parent()
                    for i in range(parent.childCount()):
                        if parent.child(i) not in songs_to_add:
                            songs_to_add.append(parent.child(i))

                else:
                    # This is a mapset, add all songs in it to the remove list
                    for i in range(item.childCount()):
                        if item.child(i) not in songs_to_add:
                            songs_to_add.append(item.child(i))

            tlis = [self.ui.addsongs_list.topLevelItem(t) for t in range(self.ui.addsongs_list.topLevelItemCount())]
            # Add all of the songs to the left list
            for song in songs_to_add:
                tli = None

                # Find toplevelitem
                for t in tlis:
                    if t.text(0) == song.parent().text(0):
                        tli = t
                        break

                if not tli:
                    tli = QtWidgets.QTreeWidgetItem()
                    tli.setText(0, song.parent().text(0))
                    tlis.append(tli)
                    self.ui.addsongs_list.addTopLevelItem(tli)

                # Add item to top level item
                diff = self.ui.allsongs_list.itemWidget(song, 0).difficulty

                continue_add = True

                for t in tlis:
                    for c in [t.child(i) for i in range(t.childCount())]:
                        if diff == self.ui.addsongs_list.itemWidget(c, 0).difficulty:
                            continue_add = False
                            break

                if continue_add:
                    # Create BeatmapItem
                    bmi = BeatmapItem(diff)
                    bmi.set_name(diff.name, diff.artist)
                    bmi.set_artist(diff.mapper)
                    bmi.set_difficulty(diff.difficulty)
                    bmi.set_stars("AR{}, CS{}, HP{}, OD{}".format(diff.ar, diff.cs, diff.hp, diff.od))
                    bmi.set_local()

                    # Create QListWidgetItem
                    i = QtWidgets.QTreeWidgetItem()

                    # Add item to top level item
                    tli.addChild(i)
                    self.ui.addsongs_list.setItemWidget(i, 0, bmi)

    def remove_beatmap(self):
        selected_items = self.ui.addsongs_list.selectedItems()
        songs_to_remove = []

        # Add all songs we need to remove based on the selections
        if selected_items:
            for item in selected_items:
                widget = self.ui.addsongs_list.itemWidget(item, 0)
                if isinstance(widget, BeatmapItem):
                    # This is a beatmap, add its song to the remove list
                    if item not in songs_to_remove:
                        songs_to_remove.append(item)

                else:
                    # This is a mapset, add all songs in it to the remove list
                    # First get all of the subitems
                    for i in range(item.childCount()):
                        child = item.child(i)
                        if child not in songs_to_remove:
                            songs_to_remove.append(child)

            # Remove all of the songs
            for song in songs_to_remove:
                # Remove from frontend
                parent = song.parent()
                parent.takeChild(parent.indexOfChild(song))

                # If there are no more items in the mapset item, remove it, too.
                if parent.childCount() == 0:
                    self.ui.addsongs_list.takeTopLevelItem(self.ui.addsongs_list.indexOfTopLevelItem(parent))

    def remove_mapset(self):
        selected_items = self.ui.addsongs_list.selectedItems()
        songs_to_remove = []
        sets_to_remove = []

        # Add all songs we need to remove based on the selections
        if selected_items:
            for item in selected_items:
                widget = self.ui.addsongs_list.itemWidget(item, 0)
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
                    if child not in songs_to_remove:
                        songs_to_remove.append(child)

            # Remove all of the songs
            for song in songs_to_remove:
                # Remove from frontend
                parent = song.parent()
                parent.takeChild(parent.indexOfChild(song))

                # If there are no more items in the mapset item, remove it, too.
                if parent.childCount() == 0:
                    self.ui.addsongs_list.takeTopLevelItem(self.ui.addsongs_list.indexOfTopLevelItem(parent))

    def searchbar_updated(self, text):
        # Search in the TreeView
        match = Qt.MatchWildcard | Qt.MatchContains | Qt.MatchWrap |\
                Qt.MatchStartsWith | Qt.MatchEndsWith | Qt.MatchFixedString
        matches = self.ui.allsongs_list.findItems(text, match)

        # Hide, uncollapse and unselect all items in the TreeView
        for y in self.allsongs_toplevel_items:
            y.setHidden(True)
            y.setExpanded(False)
            y.setSelected(False)

        # Unhide the found items
        first = True
        for y in matches:
            y.setHidden(False)

            # If there are less than three results, expand them
            if len(matches) < 3:
                y.setExpanded(True)

            # Select the first match
            if first:
                y.setSelected(True)
                first = False
