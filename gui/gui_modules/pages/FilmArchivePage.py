from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea

import data_handle.film_archived_database
from gui.gui_modules.components.film.FilmArchiveCard import FilmArchiveCard


class FilmArchivePage(QWidget):
    def __init__(self):
        super().__init__()
        self.films = data_handle.film_archived_database.get_all_archived()
        self.l = QVBoxLayout()
        self.w = QWidget()
        self.scrollbar = QScrollArea()
        self.scrollbar.setProperty('cssClass', 'scroll')
        self.scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollbar.setWidgetResizable(True)
        self.l.setContentsMargins(0, 0, 0, 0)
        self.l.setAlignment(Qt.AlignTop)
        self.w.setLayout(self.l)
        self.m = QVBoxLayout()
        self.m.setContentsMargins(0, 0, 0, 0)

        self.initUI()
        self.m.addWidget(self.scrollbar)
        self.setLayout(self.m)


    def initUI(self):
        self.title = QLabel("archived films")
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title.setProperty('cssClass', 'film-title')

        self.main_layout = QGridLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        i = j = 0
        for id in self.films:
            film = self.films[id]
            film_card = FilmArchiveCard(id, film)
            self.main_layout.addWidget(film_card, i, j)
            j += 1
            if (j) % 3 == 0:
                i += 1
                j = 0

        self.scrollbar.setWidget(self.w)
        self.m.addWidget(self.title)
        self.l.addLayout(self.main_layout)
