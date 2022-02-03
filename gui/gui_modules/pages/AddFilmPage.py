from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from gui.gui_modules.components.film.FilmSetting import FilmSetting


class AddFilmPage(QWidget):
    def __init__(self):
        super().__init__()
        self.title = QLabel("add film")
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.main_layout)
        self.initUI()

    def initUI(self):
        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setProperty('cssClass', 'film-title')

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(FilmSetting())
