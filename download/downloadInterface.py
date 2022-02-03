class DownloadInterface:

    def __init__(self, link, directory, query=""):
        self.link = link
        self.directory = directory
        self.query = query

    def check_is_exist(self):
        pass

    def download_file(self, directory):
        pass

    def start(self, sync=False):
        pass

    def stop(self):
        pass

    def cancel(self):
        pass

    def set_callback(self):
        pass

    def get_file_data(self):
        pass

    def parse_data(self):
        pass

    def exec_query(self):
        pass
