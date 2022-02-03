from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QAbstractSpinBox, QHBoxLayout, QCheckBox, \
    QPushButton, QScrollArea

import data_handle.film_database
from globals.globals import Communicate
from gui.gui_modules.components.form_fields.DayCheckbox import DayCheckbox
from gui.gui_modules.components.form_fields.GetDir import GetDir
from gui.gui_modules.components.form_fields.MultiDoubleTextArea import MultiDoubleTextArea
from gui.gui_modules.components.form_fields.GetFile import GetFile
from tools.commands import checkNotify


class FilmSetting(QWidget):
    def __init__(self, film_id=None):
        super().__init__()
        self.signals = Communicate.getInstance()
        self.film_id = film_id
        if film_id:
            self.apply_func = self.change_film_setting
            self.film = data_handle.film_database.get_film(film_id)
        else:
            self.apply_func = self.add_film
            self.film = {
                "name": "",
                "video": [],
                "subtitle": [],
                "directory": "",
                "last_episode_watched": 0,
                "notified": False,
                "notify_days": [],
                "is_new": False,
                "icon": "images/icon.png"
            }
        self.w = QWidget()
        self.scrollbar = QScrollArea()
        self.scrollbar.setProperty('cssClass', 'scroll')
        self.scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollbar.setWidgetResizable(True)
        self.scrollbar.setWidget(self.w)

        self.main_layout = QVBoxLayout()
        self.w.setLayout(self.main_layout)
        self.m = QVBoxLayout()
        self.m.setContentsMargins(0, 0, 0, 0)
        self.initUI()
        self.m.addWidget(self.scrollbar)
        self.setLayout(self.m)

    def initUI(self):
        self.name_lable = QLabel("film name")
        self.name_lable.setProperty("cssClass", "setting-widget-text")
        self.name_input = QLineEdit()
        self.name_input.setProperty("cssClass", "setting-widget")
        self.name_input.setText(self.film["name"])

        self.icon_lable = QLabel("film icon")
        self.icon_lable.setProperty("cssClass", "setting-widget-text")
        self.icon_input = GetFile()
        # self.icon_input.setProperty("cssClass", "setting-widget")
        self.icon_input.set_dir(self.film["icon"])

        self.video_link_lable = QLabel("video link")
        self.video_link_lable.setProperty("cssClass", "setting-widget-text")
        # self.video_link_input = QLineEdit()
        # self.video_link_input.setProperty("cssClass", "setting-widget")
        # self.video_link_input.setText(self.film["video_link"])
        self.video_link_input = MultiDoubleTextArea("link", "query")
        for v in self.film["video"]:
            self.video_link_input.addItem(v)

        self.subtitle_link_lable = QLabel("subtitle link")
        self.subtitle_link_lable.setProperty("cssClass", "setting-widget-text")
        # self.subtitle_link_input = QLineEdit()
        # self.subtitle_link_input.setProperty("cssClass", "setting-widget")
        # self.subtitle_link_input.setText(self.film["subtitle_link"])
        self.subtitle_link_input = MultiDoubleTextArea("link", "query")
        for v in self.film["subtitle"]:
            self.subtitle_link_input.addItem(v)

        # self.subtitle_query_lable = QLabel("subtitle query")
        # self.subtitle_query_lable.setProperty("cssClass", "setting-widget-text")
        # self.subtitle_query_input = QLineEdit()
        # self.subtitle_query_input.setProperty("cssClass", "setting-widget")
        # self.subtitle_query_input.setText(self.film["subtitle_query"])

        self.directory_lable = QLabel("directory")
        self.directory_lable.setProperty("cssClass", "setting-widget-text")
        self.directory_input = GetDir()
        # self.directory_input.setProperty("cssClass", "setting-widget")
        self.directory_input.set_dir(self.film["directory"])

        self.episode_lable = QLabel("last episode watched")
        self.episode_lable.setProperty("cssClass", "setting-widget-episode-text")
        self.episode_input = QSpinBox()
        self.episode_input.setProperty("cssClass", "setting-widget")
        self.episode_input.setMaximum(9999)
        self.episode_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.episode_input.setValue(self.film["last_episode_watched"])

        self.episode_layout = QHBoxLayout()
        self.episode_layout.addWidget(self.episode_lable)
        self.episode_layout.addWidget(self.episode_input)

        self.notified_lable = QLabel("notified")
        self.notified_lable.setProperty("cssClass", "setting-checkbox-widget-text")
        self.notified_input = QCheckBox()
        self.notified_input.setProperty("cssClass", "setting-checkbox-widget")
        self.notified_input.setChecked(self.film["notified"])

        self.notified_layout = QHBoxLayout()
        self.notified_layout.addWidget(self.notified_lable)
        self.notified_layout.addWidget(self.notified_input)

        self.notify_days_lable = QLabel("notify days")
        self.notify_days_lable.setProperty("cssClass", "setting-checkbox-widget-text")
        self.notify_days_input = DayCheckbox()
        # self.notify_days_input.setProperty("cssClass", "setting-checkbox-widget")
        self.notify_days_input.set_days(self.film["notify_days"])

        self.notify_days_layout = QHBoxLayout()
        self.notify_days_layout.addWidget(self.notify_days_lable)
        self.notify_days_layout.addWidget(self.notify_days_input)

        self.apply_setting_btn = QPushButton()
        self.apply_setting_btn.setText("apply")
        self.apply_setting_btn.setObjectName('apply-btn')
        self.apply_setting_btn.clicked.connect(self.apply_func)
        self.apply_setting_btn.setFixedWidth(100)
        self.apply_setting_btn.setCursor(Qt.PointingHandCursor)

        self.main_layout.addWidget(self.name_lable)
        self.main_layout.addWidget(self.name_input)
        self.main_layout.addWidget(self.icon_lable)
        self.main_layout.addWidget(self.icon_input)
        self.main_layout.addWidget(self.video_link_lable)
        self.main_layout.addWidget(self.video_link_input)
        self.main_layout.addWidget(self.subtitle_link_lable)
        self.main_layout.addWidget(self.subtitle_link_input)
        # self.main_layout.addWidget(self.subtitle_query_lable)
        # self.main_layout.addWidget(self.subtitle_query_input)
        self.main_layout.addWidget(self.directory_lable)
        self.main_layout.addWidget(self.directory_input)
        self.main_layout.addLayout(self.episode_layout)
        self.main_layout.addLayout(self.notified_layout)
        self.main_layout.addLayout(self.notify_days_layout)
        self.main_layout.addWidget(self.apply_setting_btn)

    def add_film(self):
        name = self.name_input.text()
        icon = self.icon_input.get_dir()
        video_link = self.video_link_input.get_all()
        for v in range(len(video_link)):
            video_link[v]["offset"] = 0

        subtitle_link = self.subtitle_link_input.get_all()
        for v in range(len(subtitle_link)):
            subtitle_link[v]["offset"] = 0

        directory = self.directory_input.get_dir()
        episode = self.episode_input.value()
        notified = self.notified_input.isChecked()
        notify_days = self.notify_days_input.get_days()

        f = self.film

        f["name"] = name
        f["icon"] = icon
        f["video"] = video_link
        f["subtitle"] = subtitle_link
        f["directory"] = directory
        f["last_episode_watched"] = episode
        f["notified"] = notified
        f["notify_days"] = notify_days
        film_id = data_handle.film_database.add_film(f)
        self.signals.menu_refresh.emit()
        self.signals.page_changing.emit('film', str(film_id))
        checkNotify()

    def change_film_setting(self):
        name = self.name_input.text()
        icon = self.icon_input.get_dir()
        video_link = self.video_link_input.get_all()
        for v in range(len(video_link)):
            video_link[v]["offset"] = 0
            if self.film['video'][v].get('offset'):
                video_link[v]["offset"] = self.film['video'][v].get('offset')

        subtitle_link = self.subtitle_link_input.get_all()
        for v in range(len(subtitle_link)):
            subtitle_link[v]["offset"] = 0
            if self.film['subtitle'][v].get('offset'):
                subtitle_link[v]["offset"] = self.film['subtitle'][v].get('offset')
        directory = self.directory_input.get_dir()
        episode = self.episode_input.value()
        notified = self.notified_input.isChecked()
        notify_days = self.notify_days_input.get_days()

        f = data_handle.film_database.get_film(self.film_id)

        f["name"] = name
        f["icon"] = icon
        f["video"] = video_link
        f["subtitle"] = subtitle_link
        f["directory"] = directory
        f["last_episode_watched"] = episode
        f["notified"] = notified
        f["notify_days"] = notify_days

        data_handle.film_database.set_film(self.film_id, f)

        self.signals.menu_refresh.emit()
        self.signals.page_changing[str, str, bool].emit('film', str(self.film_id), True)
        checkNotify()
