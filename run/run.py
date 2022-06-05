import psutil
import os

import data_handle.film_database
from download.download import download_all, check_files_downloaded
import time
from data_handle import database
import sys
from pynput.keyboard import Key, Listener
import subprocess
from functools import partial
from globals.globals import Communicate


def main():
    film_id = int(sys.argv[1]) if (len(sys.argv) >= 2) else 0
    start = int(sys.argv[2]) if (len(sys.argv) >= 3) else 0
    end = int(sys.argv[3]) if (len(sys.argv) >= 4) else 9999
    Run(film_id, start, end)


def video_is_running():
    video_player = database.get_config('video_player')
    return video_player in (p.name() for p in psutil.process_iter())


def kill_video_player():
    try:
        video_player = database.get_config('video_player')
        for proc in psutil.process_iter():
            if proc.name() == video_player:
                proc.kill()
    finally:
        pass


def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)
    return float(result.stdout)


def get_human_readable_length(filename):
    length = int(get_length(filename))
    return f'{length // 60}:{length % 60}'


def run(film_id, start, end, is_play=True):
    film = data_handle.film_database.get_film(film_id)
    i = start
    if i == -1:
        i = data_handle.film_database.get_film_episode(film_id)
    if end == -1:
        end = data_handle.film_database.get_film_episode(film_id)
    if is_play:
        database.set_config('run', True)

        while i <= end and database.get_app() and database.get_config('run') and \
                download_all(film["video"], film["subtitle"], film["directory"], i):

            while database.get_app() and video_is_running():
                time.sleep(0.5)

            if not (database.get_config('run') and database.get_app()):
                break

            if is_play:
                if video_is_running():
                    kill_video_player()
                os.popen(f'start "" "{film["directory"].format(i)}.mkv"')
            data_handle.film_database.set_film_episode(film_id, i)
            if not (database.get_config('run') and database.get_app()):
                break

            time.sleep(0.5)
            i += 1
        database.set_config('run', False)
    else:
        while i <= end and database.get_app() and download_all(film["video"], film["subtitle"],

                                                               film["directory"], i):
            continue


def play_video(directory, is_play):
    if is_play:
        if video_is_running():
            kill_video_player()
        os.popen(f'start "" "{directory}"')


def run_without_download(film_id, episode):
    play_video(f'{data_handle.film_database.get_film(film_id)["directory"].format(episode)}.mkv', True)


def download_from(film_id, start, end):
    if start - 1 == end:
        return
    film = data_handle.film_database.get_film(film_id)
    while check_files_downloaded(film["directory"], start):
        start += 1

    download_all(film["video"], film["subtitle"], film["directory"], start,
                 callback=partial(download_from, film_id, start + 1, end))


class Run:
    def __init__(self, film_id, start, end, is_play=True):
        self.film_id = film_id
        self.start = start
        self.end = end
        self.is_play = is_play
        self.film = data_handle.film_database.get_film(film_id)
        self.i = start
        self.stop = False
        self.listener = Listener(on_release=self.key_handle)
        self.signals = Communicate.getInstance()

        if self.i == -1:
            self.i = data_handle.film_database.get_film_episode(film_id)
        if end == -1:
            self.end = data_handle.film_database.get_film_episode(film_id)

        self.listener.start()
        self.i = self.i - 1
        self.key_handle(Key.f3)
        # time.sleep(0.5)
        # while database.get_app() and video_is_running():
        #     time.sleep(0.5)
        #     if self.i >= self.end:
        #         break
        # self.stop = True
        # self.listener.stop()

    def key_handle(self, key):
        if key == Key.f3:
            temp_i = self.i + 1
            self.listener.stop()
            if temp_i <= self.end and download_all(self.film["video"], self.film["subtitle"],
                                                   self.film["directory"], temp_i, sync=False):
                play_video(f'{self.film["directory"].format(temp_i)}.mkv', self.is_play)
                self.i = temp_i
                data_handle.film_database.set_film_episode(self.film_id, self.i)
                self.signals.page_changing[str, str, bool].emit('film', str(self.film_id), True)

                temp_i += 1
                if not self.stop:
                    self.listener = Listener(on_release=self.key_handle)
                    self.listener.start()
                download_all(self.film["video"], self.film["subtitle"],
                             self.film["directory"], temp_i)
            else:
                kill_video_player()
                self.listener.stop()

        if key == Key.f1:
            temp_i = self.i - 1
            self.listener.stop()
            if temp_i <= self.end and download_all(self.film["video"], self.film["subtitle"],
                                                   self.film["directory"], temp_i):
                play_video(f'{self.film["directory"].format(temp_i)}.mkv', self.is_play)
                self.i = temp_i
                data_handle.film_database.set_film_episode(self.film_id, self.i)

                if not self.stop:
                    self.listener = Listener(on_release=self.key_handle)
                    self.listener.start()
            else:
                kill_video_player()
                self.listener.stop()


if __name__ == '__main__':
    main()
