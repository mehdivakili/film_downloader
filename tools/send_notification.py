from win10toast import ToastNotifier
import threading


class Notification:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Notification.__instance is None:
            Notification()
        return Notification.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Notification.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Notification.__instance = self
            self.toaster = ToastNotifier()

    def send_notification(self, title, subtitle, callback=lambda: None):
        if self.toaster.notification_active():
            t = threading.Thread(target=self.send_notification, args=(title, subtitle, callback))
            t.start()
            t.join(timeout=1)
            return t
        else:
            return self.toaster.show_toast(title, subtitle, threaded=True, icon_path="icon.ico",
                                           callback_on_click=callback)

