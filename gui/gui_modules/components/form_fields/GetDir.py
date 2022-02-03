from PyQt5.QtCore import Qt, pyqtSignal, QObject, QUrl
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QDialog


class GetDirSignal(QObject):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()


class GetDir(QWidget):

    def __init__(self):
        super().__init__()
        self.l = QHBoxLayout()
        self.l.setContentsMargins(0, 0, 0, 0)
        self.btn = QPushButton()
        self.dir = QLineEdit()
        self.setAcceptDrops(True)
        self.on_get_file = GetDirSignal()
        self.initUI()
        self.setLayout(self.l)

    def initUI(self):
        self.btn.setProperty("cssClass", "run-widget")
        self.btn.setText("browse")
        self.btn.setFixedWidth(100)
        self.btn.clicked.connect(self.set_dir)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.dir.setProperty("cssClass", "setting-widget")
        # self.dir.setEnabled(False)
        self.l.addWidget(self.dir)
        self.l.addWidget(self.btn)

    def set_dir(self, directory=False):
        if directory is False:
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.DirectoryOnly)
            dialog.setSidebarUrls([QUrl.fromLocalFile('C:\\\\users\\acer\\Downloads\\Video')])
            if dialog.exec_() == QDialog.Accepted and dialog.selectedFiles():
                directory = dialog.selectedFiles()[0]
        if directory:
            self.dir.setText(directory)
            self.on_get_file.signal.emit(directory)

    def get_dir(self):
        return self.dir.text()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ingore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            self.set_dir(event.mimeData().urls()[0].toLocalFile())
