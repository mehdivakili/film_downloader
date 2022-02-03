import zipfile

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QSpinBox, QAbstractSpinBox, \
    QPushButton, QScrollArea, QMessageBox

import data_handle.film_archived_database
import data_handle.film_database
from globals.globals import Communicate
from gui.gui_modules.components.form_fields.GetFile import GetFile
from tools import commands


class FilmTools(QWidget):
    def __init__(self, film_id):
        super().__init__()
        self.film_id = film_id
        self.film = data_handle.film_database.get_film(film_id)
        self.signals = Communicate.getInstance()
        self.tools_layout = QVBoxLayout()
        self.w = QWidget()
        self.scrollbar = QScrollArea()
        self.scrollbar.setProperty('cssClass', 'scroll')
        self.scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollbar.setWidgetResizable(True)
        self.scrollbar.setWidget(self.w)

        self.w.setLayout(self.tools_layout)
        self.m = QVBoxLayout()
        self.m.setContentsMargins(0, 0, 0, 0)
        self.initUI()
        self.m.addWidget(self.scrollbar)
        self.setLayout(self.m)
        self.tools_layout.setAlignment(Qt.AlignTop)

    def initUI(self):
        self.file_rename_title = QLabel("file rename")
        self.file_rename_title.setProperty('cssClass', 'film-title')

        self.file_rename_path_lable = QLabel("file rename path")
        self.file_rename_path_lable.setProperty("cssClass", "setting-widget-text")
        self.file_rename_path_input = QLineEdit()
        self.file_rename_path_input.setProperty("cssClass", "setting-widget")
        self.file_rename_path_input.setText(self.film["directory"])

        self.file_rename_range_layout = QHBoxLayout()

        self.file_rename_range_start_title = QLabel("start: ")
        self.file_rename_range_start_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.file_rename_range_start_title.setProperty('cssClass', 'setting-widget-text')
        self.file_rename_range_start_title.setFixedWidth(50)

        self.file_rename_range_start_input = QSpinBox()
        self.file_rename_range_start_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.file_rename_range_start_input.setProperty("cssClass", "run-widget")
        self.file_rename_range_start_input.setMaximum(9999)

        self.file_rename_range_end_title = QLabel("end: ")
        self.file_rename_range_end_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.file_rename_range_end_title.setProperty('cssClass', 'setting-widget-text')
        self.file_rename_range_end_title.setFixedWidth(50)

        self.file_rename_range_end_input = QSpinBox()
        self.file_rename_range_end_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.file_rename_range_end_input.setProperty("cssClass", "run-widget")
        self.file_rename_range_end_input.setMaximum(9999)

        self.file_rename_range_layout.addWidget(self.file_rename_range_start_title)
        self.file_rename_range_layout.addWidget(self.file_rename_range_start_input)
        self.file_rename_range_layout.addWidget(self.file_rename_range_end_title)
        self.file_rename_range_layout.addWidget(self.file_rename_range_end_input)

        self.file_rename_apply_btn = QPushButton()
        self.file_rename_apply_btn.setText("file rename")
        self.file_rename_apply_btn.setObjectName('apply-btn')
        self.file_rename_apply_btn.clicked.connect(self.file_rename)
        self.file_rename_apply_btn.setFixedWidth(200)
        self.file_rename_apply_btn.setCursor(Qt.PointingHandCursor)

        self.file_import_title = QLabel("file import")
        self.file_import_title.setProperty('cssClass', 'film-title')

        self.file_import_name_lable = QLabel("file import name")
        self.file_import_name_lable.setProperty("cssClass", "setting-widget-text")
        self.file_import_name_input = QLineEdit()
        self.file_import_name_input.setProperty("cssClass", "setting-widget")
        self.file_import_name_input.setText(self.film["directory"])

        self.file_import_ext_lable = QLabel("file import extension")
        self.file_import_ext_lable.setProperty("cssClass", "setting-widget-text")
        self.file_import_ext_input = QLineEdit()
        self.file_import_ext_input.setProperty("cssClass", "setting-widget")

        self.file_import_path_lable = QLabel("file import path")
        self.file_import_path_lable.setProperty("cssClass", "setting-widget-text")
        self.file_import_path_input = GetFile()
        self.file_import_path_input.on_get_file.signal.connect(self.update_p)

        self.file_import_range_layout = QHBoxLayout()

        self.file_import_range_start_title = QLabel("start: ")
        self.file_import_range_start_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.file_import_range_start_title.setProperty('cssClass', 'setting-widget-text')
        self.file_import_range_start_title.setFixedWidth(50)

        self.file_import_range_start_input = QSpinBox()
        self.file_import_range_start_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.file_import_range_start_input.setProperty("cssClass", "run-widget")
        self.file_import_range_start_input.setMaximum(9999)

        self.file_import_range_end_title = QLabel("end: ")
        self.file_import_range_end_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.file_import_range_end_title.setProperty('cssClass', 'setting-widget-text')
        self.file_import_range_end_title.setFixedWidth(50)

        self.file_import_range_end_input = QSpinBox()
        self.file_import_range_end_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.file_import_range_end_input.setProperty("cssClass", "run-widget")
        self.file_import_range_end_input.setMaximum(9999)

        self.file_import_range_layout.addWidget(self.file_import_range_start_title)
        self.file_import_range_layout.addWidget(self.file_import_range_start_input)
        self.file_import_range_layout.addWidget(self.file_import_range_end_title)
        self.file_import_range_layout.addWidget(self.file_import_range_end_input)

        self.file_import_apply_btn = QPushButton()
        self.file_import_apply_btn.setText("file import")
        self.file_import_apply_btn.setObjectName('apply-btn')
        self.file_import_apply_btn.clicked.connect(self.file_import)
        self.file_import_apply_btn.setFixedWidth(200)
        self.file_import_apply_btn.setCursor(Qt.PointingHandCursor)

        self.sub_delay_title = QLabel("subtitle delay")
        self.sub_delay_title.setProperty('cssClass', 'film-title')

        self.sub_delay_layout = QHBoxLayout()

        self.sub_delay_second_title = QLabel("delay(second): ")
        self.sub_delay_second_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.sub_delay_second_title.setProperty('cssClass', 'setting-widget-text')
        self.sub_delay_second_title.setFixedWidth(150)

        self.sub_delay_second_input = QSpinBox()
        self.sub_delay_second_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.sub_delay_second_input.setProperty("cssClass", "run-widget")
        self.sub_delay_second_input.setMaximum(9999)
        self.sub_delay_second_input.setMinimum(-9999)

        self.sub_delay_range_start_title = QLabel("start: ")
        self.sub_delay_range_start_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.sub_delay_range_start_title.setProperty('cssClass', 'setting-widget-text')
        self.sub_delay_range_start_title.setFixedWidth(50)

        self.sub_delay_range_start_input = QSpinBox()
        self.sub_delay_range_start_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.sub_delay_range_start_input.setProperty("cssClass", "run-widget")
        self.sub_delay_range_start_input.setMaximum(9999)

        self.sub_delay_range_end_title = QLabel("end: ")
        self.sub_delay_range_end_title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.sub_delay_range_end_title.setProperty('cssClass', 'setting-widget-text')
        self.sub_delay_range_end_title.setFixedWidth(50)

        self.sub_delay_range_end_input = QSpinBox()
        self.sub_delay_range_end_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.sub_delay_range_end_input.setProperty("cssClass", "run-widget")
        self.sub_delay_range_end_input.setMaximum(9999)

        self.sub_delay_layout.addWidget(self.sub_delay_second_title)
        self.sub_delay_layout.addWidget(self.sub_delay_second_input)
        self.sub_delay_layout.addWidget(self.sub_delay_range_start_title)
        self.sub_delay_layout.addWidget(self.sub_delay_range_start_input)
        self.sub_delay_layout.addWidget(self.sub_delay_range_end_title)
        self.sub_delay_layout.addWidget(self.sub_delay_range_end_input)

        self.sub_delay_apply_btn = QPushButton()
        self.sub_delay_apply_btn.setText("subtitle delay")
        self.sub_delay_apply_btn.setObjectName('apply-btn')
        self.sub_delay_apply_btn.clicked.connect(self.subtitle_delay)
        self.sub_delay_apply_btn.setFixedWidth(200)
        self.sub_delay_apply_btn.setCursor(Qt.PointingHandCursor)

        self.delete_btn = QPushButton()
        self.delete_btn.setText('delete film')
        self.delete_btn.setObjectName('delete-btn')
        self.delete_btn.setFixedWidth(200)
        self.delete_btn.clicked.connect(self.delete_film)
        self.delete_btn.setCursor(Qt.PointingHandCursor)

        self.archive_btn = QPushButton()
        self.archive_btn.setText('archive film')
        self.archive_btn.setObjectName('archive-btn')
        self.archive_btn.setFixedWidth(200)
        self.archive_btn.clicked.connect(self.archive_film)
        self.archive_btn.setCursor(Qt.PointingHandCursor)

        self.other_opt_title = QLabel("other operations")
        self.other_opt_title.setProperty('cssClass', 'film-title')

        self.other_opt_layout = QHBoxLayout()
        self.other_opt_layout.setAlignment(Qt.AlignLeft)

        self.other_opt_layout.addWidget(self.delete_btn)
        self.other_opt_layout.addWidget(self.archive_btn)

        self.tools_layout.addWidget(self.file_rename_title)
        self.tools_layout.addWidget(self.file_rename_path_lable)
        self.tools_layout.addWidget(self.file_rename_path_input)
        self.tools_layout.addLayout(self.file_rename_range_layout)
        self.tools_layout.addWidget(self.file_rename_apply_btn)

        self.tools_layout.addWidget(self.file_import_title)
        self.tools_layout.addWidget(self.file_import_path_lable)
        self.tools_layout.addWidget(self.file_import_path_input)
        self.tools_layout.addWidget(self.file_import_name_lable)
        self.tools_layout.addWidget(self.file_import_name_input)
        self.tools_layout.addWidget(self.file_import_ext_lable)
        self.tools_layout.addWidget(self.file_import_ext_input)
        self.tools_layout.addLayout(self.file_import_range_layout)
        self.tools_layout.addWidget(self.file_import_apply_btn)

        self.tools_layout.addWidget(self.sub_delay_title)
        self.tools_layout.addLayout(self.sub_delay_layout)
        self.tools_layout.addWidget(self.sub_delay_apply_btn)

        self.tools_layout.addWidget(self.other_opt_title)
        self.tools_layout.addLayout(self.other_opt_layout)

    def file_rename(self):
        path = self.file_rename_path_input.text()
        start = self.file_rename_range_start_input.value()
        end = self.file_rename_range_end_input.value()
        commands.file_rename(self.film, path, start, end)

    def update_p(self, directory):
        z = zipfile.ZipFile(directory)
        names = z.namelist()
        self.file_import_name_input.setText(names[0])

    def subtitle_delay(self):
        pass

    def file_import(self):
        zip_path = self.file_import_path_input.get_dir()
        start = self.file_import_range_start_input.value()
        end = self.file_import_range_end_input.value()
        file_name = self.file_import_name_input.text()
        file_ext = self.file_import_ext_input.text()
        imported = commands.import_file(self.film, zip_path, file_name, file_ext, start, end)
        QMessageBox.about(self, f'{len(imported)} file was imported', "Message")


    def delete_film(self):
        data_handle.film_database.delete_film(self.film_id)
        self.signals.menu_refresh.emit()
        self.signals.page_changing.emit('home', '')

    def archive_film(self):
        data_handle.film_archived_database.archive_film(self.film_id)
        self.signals.menu_refresh.emit()
        self.signals.page_changing[str, str, bool].emit("restore film", '', True)
