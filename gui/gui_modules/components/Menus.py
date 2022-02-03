import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QPushButton

import data_handle.film_database
from globals.globals import Communicate
from gui.gui_modules.helpers import deleteItemsOfLayout


class Menus(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = Communicate.getInstance()
        self.signals.menu_refresh.connect(self.refresh)
        self.menu_con = QVBoxLayout()
        self.menu_con.setContentsMargins(0, 0, 0, 0)
        self.menu_con.setSpacing(0)
        self.setFixedWidth(300)
        self.initUI()
        self.setLayout(self.menu_con)

    def initUI(self):
        MENU_ITEM_HEIGHT = 60
        self.menu = QListWidget()

        self.menu.setObjectName('menu')

        films = data_handle.film_database.get_all()
        for i in films:
            film = films[i]
            f = QListWidgetItem(film["name"])
            f.setText(film["name"])
            f.setTextAlignment(Qt.AlignCenter)
            f.setData(Qt.UserRole, i)
            self.menu.addItem(f)
        self.menu.setFixedHeight(MENU_ITEM_HEIGHT * len(films))
        self.menu.itemClicked.connect(self.film_clicked)

        self.menu.setCursor(Qt.PointingHandCursor)
        self.middle_menu = QListWidget()
        self.middle_menu.setItemAlignment(Qt.AlignBottom)
        self.middle_menu.setObjectName('middle-menu')

        self.bottom_menu = QListWidget()
        self.bottom_menu.setItemAlignment(Qt.AlignBottom)
        self.bottom_menu.setObjectName('bottom-menu')

        self.bottom_menu.itemClicked.connect(self.bar_clicked)
        self.bottom_menu.setCursor(Qt.PointingHandCursor)
        items = ['home', 'setting', 'add film']
        for item in items:
            f = QListWidgetItem(item)
            f.setText(item)
            f.setTextAlignment(Qt.AlignCenter)

            self.bottom_menu.addItem(f)

        self.bottom_menu.setFixedHeight(MENU_ITEM_HEIGHT * len(items))

        # self.menu_con.addWidget(self.middle_menu)
        option_lable = QLabel("options")
        option_lable.setProperty("cssClass", 'menu-text')
        option_lable.setFixedHeight(30)
        option_lable.setAlignment(Qt.AlignHCenter)

        film_lable = QLabel("films")
        film_lable.setProperty("cssClass", 'menu-text')
        film_lable.setFixedHeight(30)
        film_lable.setAlignment(Qt.AlignHCenter)

        # self.menu_con.addWidget(option_lable)
        # self.menu_con.addWidget(self.bottom_menu)
        # self.menu_con.addWidget(film_lable)
        self.menu_con.addWidget(self.menu)
        self.menu_con.addWidget(self.middle_menu)
        self.options = Options()
        self.menu_con.addWidget(self.options)

    def set_menu_rows(self, a, b):
        self.menu.setCurrentRow(a)
        s = self.menu.item(a - 1)
        e = self.menu.item(a + 1)

        self.bottom_menu.setCurrentRow(b)

    def refresh(self):
        deleteItemsOfLayout(self.menu_con)
        self.initUI()

    def menu_refresh(self, row):
        row = int(row)
        deleteItemsOfLayout(self.menu_con)

        self.add_menu()
        if row == -2:
            self.bottom_menu.setCurrentRow(0)
            self.add_home_page()
            return
        self.add_film_page(str(row))
        self.menu.setCurrentRow(data_handle.film_database.get_film_row(row))

    def film_clicked(self, item: QListWidgetItem):
        self.bottom_menu.setCurrentRow(-1)
        self.signals.page_changing.emit('film', str(item.data(Qt.UserRole)))

    def bar_clicked(self, item: QListWidgetItem):
        self.menu.setCurrentRow(-1)
        self.signals.page_changing.emit(item.text(), '')


class Options(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = Communicate.getInstance()
        self.l = QHBoxLayout()
        self.l.setContentsMargins(0, 0, 0, 15)
        self.home_btn = OptionsBtn('fa5s.home', lambda: self.signals.page_changing.emit('home', ''))
        self.setting_btn = OptionsBtn('fa5s.cog', lambda: self.signals.page_changing.emit('setting', ''))
        self.add_film_btn = OptionsBtn('fa5s.plus', lambda: self.signals.page_changing.emit('add film', ''))
        self.restore_film_btn = OptionsBtn('fa5s.archive', lambda: self.signals.page_changing.emit('restore film', ''))
        self.initUI()
        self.setLayout(self.l)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #34495e')

    def initUI(self):
        self.l.addWidget(self.home_btn)
        self.l.addWidget(self.setting_btn)
        self.l.addWidget(self.add_film_btn)
        self.l.addWidget(self.restore_film_btn)
        self.home_btn.clicked()


class OptionsBtn(QWidget):
    def __init__(self, icon, onclick=lambda: None):
        super().__init__()
        self.icon = icon
        self.signals = Communicate.getInstance()
        self.btn = QPushButton()
        self.btn.clicked.connect(self.signals.option_click.emit)
        self.btn.clicked.connect(onclick)
        self.btn.clicked.connect(self.clicked)
        self.signals.menu_refresh.connect(self.not_clicked)
        self.signals.option_click.connect(self.not_clicked)

        self.btn.setProperty("cssClass", "option-btn")
        self.active_label = QPushButton()
        self.l = QHBoxLayout()
        self.l.setContentsMargins(0, 0, 0, 0)
        self.initUI()
        self.l.addWidget(self.btn)
        self.setLayout(self.l)
        self.setStyleSheet('''
            QPushButton[cssClass="option-btn"]{
                background: #34495e;
                color: white;
                border-radius: 25;
            }
            
            QPushButton[cssClass="option-btn"]:hover{
                background: #3498db;
            }
            *[cssClass="option-label"]{
                background: #2c3e50;
                color: white;
                border-radius: 25;
            }
            
        ''')

    def initUI(self):
        self.icon = qta.icon(self.icon, color='white')
        self.btn.setFixedSize(50, 50)
        self.btn.setIcon(self.icon)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.active_label.setFixedSize(50, 50)
        self.active_label.setIcon(self.icon)
        self.active_label.setProperty("cssClass", "option-label")
        self.active_label.hide()
        self.l.addWidget(self.active_label)

    def clicked(self):
        self.btn.hide()
        self.active_label.show()

    def not_clicked(self):
        if self.btn.isHidden():
            self.active_label.hide()
            self.btn.show()