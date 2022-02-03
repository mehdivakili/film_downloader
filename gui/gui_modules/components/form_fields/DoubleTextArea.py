from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QCheckBox


class DoubleTextArea(QWidget):
    def __init__(self, title1, title2):
        super().__init__()
        self.l = QHBoxLayout()
        self.title1 = title1
        self.title2 = title2
        self.title1_label = QLabel(title1)
        self.title2_label = QLabel(title2)
        self.title1_input = QLineEdit()
        self.title2_input = QLineEdit()
        self.title2_input.hide()
        self.show_title_2 = QCheckBox()
        self.show_title_2.clicked.connect(self.title_2_sh)
        self.title2_input.textChanged.connect(self.title_2_sh)
        self.initUI()
        self.setLayout(self.l)

    def initUI(self):
        self.title1_label.setProperty("cssClass", "setting-checkbox-widget-text")
        self.title1_label.setFixedWidth(50)
        self.title2_label.setProperty("cssClass", "setting-checkbox-widget-text")
        self.title2_label.setFixedWidth(50)
        self.title1_input.setProperty("cssClass", "setting-widget")
        # self.title1_input.setFixedHeight(5)
        self.title2_input.setProperty("cssClass", "setting-widget")
        # self.title2_input.setFixedHeight(100)
        self.show_title_2.setProperty("cssClass", "setting-checkbox-widget")

        self.l.addWidget(self.title1_label)
        self.l.addWidget(self.title1_input)
        self.l.addWidget(self.title2_label)
        self.l.addWidget(self.title2_input)
        self.l.addWidget(self.show_title_2)

    def title_2_sh(self, value):
        if value:
            self.title2_input.show()
            self.show_title_2.hide()
        else:
            self.title2_input.hide()
            self.show_title_2.show()
        self.show_title_2.setChecked(bool(value))