from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit

from globals.globals import Communicate
from data_handle import database


class LogArea(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = Communicate.getInstance()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 30, 0, 0)
        self.logs = []
        self.new_logs = []
        self.logOutput = QTextEdit()
        self.initUI()
        self.refresh_logs()
        self.signals.log_changed.connect(self.refresh_logs)
        self.setLayout(self.layout)

    def initUI(self):
        self.logOutput.setReadOnly(True)
        self.logOutput.setAutoFillBackground(False)
        font = self.logOutput.font()
        font.setFamily("Courier")
        font.setPointSize(10)

        self.layout.addWidget(self.logOutput)

    def refresh_logs(self):
        self.new_logs = database.get_log()
        if len(self.new_logs) != len(self.logs):
            diff = len(self.new_logs) - len(self.logs)
            self.logs = self.new_logs
            c = self.logOutput.textCursor()
            c.movePosition(QTextCursor.End)
            self.logOutput.setTextCursor(c)
            for i in range(-diff, 0):
                self.logOutput.insertPlainText(self.logs[i] + '\n')

            c = self.logOutput.textCursor()
            c.movePosition(QTextCursor.End)
            self.logOutput.setTextCursor(c)
