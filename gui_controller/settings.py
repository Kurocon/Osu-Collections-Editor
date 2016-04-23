import logging
import pprint

from PyQt5 import QtWidgets
import gui.settings
import settings
import json


class Settings(QtWidgets.QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.settings.Ui_SettingsDialog()
        self.ui.setupUi(self)

        # Get settings instance
        self.settings = settings.Settings.get_instance()

        # Set current values from settings
        self.ui.api_key_line.setText(self.settings.get_setting("osu_api_key"))
        self.ui.download_api_combobox.setCurrentIndex(self.settings.get_setting("download_from_api"))
        self.ui.default_songs_line.setText(self.settings.get_setting("default_songs_dir"))
        self.ui.default_collection_line.setText(self.settings.get_setting("default_collection_file"))
        self.ui.shutdown_dialog_checkbox.setChecked(self.settings.get_setting("show_shutdown_dialog"))
        self.ui.api_explanation_dialog.setChecked(self.settings.get_setting("show_api_explanation_dialog"))
        self.ui.collection_delete_dialog.setChecked(self.settings.get_setting("show_collection_delete_dialog"))
        self.ui.song_remove_dialog.setChecked(self.settings.get_setting("show_remove_song_dialog"))
        self.ui.mapset_remove_dialog.setChecked(self.settings.get_setting("show_remove_mapset_dialog"))

        # Setup handlers for buttons
        self.ui.default_songs_button.clicked.connect(self.browse_osudir)
        self.ui.default_collection_button.clicked.connect(self.browse_collectionfile)

        # Setup handlers for OK/Cancel/Apply buttons
        self.ui.button_box.accepted.connect(self.accept)
        self.ui.button_box.rejected.connect(self.reject)
        self.ui.button_box.clicked.connect(self.button_clicked)

    def button_clicked(self, button):
        if button.text() == "Apply":
            self.apply_settings()

    def accept(self):
        # Apply settings before leaving
        self.apply_settings()
        super(Settings, self).accept()

    def apply_settings(self):
        # Update settings
        self.settings.set_setting('osu_api_key', self.ui.api_key_line.text())
        self.settings.set_setting('download_from_api', self.ui.download_api_combobox.currentIndex())
        self.settings.set_setting('default_songs_dir', self.ui.default_songs_line.text())
        self.settings.set_setting('default_collection_file', self.ui.default_collection_line.text())
        self.settings.set_setting('show_shutdown_dialog', self.ui.shutdown_dialog_checkbox.isChecked())
        self.settings.set_setting('show_api_explanation_dialog', self.ui.api_explanation_dialog.isChecked())
        self.settings.set_setting('show_collection_delete_dialog', self.ui.collection_delete_dialog.isChecked())
        self.settings.set_setting('show_remove_song_dialog', self.ui.song_remove_dialog.isChecked())
        self.settings.set_setting('show_remove_mapset_dialog', self.ui.mapset_remove_dialog.isChecked())

        # Export settings to file
        with open('settings.json', 'w', encoding='utf8') as f:
                json.dump(self.settings.settings, f, sort_keys=True, indent=4)

        self.log.info("Settings were applied.")

    def browse_osudir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                               "Pick your osu! Song folder",
                                                               self.ui.default_songs_line.text())

        if directory:
            self.ui.default_songs_line.setText(directory)

        self.log.debug("New default song dir: {}".format(self.ui.default_songs_line.text()))

    def browse_collectionfile(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Pick your osu! collection.db file",
                                                     self.ui.default_collection_line.text(),
                                                     "Osu Collections (collection.db);;All files (*)")

        if file:
            self.ui.default_collection_line.setText(file[0])

        self.log.debug("New default collection file: {}".format(self.ui.default_collection_line.text()))
