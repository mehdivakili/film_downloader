import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QHBoxLayout

import data_handle.film_database
from gui.gui_modules.components.film.FilmTools import FilmTools
from gui.gui_modules.components.film.FilmList import FilmList
from gui.gui_modules.components.film.FilmRun import FilmRun
from gui.gui_modules.components.film.FilmSetting import FilmSetting


class FilmPage(QWidget):
    def __init__(self, film_id):
        super().__init__()
        self.tabs = QTabWidget()
        self.film_id = film_id
        self.film = data_handle.film_database.get_film(film_id)
        self.film_name = self.film["name"]
        self.l = QVBoxLayout()
        self.l.setContentsMargins(0, 0, 0, 0)
        self.l.setAlignment(Qt.AlignTop)
        self.setLayout(self.l)
        self.initUI()

    def initUI(self):
        self.title = QLabel(self.film_name)
        self.title.setAlignment(Qt.AlignHCenter)
        self.title = QLabel(self.film_name)
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        # self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.title.setProperty('cssClass', 'film-title')

        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        self.run_layout = QVBoxLayout()
        self.run_layout.setAlignment(Qt.AlignTop)

        self.setting_layout = QVBoxLayout()
        self.setting_layout.setAlignment(Qt.AlignTop)

        self.icon = QLabel(self)
        pixmap = QPixmap(self.film['icon'])
        self.icon.setObjectName('icon')
        self.icon.setStyleSheet(f"border-image: url('{self.film['icon']}')")
        self.icon.setFixedSize(350, 350 * pixmap.height() / pixmap.width())

        w_run = QWidget()
        self.run_layout.addWidget(self.icon)
        self.run_layout.addWidget(FilmRun(self.film_id))
        self.main_layout.addWidget(FilmList(self.film_id))
        self.main_layout.addLayout(self.run_layout)
        w_run.setLayout(self.main_layout)

        self.tabs.setObjectName("film-page-tab")
        self.tabs.setProperty("cssClass", "film-page-tab")
        self.tabs.addTab(w_run, qta.icon('fa5s.play', color='white', scale_factor=1.1, rotated=90), "")
        self.tabs.addTab(FilmSetting(self.film_id), qta.icon('fa5s.pen', color='white', scale_factor=1.1, rotated=90),
                         "")
        self.tabs.addTab(FilmTools(self.film_id), qta.icon('fa5s.wrench', color='white', scale_factor=1.1, rotated=90),
                         "")
        self.tabs.setTabPosition(QTabWidget.West)

        self.bar_back = QWidget()
        self.bar_back.setParent(self)
        self.bar_back.setStyleSheet("background: #34495e;")
        self.bar_back.setFixedSize(62, 10000)
        self.bar_back.move(0, 0)
        self.l.addWidget(self.title)
        # self.tabs.setCornerWidget(self.title)
        self.l.addWidget(self.tabs)