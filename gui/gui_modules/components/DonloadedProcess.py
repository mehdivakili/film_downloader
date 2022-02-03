from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton

import data_handle.download_database
from download.download import DownloadManager
from tools import commands


class DownloadedProcessList(QWidget):
    def __init__(self):
        super().__init__()
        self.l = QVBoxLayout()
        self.setLayout(self.l)
        self.set_DownloadedProcess()
        self.timer = QTimer()
        self.timer.timeout.connect(self.set_DownloadedProcess)
        self.timer.setInterval(1000)
        self.timer.start()

    def set_DownloadedProcess(self):
        while self.l.count():
            item = self.l.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.deleteItemsOfLayout(item.layout())
        downloads = data_handle.download_database.get_download_all()
        for directory in downloads:
            self.l.addWidget(DownloadedProcess(directory))


class DownloadedProcess(QWidget):

    def __init__(self, directory):
        super().__init__()
        self.dir = directory
        self.data = data_handle.download_database.get_download(directory)
        self.download = DownloadManager.get_download(directory, self.data["link"])
        self.l = QHBoxLayout()
        self.setLayout(self.l)
        self.initUI()

    def initUI(self):

        self.file_name = self.dir.replace('/', '\\').split('\\')[-1]
        self.text = QLabel(self.file_name)
        self.text.setProperty("cssClass", "download-widget-text")

        self.progressBar = QProgressBar()
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setProperty("cssClass", "download-widget")
        self.set_progress_bar()
        self.btn = QPushButton()
        self.btn.setCursor(Qt.PointingHandCursor)
        if self.download.is_stopped:
            self.btn.setText('resume')
        else:
            self.btn.setText('stop')
        self.btn.setProperty("cssClass", "download-widget")
        self.btn.clicked.connect(self.set_dl_status)

        self.cancel_btn = QPushButton()
        self.cancel_btn.setText("cancel")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.setProperty("cssClass", "download-widget")
        self.cancel_btn.clicked.connect(self.cancel_download)

        self.l.addWidget(self.text)
        self.l.addWidget(self.progressBar)
        self.l.addWidget(self.btn)
        self.l.addWidget(self.cancel_btn)

    def cancel_download(self):
        commands.cancel_download(self.download)

    def set_dl_status(self):
        self.download = DownloadManager.get_download(self.dir)
        if self.download.is_stopped:
            self.download.start(True)
            self.btn.setText("stop")
        else:
            self.download.stop()
            self.btn.setText("resume")

    def set_progress_bar(self):
        self.download = DownloadManager.get_download(self.dir)
        if self.download:
            self.download_percent = int(self.download.dl / DownloadManager.set_download_len(self.dir, 1) * 100)
            self.progressBar.setValue(self.download_percent)
