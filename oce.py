import signal
from logging.config import fileConfig, logging

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox

from gui_controller.startup import Startup
from gui_controller.main import MainWindow
import sys

# Version is in the format {release}.{subrelease}{a|b|g}{a,b,g number}
# Where a is alpha, b is beta, g is gamma, nothing is release
# a,b,g number is the number of the alpha/beta/gamma release.
# Releases don't need to have a number, they can just be version 1.0, 2.4, etc.
__version__ = "1.1.2"
__build__ = 103


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

    from settings import Settings
    s = Settings.get_instance()

    try:
        show_dialog = bool(s.get_setting("show_shutdown_dialog", True))
    except ValueError:
        s.set_setting("show_shutdown_dialog", True)
        show_dialog = True

    if show_dialog:
        if QMessageBox.question(None, 'Stopping', "Are you sure you want to quit?",
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No) == QMessageBox.Yes:
            QApplication.quit()
    else:
        QApplication.quit()

if __name__ == "__main__":
    fileConfig('logging.conf')
    log = logging.getLogger(__name__)
    log.debug("Debugging mode enabled...")
    log.info("osu! Collection Editor starting...")

    main()
