from PyQt5.QtWidgets import QLineEdit

from gui.gui_modules.components.form_fields.InputArrayField import InputArrayField


class MultiLineEdit(InputArrayField):

    def __init__(self):
        super().__init__(new_func=self.new, get_func=self.get, update_func=self.update)

    def new(self, args):
        e = QLineEdit()
        e.setProperty("cssClass", "setting-widget")
        if args[0]:
            e.setText(args[0])
        return e

    def get(self, e):
        return e.text()

    def update(self, item, value):
        item.setText(value)