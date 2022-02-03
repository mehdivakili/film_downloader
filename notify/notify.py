import data_handle.film_database
from download import download
from data_handle import database
from functools import partial
from tools.send_notification import Notification
from tools import commands


def notify(film, film_id, episode):
    film["is_new"] = True
    data_handle.film_database.set_film(film_id, film)
    n = Notification.getInstance()
    f = partial(commands.run_film, film_id, episode, episode)
    n.send_notification(f'the episode {episode} of {film["name"]} is download', "click to watch", f)


def main():

    if database.get_config('notify') and database.get_app():
        database.log('notify start')
        day = commands.get_day_of_current_week()
        films = data_handle.film_database.get_all()

        for i in films:
            film = films[i]
            episode = film['last_episode_watched'] + 1

            if not database.get_app():
                continue

            elif not film['notified'] or day not in film["notify_days"]:
                database.log(f"{film['name']} not notified")
                continue

            elif download.check_files_downloaded(film['directory'], episode):
                database.log(f"{film['name']} episode {episode} exists")
                continue

            if download.check_is_exist(film["video"], episode) or download.check_is_exist(film["subtitle"], episode):
                database.log(f"{film['name']} check and exist")
                callback = partial(notify, film, i, episode)
                download.download_all_callback(film["video"], film["subtitle"],
                                               film['directory'], episode,
                                               callback)
            else:
                database.log(f"{film['name']} episode {episode} not released")
    database.log('notify end')


if __name__ == '__main__':
    main()
