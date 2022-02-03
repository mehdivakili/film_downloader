from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRunnable, QTimer

import data_handle.film_database
from tools.commands import run_film, run_p
from functools import partial
from data_handle import database
from notify import notify


class Notify(QRunnable):
    def __init__(self):
        super().__init__()

    def run(self):
        run_p(notify.main())


class Toolbar:
    def __init__(self, app, main_win):
        self.timer = QTimer()
        self.app = app
        self.menu = QMenu()
        self.main_win = main_win
        self.trayIcon = QSystemTrayIcon(QIcon('icon.ico'))
        self.init_toolbar()

    def handle_click(self, reason: QSystemTrayIcon.ActivationReason):

        if reason == 1:
            self.add_menu()
        elif reason == 3:
            self.main_win.show()
            database.set_config('main_run', True)

    def add_menu(self):
        menu = self.menu
        for a in menu.actions():
            menu.removeAction(a)

        films = data_handle.film_database.get_all()
        for i in films:
            film = films[i]
            if film["is_new"]:
                watch = menu.addAction(f'watch {film["name"]} episode {film["last_episode_watched"] + 1}')
                watch.triggered.connect(
                    partial(run_film, i, film["last_episode_watched"] + 1, film["last_episode_watched"] + 1, True))
        exit_action = menu.addAction('Quit')
        exit_action.triggered.connect(self.quit)

    def quit(self):
        self.main_win.quit()

    def show(self):
        self.trayIcon.show()

    def init_toolbar(self):
        if not database.get_config('toolbar'):
            return
        # database.set_config('notify', True)
        run_p(notify.main)
        self.timer.timeout.connect(partial(run_p, notify.main))
        self.timer.setInterval(1000000)
        self.timer.start()
        self.trayIcon.activated.connect(self.handle_click)
        self.trayIcon.setContextMenu(self.menu)
