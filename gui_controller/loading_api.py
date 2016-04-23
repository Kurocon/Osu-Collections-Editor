from logging.config import logging
from PyQt5 import QtWidgets, QtCore, QtGui
import gui.loading
import settings
import util.osu_parser as op
import util.osu_api as oa


class LoadingApi(QtWidgets.QDialog):
    progress = QtCore.pyqtSignal(int)
    current = QtCore.pyqtSignal(str)
    text = QtCore.pyqtSignal(str)
    done = QtCore.pyqtSignal()

    def __init__(self, collections, unmatched_maps):
        super(LoadingApi, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.loading.Ui_LoadingDialog()
        self.ui.setupUi(self)

        self.setModal(True)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)

        self.collections = collections
        self.unmatched_maps = unmatched_maps
        self.api_matched_maps = []

        self.progress.connect(self.update_precentage)
        self.current.connect(self.update_current)
        self.text.connect(self.update_text)
        self.done.connect(self.dismiss)

        self.ui.progressbar.setRange(0, 100)

        self.thread = QtCore.QThread()

    def keyPressEvent(self, event):
        if event.key() not in [QtCore.Qt.Key_Escape, QtCore.Qt.Key_Alt, QtCore.Qt.Key_AltGr, QtCore.Qt.Key_F4]:
            super(LoadingApi, self).keyPressEvent(event)

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
        w = LoadApiTask(self.collections, self.unmatched_maps, self)
        w.moveToThread(self.thread)
        self.thread.started.connect(w.work)
        self.thread.start()
        super(LoadingApi, self).exec_()

    def dismiss(self):
        self.hide()


class LoadApiTask(QtCore.QObject):
    def __init__(self, cols, umaps, dialog):
        super(LoadApiTask, self).__init__()
        self.collections = cols
        self.unmatched_maps = umaps
        self.api_matched_maps = []
        self.dialog = dialog
        self.settings = settings.Settings.get_instance()
        self.log = logging.getLogger(__name__)

    def work(self):
        # Load maps from API
        self.log.debug("Loading from API...")
        self.dialog.text.emit("Loading from API...")

        # Try to look up every unmatched beatmap
        umaps = self.unmatched_maps[:]
        mmaps = []
        identified_count = 0
        progress = 0
        total_progress = len(umaps)
        for umap in umaps:

            # Update progressbar
            self.log.debug("Processing {}, progress: {}/{}={}%".format(umap.hash, progress, total_progress, int((progress/total_progress)*100)))
            self.dialog.progress.emit(int((progress/total_progress)*100))
            self.dialog.current.emit(umap.hash)
            progress += 1

            res = oa.get_beatmap_by_hash(umap.hash)

            if res:
                details = res[0]
                # Create a difficulty for the map
                diff = op.Difficulty2("api")
                diff.name = details['title']
                diff.artist = details['artist']
                diff.mapper = details['creator']
                diff.difficulty = details['version']
                diff.ar = float(details['diff_approach'])
                diff.cs = float(details['diff_size'])
                diff.hp = float(details['diff_drain'])
                diff.od = float(details['diff_overall'])
                diff.hash = umap.hash
                diff.from_api = True
                umap.from_api = True
                diff.beatmap_id = details['beatmap_id']

                self.dialog.current.emit("{} found!".format(umap.hash))

                # Try to set the mapset of the beatmap and create a new one if we fail
                for m in mmaps:
                    if hasattr(m.mapset, 'beatmapset_id') and m.mapset.beatmapset_id == int(details['beatmapset_id']):
                        self.log.debug("Linked beatpam {} - {} [{}] to mapset {}".format(diff.artist, diff.name, diff.difficulty, m.mapset.beatmapset_id))
                        # There is a mapset! Add it to the mapset and use this mapset
                        m.mapset.add_difficulty(diff)
                        umap.mapset = m.mapset
                        umap.difficulty = diff
                        mmaps.append(umap)
                        break
                # If the for loop ended without breaking, create a mapset for this map
                else:
                    umap.mapset = op.Song()
                    umap.mapset.add_difficulty(diff)
                    umap.mapset.beatmapset_id = int(details['beatmapset_id'])
                    self.log.debug("Created new mapset for beatpam {} - {} [{}] (beatmapset_id {})".format(diff.artist, diff.name, diff.difficulty, umap.mapset.beatmapset_id))
                    umap.difficulty = diff
                    mmaps.append(umap)
                # Remove the map from the unmatched maps, it is now matched.
                identified_count += 1
                self.unmatched_maps.remove(umap)
                self.api_matched_maps.append(umap)

        # Add all maps that are now matched to the collection properly.
        self.log.debug("Adding found maps to collections...")
        self.dialog.text.emit("Adding found maps to collections...")
        self.dialog.progress.emit(99)

        for col in self.collections.collections:
            unm = col.unmatched[:]
            for um in unm:
                self.dialog.current.emit(um.hash)
                # If this map is now matched, remove it from the unmatched maps and add the mapset.
                replacement = next((x for x in mmaps if x.hash == um.hash), None)
                if replacement:
                    self.log.debug("Found replacement for {} in collection {}".format(um.hash, col.name))
                    col.unmatched.remove(um)
                    # Add the mapset if it isn't already in the list
                    if um.mapset not in col.mapsets:
                        col.mapsets.append(replacement.mapset)

        self.dialog.progress.emit(100)

        self.dialog.identified_count = identified_count
        self.dialog.collections = self.collections
        self.dialog.unmatched_maps = self.unmatched_maps
        self.dialog.api_matched_maps = self.api_matched_maps

        # Notify we're done.
        self.dialog.done.emit()
