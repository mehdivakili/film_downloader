import json

from data_handle.film_database import get_film, delete_film, set_film
from data_handle.database import BASE_DATA_PATH


def get_all_archived():
    with open(BASE_DATA_PATH + '/archived_films.json') as f:
        data = json.load(f)

    return data


def set_all_archived(data):
    f = open(BASE_DATA_PATH + '/archived_films.json', 'w')
    f.write(json.dumps(data))
    f.close()


def archive_film(film_id):
    film = get_film(film_id)
    archived_film = get_all_archived()
    archived_film[film_id] = film
    set_all_archived(archived_film)
    delete_film(film_id)


def restore_film(film_id):
    archived_film = get_all_archived()
    film = archived_film.get(film_id)
    if film:
        del archived_film[film_id]
        set_all_archived(archived_film)
        set_film(film_id, film)


def delete_archived_film(film_id):
    archived_film = get_all_archived()
    film = archived_film.get(film_id)
    if film:
        del archived_film[film_id]
        set_all_archived(archived_film)
