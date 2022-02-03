from time import sleep

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

import data_handle.film_database
from globals.globals import Communicate
from tools import commands


class MustWatchList(QWidget):
    def __init__(self):
        super().__init__()
        self.l = QVBoxLayout()
        self.setLayout(self.l)
        self.set_MustWatched()
        self.timer = QTimer()
        self.timer.timeout.connect(self.set_MustWatched)
        self.timer.setInterval(1000)
        self.timer.start()

    def set_MustWatched(self):
        while self.l.count():
            item = self.l.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.deleteItemsOfLayout(item.layout())
        films = data_handle.film_database.get_all()
        for i in films:
            f = films[i]
            if f["is_new"]:
                self.l.addWidget(MustWatch(i))


class MustWatch(QWidget):
    def __init__(self, film_id):
        super().__init__()
        self.film_id = film_id
        self.film = data_handle.film_database.get_film(film_id)
        self.episode = self.film["last_episode_watched"] + 1
        self.l = QHBoxLayout()
        self.initUI()
        self.setLayout(self.l)

    def run(self):
        commands.run_film(self.film_id, self.episode, self.episode, True)
        sleep(0.1)
        signal = Communicate.getInstance()
        signal.menu_refresh.emit()
        signal.page_changing[str, str, bool].emit('film', str(self.film_id), True)

    def initUI(self):
        self.btn = QPushButton()
        self.text = QLabel(f"the episode {self.episode} of {self.film['name']} has been released")
        self.text.setProperty("cssClass", "watched-widget-text")
        self.text.setAlignment(Qt.AlignCenter)
        self.btn.setProperty("cssClass", "watched-widget")
        self.text.setAlignment(Qt.AlignCenter)
        self.btn.setText("watch")
        self.btn.setFixedWidth(150)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.clicked.connect(self.run)
        self.l.addWidget(self.btn)
        self.l.addWidget(self.text)
        self.l.setAlignment(Qt.AlignTop)
