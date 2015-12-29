import signal
from logging.config import fileConfig, logging

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox

from gui_controller.startup import Startup
from gui_controller.main import MainWindow
import sys


def main():
    # Add Interrupt handler
    signal.signal(signal.SIGINT, sigint_handler)

    # Create application
    app = QApplication(sys.argv)

    # Add timer to make time to handle interrupts
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)  # Let the interpreter run

    # Show the window and start the app
    form = MainWindow()
    form.show()
    app.exec_()


def startup():
    app = QApplication(sys.argv)
    form = Startup()
    form.show()
    app.exec_()


def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    if QMessageBox.question(None, 'Stopping', "Are you sure you want to quit?",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.No) == QMessageBox.Yes:
        QApplication.quit()

if __name__ == "__main__":
    fileConfig('logging.conf')
    log = logging.getLogger(__name__)
    log.debug("Debugging mode enabled...")
    log.info("osu! Collection Editor starting...")

    main()
