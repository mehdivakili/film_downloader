from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QLabel


class DayCheckbox(QWidget):
    def __init__(self):
        super().__init__()
        self.checkboxes = []
        self.l = QHBoxLayout()
        for i in range(7):
            w = QCheckBox()
            w.setProperty('cssClass', 'setting-checkbox-widget')

            l = QLabel(str(i) + ':')
            l.setProperty('cssClass', 'setting-checkbox-widget-text')
            l.setFixedWidth(20)
            self.checkboxes.append(w)
            self.l.addWidget(l)
            self.l.addWidget(w)

        self.setLayout(self.l)

    def set_days(self, days):
        for i in range(7):
            self.checkboxes[i].setChecked(i in days)

    def get_days(self):
        return [i for i in range(7) if self.checkboxes[i].isChecked()]