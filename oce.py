from logging.config import fileConfig, logging

from PyQt5 import QtWidgets
from gui_controller.startup import Startup
from gui_controller.main import MainWindow
import sys


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()


def startup():
    app = QtWidgets.QApplication(sys.argv)
    form = Startup()
    form.show()
    app.exec_()


if __name__ == "__main__":
    fileConfig('logging.conf')
    log = logging.getLogger(__name__)
    log.debug("Debugging mode enabled...")
    log.info("osu! Collection Editor starting...")

    main()
