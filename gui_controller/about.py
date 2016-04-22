import logging

from PyQt5 import QtWidgets
import gui.about


class About(QtWidgets.QDialog):
    def __init__(self):
        super(About, self).__init__()
        self.log = logging.getLogger(__name__)

        self.ui = gui.about.Ui_AboutDialog()
        self.ui.setupUi(self)

        # Set the version string according to the current version
        from oce import __version__ as oce_version
        from oce import __build__ as oce_build
        self.ui.version_text.setText("Version {}, Build {}".format(oce_version, oce_build))
