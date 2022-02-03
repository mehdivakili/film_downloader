from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from gui.gui_modules.helpers import deleteItemsOfLayout


class InputArrayField(QWidget):
    def __init__(self, new_func=lambda v: None, get_func=lambda i: None, remove_func=lambda i: None,
                 update_func=lambda v, i: None):
        super().__init__()
        self.l = QVBoxLayout()
        self.items_layout = QVBoxLayout()
        self.items = []
        self.setLayout(self.l)
        self.l.setContentsMargins(0, 0, 0, 0)
        self.new_func = new_func
        self.get_func = get_func
        self.remove_func = remove_func
        self.update_func = update_func

        self.add_btn = QPushButton()
        self.add_btn.setText("add")
        self.add_btn.setObjectName('apply-btn')
        self.add_btn.clicked.connect(self.addItem)
        self.add_btn.setFixedWidth(100)
        self.add_btn.setCursor(Qt.PointingHandCursor)

        self.l.addLayout(self.items_layout)
        self.l.addWidget(self.add_btn)

    def addItem(self, *args):
        item = self.new_func(args)
        l = QHBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)
        l.addWidget(item)
        count = self.items_layout.count()
        delete_btn = QPushButton()
        delete_btn.setText("delete")
        delete_btn.setProperty("cssClass", "run-widget")
        delete_btn.clicked.connect(partial(self.removeItem, l, item))
        delete_btn.setFixedWidth(100)
        delete_btn.setCursor(Qt.PointingHandCursor)

        l.addWidget(delete_btn)

        self.items_layout.addLayout(l)
        self.items.append(item)

    def removeItem(self, l, item):
        self.remove_func(item)
        for i in range(len(self.items)):
            if self.items[i] == item:
                del self.items[i]
                break
        deleteItemsOfLayout(l)

    def updateItem(self, item, value):
        self.update_func(item, value)

    def get_all(self):
        out = []
        for i in self.items:
            out.append(self.get_func(i))
        return out