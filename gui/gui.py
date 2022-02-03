from PyQt5.QtWidgets import (QMainWindow, QApplication, QScrollArea, QVBoxLayout, QHBoxLayout, QWidget)
from PyQt5.QtGui import QIcon

import data_handle.film_database
import sys
from data_handle import database
from PyQt5.QtCore import QLockFile
from globals.globals import Communicate
from gui.gui_modules.components.Menus import Menus
from gui.gui_modules.pages.AddFilmPage import AddFilmPage
from gui.gui_modules.pages.FilmArchivePage import FilmArchivePage
from gui.gui_modules.pages.SettingPage import SettingPage
from gui.gui_modules.pages.FilmPage import FilmPage
from gui.gui_modules.pages.HomePage import HomePage


class MainWindow(QMainWindow):

    def __init__(self, app):

        super().__init__()
        self.pages = {}
        self.menu = Menus()
        self.content = QVBoxLayout()
        self.scroll = QScrollArea()
        self.main_view = QHBoxLayout()
        self.app = app
        self.signals = Communicate.getInstance()

        self.initUI()

    def initUI(self):

        self.setGeometry(100, 50, 1280, 800)
        self.setWindowTitle('Anime downloader')
        self.setWindowIcon(QIcon('./icon.ico'))
        w = QWidget()

        self.main_view.setContentsMargins(0, 0, 0, 0)
        self.main_view.setSpacing(0)
        w.setLayout(self.main_view)

        self.setCentralWidget(w)

        self.signals.page_changing[str, str].connect(self.change_page)
        self.signals.page_changing[str, str, bool].connect(self.change_page)

        self.main_view.addLayout(self.content)
        self.main_view.addWidget(self.menu)

        self.add_all_pages(self.pages)
        self.hide_all_pages(self.pages)

        self.add_home_page()
        self.add_options()

        with open('gui/styles/style.qss') as s:
            style = s.read()
            self.setStyleSheet(style)

    def add_options(self):
        pass

    def change_page(self, page_name, arg, refresh=False):
        self.hide_all_pages(self.pages)

        if page_name == 'film':
            self.add_film_page(arg, refresh=refresh)
            self.menu.set_menu_rows(data_handle.film_database.get_film_row(arg), -1)
            self.signals.option_click.emit()
        elif page_name == 'home':
            self.add_home_page(refresh=refresh)
            self.menu.set_menu_rows(-1, 0)
        elif page_name == 'setting':
            self.add_setting_page(refresh=refresh)
            self.menu.set_menu_rows(-1, 1)
        elif page_name == 'add film':
            self.add_add_film_page(refresh=refresh)
            self.menu.set_menu_rows(-1, 2)
        elif page_name == 'restore film':
            self.add_restore_film_page(refresh=refresh)
            self.menu.set_menu_rows(-1, 2)
        self.add_options()

    def add_film_page(self, film_id, refresh=False):
        if "films" not in self.pages.keys():
            self.pages["films"] = {}
        if film_id not in self.pages["films"].keys():
            self.pages["films"][film_id] = FilmPage(film_id)
            self.content.addWidget(self.pages["films"][film_id])
        elif refresh:
            self.pages["films"][film_id].setParent(None)
            self.pages["films"][film_id].deleteLater()
            self.pages["films"][film_id] = FilmPage(film_id)
            self.content.addWidget(self.pages["films"][film_id])
            if self.pages["films"][film_id].isHidden():
                self.pages["films"][film_id].show()
        else:
            self.pages["films"][film_id].show()

    def add_home_page(self, refresh=False):
        if "home" not in self.pages.keys() or refresh:
            self.pages["home"] = HomePage()
            self.content.addWidget(self.pages["home"])
        else:
            self.pages["home"].show()

    def add_setting_page(self, refresh=False):
        if "setting" not in self.pages.keys() or refresh:
            self.pages["setting"] = SettingPage()
            self.content.addWidget(self.pages["setting"])
        else:
            self.pages["setting"].show()

    def add_add_film_page(self, refresh=False):
        if "add" not in self.pages.keys() or refresh:
            self.pages["add"] = AddFilmPage()
            self.content.addWidget(self.pages["add"])
        else:
            self.pages["add"].show()

    def add_restore_film_page(self, refresh=False):
        if "restore" not in self.pages.keys() or refresh:
            self.pages["restore"] = FilmArchivePage()
            self.content.addWidget(self.pages["restore"])
        else:
            self.pages["restore"].show()

    def closeEvent(self, event):
        if __name__ == '__main__':
            return event.accept()

        event.ignore()
        self.hide()
        database.set_config('main_run', False)

    def quit(self):
        database.set_config("main_run", True)
        self.app.quit()

    def hide_all_pages(self, pages):
        for page in pages:
            page = pages[page]
            if isinstance(page, QWidget):
                if not page.isHidden():
                    page.hide()
            else:
                self.hide_all_pages(page)

    def add_all_pages(self, pages):
        for page in pages:
            page = pages[page]
            if isinstance(page, QWidget):
                self.content.addWidget(page)
            else:
                self.add_all_pages(page)


def main():
    lock_file = QLockFile("../app.lock")
    try:
        lock_file.tryLock()
        database.log('test log')
        app = QApplication(sys.argv)
        ex = MainWindow(app)
        ex.show()
        sys.exit(app.exec_())
    finally:
        lock_file.unlock()
        database.remove_log()


if __name__ == '__main__':
    main()
