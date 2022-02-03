from gui.gui_modules.components.form_fields.DoubleTextArea import DoubleTextArea
from gui.gui_modules.components.form_fields.InputArrayField import InputArrayField


class MultiDoubleTextArea(InputArrayField):
    def __init__(self, key1, key2):
        super().__init__(new_func=self.new, get_func=self.get, update_func=self.update)
        self.key1 = key1
        self.key2 = key2

    def new(self, args):

        e = DoubleTextArea(self.key1, self.key2)
        if args[0]:
            data = args[0]
            if self.key1 in data.keys():
                e.title1_input.setText(data[self.key1])
            if self.key2 in data.keys():
                e.title2_input.setText(data[self.key2])

        return e

    def get(self, e):
        title1 = e.title1_label.text()
        title2 = e.title2_label.text()
        input1 = e.title1_input.text()
        input2 = e.title2_input.text()
        return {title1: input1, title2: input2}

    def update(self, item, value):
        item.title1_input.setText(value[item.title1_label.text()])
        item.title2_input.setText(value[item.title2_label.text()])