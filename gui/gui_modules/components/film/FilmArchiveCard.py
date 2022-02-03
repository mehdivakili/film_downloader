from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

import data_handle.film_archived_database
from globals.globals import Communicate


class FilmArchiveCard(QWidget):
    def __init__(self, film_id, film):
        super().__init__()
        self.l = QVBoxLayout()
        self.film_id = film_id
        self.film = film
        self.initUi()
        self.setLayout(self.l)
        self.signals = Communicate.getInstance()

    def initUi(self):
        self.title = QLabel(self.film["name"])
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title.setProperty('cssClass', 'film-title')

        self.icon = QLabel(self)
        # pixmap = QPixmap(self.film['icon'])
        self.icon.setObjectName('icon')
        self.icon.setStyleSheet(f"border-image: url('{self.film['icon']}')")
        self.icon.setFixedHeight(200)

        self.restore_btn = QPushButton()
        self.restore_btn.setText("restore")
        self.restore_btn.setObjectName('apply-btn')
        self.restore_btn.clicked.connect(self.restore)
        self.restore_btn.setCursor(Qt.PointingHandCursor)

        self.delete_btn = QPushButton()
        self.delete_btn.setText("delete")
        self.delete_btn.setObjectName('delete-btn')
        self.delete_btn.clicked.connect(self.delete)
        self.delete_btn.setCursor(Qt.PointingHandCursor)

        self.l.addWidget(self.icon)
        self.l.addWidget(self.title)
        self.l.addWidget(self.restore_btn)
        self.l.addWidget(self.delete_btn)

    def restore(self):
        data_handle.film_archived_database.restore_film(self.film_id)
        self.signals.page_changing[str, str, bool].emit("restore film", '', True)
        self.signals.menu_refresh.emit()

    def delete(self):
        data_handle.film_archived_database.delete_archived_film(self.film_id)
        self.signals.page_changing[str, str, bool].emit("restore film", '', True)
