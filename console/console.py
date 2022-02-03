import time
from tools import commands
from data_handle import database


def show_film():
    film_id = input("film_id: ")
    start = input("start: ")
    end = input("end: ")
    if end == '-2':
        end = 9999
    commands.run_film(film_id, start, end)


def kill():
    con = input("what is kill: ")
    database.set_config(con, False)


def add_film():
    film_name = input("film name: ")
    film_video_link = input("video link: ")
    film_subtitle_link = input("subtitle link: ")
    film_dir = input("path to save")
    film_episode = int(input("last episode watched: "))
    film_notified = input('notified? ')
    if film_notified.upper()[0] in ["T", "Y"]:
        film_notified = True
    else:
        film_notified = False
    commands.add_film(film_name, film_video_link, film_subtitle_link, '', film_dir, film_episode, film_notified)


def run():
    con = input("what is run: ")
    database.set_config(con, True)


if __name__ == '__main__':
    while True:
        command = input('type your command: ')

        if command == 'exit':
            exit(0)
        elif command == 'show':
            show_film()
        elif command == 'kill':
            kill()
        elif command == 'run':
            run()
        elif command == 'add':
            add_film()

        time.sleep(0.5)
