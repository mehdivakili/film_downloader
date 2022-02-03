from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal


class Communicate(QObject):
    __instance = None
    page_changing = pyqtSignal([str, str], [str, str, bool])
    menu_refresh = pyqtSignal()
    option_click = pyqtSignal()
    log_changed = pyqtSignal()
    lock_file = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Communicate.__instance is None:
            Communicate()
        return Communicate.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Communicate.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            super().__init__()
            Communicate.__instance = self

    @staticmethod
    def run_app():
        QtCore.QCoreApplication.processEvents()
