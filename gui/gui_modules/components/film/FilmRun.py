from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSpinBox, QAbstractSpinBox

import data_handle.film_database
from data_handle import database
from gui.gui_modules.helpers import deleteItemsOfLayout
from run.run import kill_video_player
from tools import commands


class FilmRun(QWidget):
    def __init__(self, film_id):
        super().__init__()
        self.film_id = film_id
        self.film = data_handle.film_database.get_film(film_id)
        self.run_layout = QVBoxLayout()
        self.initUI()
        self.setLayout(self.run_layout)
        self.run_layout.setContentsMargins(0, 0, 0, 0)

    def initUI(self):
        self.show_run()

    def show_run(self):
        deleteItemsOfLayout(self.run_layout)
        self.run_last_episode_btn = QPushButton()
        self.run_last_episode_btn.setText("play last episode")
        self.run_last_episode_btn.setProperty("cssClass", "run-widget")
        self.run_last_episode_btn.clicked.connect(self.run_last_episode)
        self.run_last_episode_btn.setCursor(Qt.PointingHandCursor)

        self.run_from_layout = QHBoxLayout()
        self.run_from_btn = QPushButton()
        self.download_from_btn = QPushButton()
        self.run_from_btn.setText("play from")
        self.run_from_btn.setProperty("cssClass", "run-widget")
        self.run_from_btn.setCursor(Qt.PointingHandCursor)
        self.run_from_btn.clicked.connect(self.run_from)

        self.download_from_btn.setText("dl from")
        self.download_from_btn.setProperty("cssClass", "run-widget")
        self.download_from_btn.setCursor(Qt.PointingHandCursor)
        self.download_from_btn.clicked.connect(self.download_from)

        self.run_from_input = QSpinBox()
        self.run_from_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.run_from_input.setProperty("cssClass", "run-widget")
        self.run_from_input.setMaximum(9999)

        self.run_episode_layout = QHBoxLayout()
        self.run_episode_btn = QPushButton()
        self.download_episode_btn = QPushButton()
        self.run_episode_btn.setText("play episode")
        self.run_episode_btn.setProperty("cssClass", "run-widget")
        self.run_episode_btn.clicked.connect(self.run_episode)
        self.run_episode_btn.setCursor(Qt.PointingHandCursor)
        self.download_episode_btn.setText("dl episode")
        self.download_episode_btn.setProperty("cssClass", "run-widget")
        self.download_episode_btn.clicked.connect(self.download_episode)
        self.download_episode_btn.setCursor(Qt.PointingHandCursor)
        self.run_episode_input = QSpinBox()
        self.run_episode_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.run_episode_input.setProperty("cssClass", "run-widget")
        self.run_episode_input.setMaximum(9999)

        self.run_l = QHBoxLayout()
        self.run_btn = QPushButton()
        self.download_btn = QPushButton()
        self.run_btn.setText("play")
        self.run_btn.setProperty("cssClass", "run-widget")
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.clicked.connect(self.run)
        self.download_btn.setText("download")
        self.download_btn.setProperty("cssClass", "run-widget")
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.clicked.connect(self.download)
        self.run_start_input = QSpinBox()
        self.run_start_input.setMaximum(9999)
        self.run_start_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.run_start_input.setProperty("cssClass", "run-widget")
        self.run_end_input = QSpinBox()
        self.run_end_input.setMaximum(9999)
        self.run_end_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.run_end_input.setProperty("cssClass", "run-widget")

        self.run_episode_layout.addWidget(self.download_episode_btn)
        self.run_episode_layout.addWidget(self.run_episode_btn)
        self.run_episode_layout.addWidget(self.run_episode_input)

        self.run_from_layout.addWidget(self.download_from_btn)
        self.run_from_layout.addWidget(self.run_from_btn)
        self.run_from_layout.addWidget(self.run_from_input)

        self.run_l.addWidget(self.download_btn)
        self.run_l.addWidget(self.run_btn)
        self.run_l.addWidget(self.run_start_input)
        self.run_l.addWidget(self.run_end_input)

        self.run_layout.addWidget(self.run_last_episode_btn)
        self.run_layout.addLayout(self.run_episode_layout)
        self.run_layout.addLayout(self.run_from_layout)
        self.run_layout.addLayout(self.run_l)

    def run_last_episode(self):
        if self.film["is_new"]:
            commands.run_film(self.film_id, self.film["last_episode_watched"] + 1,
                              self.film["last_episode_watched"] + 1)
        else:
            commands.run_film(self.film_id, self.film["last_episode_watched"], self.film["last_episode_watched"])

        # self.show_kill()

    def run_episode(self):
        episode = int(self.run_episode_input.value())
        commands.run_film(self.film_id, episode, episode)
        self.show_kill()

    def run_from(self):
        start = int(self.run_from_input.value())
        commands.run_film(self.film_id, start)
        # self.show_kill(True)

    def run(self):
        start = int(self.run_start_input.value())
        end = int(self.run_end_input.value())
        commands.run_film(self.film_id, start, end)
        # self.show_kill(True)

    def download_episode(self):
        episode = int(self.run_episode_input.value())
        commands.run_film(self.film_id, episode, episode, False)
        # self.show_kill()

    def download_from(self):
        start = int(self.run_from_input.value())
        commands.run_film(self.film_id, start, is_play=False)
        # self.show_kill(True)

    def download(self):
        start = int(self.run_start_input.value())
        end = int(self.run_end_input.value())
        commands.run_film(self.film_id, start, end, False)
        # self.show_kill(True)

    def show_kill(self, is_con=False):
        deleteItemsOfLayout(self.run_layout)
        if is_con or database.get_config("run"):
            self.kill_btn = QPushButton()
            self.kill_btn.setProperty("cssClass", "run-widget")
            self.kill_btn.setText("ignore watching next episode")
            self.kill_btn.clicked.connect(self.kill_film)
            self.run_layout.addWidget(self.kill_btn
                                      )
        self.kill_video_player_btn = QPushButton()
        self.kill_video_player_btn.setProperty("cssClass", "run-widget")
        self.kill_video_player_btn.setText("stop watching")
        self.kill_video_player_btn.clicked.connect(partial(self.kill_film, True))
        self.run_layout.addWidget(self.kill_video_player_btn)

    def kill_film(self, kill_vid=False):
        commands.kill_film()
        if kill_vid:
            kill_video_player()
        deleteItemsOfLayout(self.run_layout)
        self.show_run()