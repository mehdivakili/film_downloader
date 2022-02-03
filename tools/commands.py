import os
import zipfile

import data_handle.film_database
from data_handle import database
import threading
from run import run
from download import download
from notify import notify
import jdatetime

DETACHED_PROCESS = 0x00000008


def run_film(film_id, start, end=9999, is_play=True):
    if is_play:
        return run_p(run.Run, (int(film_id), int(start), int(end), is_play))
    return run_p(run.download_from, (int(film_id), int(start), int(end)))


def kill_film():
    database.set_config('run', False)


def add_film(film_name, vid_link, sub_link, sub_query, directory, last_episode, notify, icon='images/icon.png'):
    if not icon:
        icon = 'images/icon.png'
    film = {
        "name": film_name,
        "video_link": vid_link,
        "subtitle_link": sub_link,
        "subtitle_query": sub_query,
        "directory": directory,
        "last_episode_watched": last_episode,
        "notified": notify,
        "is_new": False,
        "icon": icon
    }
    return data_handle.film_database.add_film(film)


def run_p(f, args=()):
    t = threading.Thread(target=f, args=args)
    t.start()
    return t


def start_download(directory):
    download.DownloadManager.get_download(directory).start(True)


def import_file(film, zip_path, file_name: str, ext, start, end):
    z = zipfile.ZipFile(zip_path)
    names = z.namelist()
    out_dir = film["directory"] + '.' + ext
    file_name = file_name.replace('\\', '/')
    imported_files = []
    for i in range(start, end + 1):
        in_dir = file_name.format(i)
        if in_dir in names:
            with z.open(in_dir, 'r') as sub:
                with open(out_dir.format(i), 'wb') as f:
                    f.write(sub.read())
                    imported_files.append(in_dir)

    return imported_files


def file_rename(film, path, start, end):
    for i in range(start, end + 1):
        if os.path.exists(path.format(i)):
            os.rename(path.format(i), rf'{film["directory"].format(i)}.{path[-3:]}')


def get_day_of_current_week():
    return jdatetime.datetime.today().weekday()


def checkNotify():
    run_p(notify.main)


def cancel_download(download):
    run_p(download.cancel_download)
