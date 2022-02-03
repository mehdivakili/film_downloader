from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QListWidget, QVBoxLayout, QListWidgetItem, QHBoxLayout, QLabel

import data_handle.film_database
from download.download import check_files_downloaded
from globals.globals import Communicate
from run.run import run_without_download
from tools import commands


class FilmList(QWidget):
    def __init__(self, film_id):
        super().__init__()
        self.see_all_btn = QPushButton()
        self.signals = Communicate.getInstance()
        self.film_id = film_id
        self.film = data_handle.film_database.get_film(film_id)
        self.max = self.film["last_episode_watched"] + 1
        self.min = 0
        self.list = QListWidget()
        self.list_layout = QVBoxLayout()
        self.setLayout(self.list_layout)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.min_lim = self.min
        if self.film["last_episode_watched"] - 15 > self.min_lim:
            self.min_lim = self.film["last_episode_watched"] - 15
        for i in range(self.max, self.min_lim, -1):
            item = FilmListItem(film_id, i)
            item_list = QListWidgetItem(self.list)
            item_list.setSizeHint(item.sizeHint())
            self.list.addItem(item_list)
            self.list.setItemWidget(item_list, item)

        self.initUI()

    def initUI(self):
        self.list.setObjectName("film-list")
        self.list.setSpacing(5)
        self.list_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.list_layout.setContentsMargins(0, 0, 0, 0)

        self.list_layout.addWidget(self.list)

        if self.min_lim != self.min:
            self.see_all_btn.setText("see all")
            self.see_all_btn.setObjectName('apply-btn')
            self.see_all_btn.clicked.connect(self.see_all)
            self.see_all_btn.setCursor(Qt.PointingHandCursor)

            self.list_layout.addWidget(self.see_all_btn)

    def see_all(self):
        self.see_all_btn.deleteLater()
        self.see_all_btn.setParent(None)
        for i in range(self.min_lim, self.min, -1):
            item = FilmListItem(self.film_id, i)
            item_list = QListWidgetItem(self.list)
            item_list.setSizeHint(item.sizeHint())
            self.list.addItem(item_list)
            self.list.setItemWidget(item_list, item)
            self.signals.run_app()


class FilmListItem(QWidget):
    def __init__(self, film_id, episode):
        super().__init__()
        self.item_layout = QHBoxLayout()
        self.film_id = film_id
        self.episode = episode
        self.film = data_handle.film_database.get_film(film_id)
        self.dir = self.film["directory"].format(episode) + '.mkv'
        self.initUI()
        self.setLayout(self.item_layout)

    def initUI(self):
        self.title = QLabel(f'episode {self.episode}')
        self.title.setProperty("cssClass", 'film-list-item-title')

        self.icon = QLabel(self)
        pixmap = QPixmap(self.film['icon'])
        self.icon.setStyleSheet(f"border-image: url('{self.film['icon']}');border-radius: 5px;")
        self.icon.setFixedSize(60 * pixmap.width() / pixmap.height(), 60)

        self.content_layout = QVBoxLayout()

        self.tool_layout = QHBoxLayout()

        self.run_btn = QPushButton()
        self.run_btn.setText("watch")
        self.run_btn.setProperty("cssClass", "run-widget")
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.clicked.connect(self.run)
        self.run_btn.setFixedWidth(100)

        self.run_no_dl_btn = QPushButton()
        self.run_no_dl_btn.setText("watch no dl")
        self.run_no_dl_btn.setProperty("cssClass", "run-widget")
        self.run_no_dl_btn.setCursor(Qt.PointingHandCursor)
        self.run_no_dl_btn.clicked.connect(self.run_without_download)
        self.run_no_dl_btn.setFixedWidth(100)

        if check_files_downloaded(self.film["directory"], self.episode):
            # self.info = f'duration: {get_human_readable_length(self.dir)} minute   size:{int(os.path.getsize(self.dir) >> 20)}MB'
            self.info = 'film is ready to watch'
        else:
            self.info = "film not downloaded"
        self.info_label = QLabel(self.info)
        self.info_label.setProperty("cssClass", "setting-widget-text")
        self.tool_layout.addWidget(self.info_label)

        self.content_layout.addWidget(self.title)
        self.content_layout.addLayout(self.tool_layout)

        self.item_layout.addWidget(self.icon)
        self.item_layout.addLayout(self.content_layout)
        self.item_layout.addWidget(self.run_btn)
        self.item_layout.addWidget(self.run_no_dl_btn)

    def run(self):
        commands.run_film(self.film_id, self.episode, 9999)

    def run_without_download(self):
        run_without_download(self.film_id, self.episode)