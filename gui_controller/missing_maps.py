from logging.config import logging
from PyQt5 import QtWidgets, QtGui, QtCore
import gui.missing_maps
from settings import Settings
import webbrowser


class MissingMaps(QtWidgets.QDialog):

    def __init__(self, api, unmatched):
        super(MissingMaps, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.missing_maps.Ui_MissingMapsDialog()
        self.ui.setupUi(self)

        self.setModal(True)
        # self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)

        # Fix the column sizes so the last two colums (links) are small and fixed, and the mapper colum resizes
        header = QtWidgets.QHeaderView(QtCore.Qt.Horizontal, self.ui.api_table)
        self.ui.api_table.setHorizontalHeader(header)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        # Set initial sizes for interactive columns
        for i in range(0, 3):
            header.resizeSection(i, 160)

        # Set fixed sizes of icon columns
        for i in range(4, 6):
            header.resizeSection(i, 40)

        self.api_maps = api if api is not None else []
        self.unmatched_maps = unmatched if unmatched is not None else []
        self.link_lookup = {}

        # Connect open_link function to table clicked signal
        self.ui.api_table.cellClicked.connect(self.open_link)

        # Load icons
        self.osu_icon = QtGui.QIcon()
        self.osu_icon.addPixmap(QtGui.QPixmap("icons/osu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bloodcat_icon = QtGui.QIcon()
        self.bloodcat_icon.addPixmap(QtGui.QPixmap("icons/bloodcat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

    def exec_(self):

        # Add api maps
        self.ui.api_table.setRowCount(len(self.api_maps))
        for i, map in enumerate(self.api_maps):
            self.log.debug("Setting row {} to {}".format(i, map.difficulty))
            artist = QtWidgets.QTableWidgetItem(map.difficulty.artist)
            title = QtWidgets.QTableWidgetItem(map.difficulty.name)
            mapper = QtWidgets.QTableWidgetItem(map.difficulty.mapper)
            difficulty = QtWidgets.QTableWidgetItem(map.difficulty.difficulty)

            self.link_lookup[i] = [Settings.OSU_BEATMAP_URL.format(map.difficulty.beatmap_id),
                                   Settings.BLOODCAT_SEARCH_URL.format(map.difficulty.beatmap_id)]

            osu = QtWidgets.QTableWidgetItem("")
            osu.setIcon(self.osu_icon)
            bloodcat = QtWidgets.QTableWidgetItem("")
            bloodcat.setIcon(self.bloodcat_icon)

            for n, item in enumerate([artist, title, mapper, difficulty, osu, bloodcat]):
                self.ui.api_table.setItem(i, n, item)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        # Add unmatched maps
        for map in self.unmatched_maps:
            self.ui.unmatched_textbox.append("{}".format(map.hash))

        # Remove empty ui elements
        if len(self.api_maps) != 0 or len(self.unmatched_maps) != 0:
            self.ui.no_missing_label.hide()

        if len(self.api_maps) == 0:
            self.ui.api_box.hide()

        if len(self.unmatched_maps) == 0:
            self.ui.unmatched_box.hide()

        super(MissingMaps, self).exec_()

    def open_link(self, row, column):
        if column == 4:
            webbrowser.open(self.link_lookup[row][0])
        elif column == 5:
            webbrowser.open(self.link_lookup[row][1])

    def dismiss(self):
        self.hide()
