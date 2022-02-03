from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QLockFile
from gui.gui import MainWindow
from gui.toolbar import Toolbar
import sys
from data_handle.database import set_config, remove_log, window_should_open
from globals.globals import Communicate
from download.download import DownloadManager


def show_window():
    global main_win
    if main_win.isHidden() and window_should_open():
        main_win.show()


if __name__ == '__main__':
    lock_file = QLockFile("app.lock")
    is_end = True
    try:
        if lock_file.tryLock():
            signals = Communicate.getInstance()
            signals.lock_file = lock_file
            app = QApplication(sys.argv)
            DownloadManager.init()
            main_win = MainWindow(app)
            timer = QTimer()
            timer.timeout.connect(show_window)
            timer.setInterval(500)
            timer.start()
            toolbar = Toolbar(app, main_win)
            toolbar.show()
            main_win.show()

            sys.exit(app.exec_())
        else:
            is_end = False
            set_config('main_run', True)
            exit(0)
    finally:
        lock_file.unlock()
        remove_log()
