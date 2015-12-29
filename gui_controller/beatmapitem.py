import logging

from PyQt5 import QtWidgets, QtGui
import gui.beatmapitem


class BeatmapItem(QtWidgets.QWidget):
    def __init__(self):
        super(BeatmapItem, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.beatmapitem.Ui_BeatmapItem()
        self.ui.setupUi(self)

    def set_name(self, name, artist=None):
        if artist:
            self.ui.name_label.setText("{} - {}".format(artist, name))
        else:
            self.ui.name_label.setText("{}".format(name))

    def set_artist(self, mapper):
        self.ui.mapper_label.setText("({})".format(mapper))

    def set_difficulty(self, difficulty):
        self.ui.difficulty_label.setText(difficulty)

    def set_stars(self, stars):
        self.ui.star_label.setText("({})".format(stars))

    def set_unmatched(self):
        self.ui.warning_label.setPixmap(QtGui.QPixmap("icons/warning.png"))
        self.ui.warning_label.setStatusTip("You do not have this song in your songs directory.")
        self.ui.warning_label.setToolTip("You do not have this song in your songs directory.")

    def set_from_internet(self):
        self.ui.warning_label.setPixmap(QtGui.QPixmap("icons/internet.png"))
        self.ui.warning_label.setStatusTip("You do not have this song. Its details were loaded from the internet.")
        self.ui.warning_label.setToolTip("You do not have this song. Its details were loaded from the internet.")

    def set_local(self):
        self.ui.warning_label.setPixmap(QtGui.QPixmap("icons/local.png"))
        self.ui.warning_label.setStatusTip("This is a local beatmap.")
