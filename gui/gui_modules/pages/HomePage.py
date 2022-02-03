from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from gui.gui_modules.components.DonloadedProcess import DownloadedProcessList
from gui.gui_modules.components.MustWatch import MustWatchList


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.home_layout = QVBoxLayout()
        self.watched_layout = QVBoxLayout()
        self.watched_layout.setObjectName('watched')
        self.watched_layout.setAlignment(Qt.AlignTop)
        self.download_layout = QVBoxLayout()
        self.download_layout.setAlignment(Qt.AlignTop)
        title = QLabel("new episodes")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("new-episodes-title")
        self.watched_layout.addWidget(title)
        self.watched_layout.addWidget(MustWatchList())

        title2 = QLabel("downloads")
        title2.setAlignment(Qt.AlignCenter)
        title2.setObjectName("downloads-title")
        self.download_layout.addWidget(title2)
        self.download_layout.addWidget(DownloadedProcessList())

        self.home_layout.addLayout(self.watched_layout)
        self.home_layout.addLayout(self.download_layout)
        self.setLayout(self.home_layout)