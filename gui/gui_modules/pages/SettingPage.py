from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout

from gui.gui_modules.components.form_fields.MultyLineEdit import MultiLineEdit
from gui.gui_modules.components.form_fields.LogArea import LogArea

from data_handle import database
from tools.commands import checkNotify


class SettingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.apply_setting_btn = QPushButton()
        self.notify_layout = QHBoxLayout()
        self.notify_btn = QPushButton()
        self.notify_input = QCheckBox()
        self.notify_label = QLabel("notify")
        self.wifi_inputs = MultiLineEdit()
        self.wifi_label = QLabel("trusted wifi")
        self.video_input = QLineEdit()
        self.video_label = QLabel("video player")
        self.proxy_input = QLineEdit()
        self.proxy_label = QLabel("proxy")
        self.title = QLabel("setting")
        self.log_area = LogArea()
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.initUI()
        self.setLayout(self.main_layout)

    def initUI(self):

        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setProperty('cssClass', 'film-title')

        self.proxy_label.setProperty("cssClass", "setting-widget-text")
        self.proxy_input.setProperty("cssClass", "setting-widget")
        if database.get_proxy():
            self.proxy_input.setText(database.get_proxy().get("http"))

        self.video_label.setProperty("cssClass", "setting-widget-text")
        self.video_input.setProperty("cssClass", "setting-widget")
        if database.get_config("video_player"):
            self.video_input.setText(database.get_config("video_player"))

        self.wifi_label.setProperty("cssClass", "setting-widget-text")

        wifis = database.get_config("trusted_wifi")
        for i in range(len(wifis)):
            self.wifi_inputs.addItem(wifis[i])

        self.notify_label.setProperty("cssClass", "setting-checkbox-widget-text")
        self.notify_input.setProperty("cssClass", "setting-checkbox-widget")
        self.notify_input.setChecked(database.get_config("notify"))

        self.notify_btn.setText("check updates now")
        self.notify_btn.setProperty("cssClass", "run-widget")
        self.notify_btn.setCursor(Qt.PointingHandCursor)
        self.notify_btn.clicked.connect(checkNotify)
        self.notify_btn.setFixedWidth(200)

        self.notify_layout.addWidget(self.notify_label)
        self.notify_layout.addWidget(self.notify_input)
        self.notify_layout.addWidget(self.notify_btn)

        self.apply_setting_btn.setText("apply")
        self.apply_setting_btn.setObjectName('apply-btn')
        self.apply_setting_btn.clicked.connect(self.apply_setting)
        self.apply_setting_btn.setFixedWidth(100)
        self.apply_setting_btn.setCursor(Qt.PointingHandCursor)

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.proxy_label)
        self.main_layout.addWidget(self.proxy_input)
        self.main_layout.addWidget(self.video_label)
        self.main_layout.addWidget(self.video_input)
        self.main_layout.addWidget(self.wifi_label)
        self.main_layout.addWidget(self.wifi_inputs)
        self.main_layout.addLayout(self.notify_layout)
        self.main_layout.addWidget(self.apply_setting_btn)
        self.main_layout.addWidget(self.log_area)

    def apply_setting(self):
        proxy = False
        if self.proxy_input.text():
            proxy = {
                "http": self.proxy_input.text()
            }
        wifis = self.wifi_inputs.get_all()

        notify = self.notify_input.isChecked()

        database.set_config("notify", notify)
        if proxy:
            database.set_config("proxy", proxy)
        database.set_config("trusted_wifi", wifis)
        if self.video_input.text():
            database.set_config("video_player", self.video_input.text())
