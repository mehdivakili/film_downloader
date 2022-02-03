import json
import random


def get_film(film_id):
    film_id = str(film_id)
    with open('data/films.json') as f:
        data = json.load(f)

    return data.get(film_id)


def get_all():
    with open('data/films.json') as f:
        data = json.load(f)

    return data


def set_film(film_id, film_data):
    with open('data/films.json') as f:
        data = json.load(f)
    data[film_id] = film_data
    f = open('data/films.json', 'w')
    f.write(json.dumps(data))
    f.close()


def add_film(film):
    film_id = random.randint(1000000, 9999999)
    with open('data/films.json') as f:
        data = json.load(f)
    data[film_id] = film
    f = open('data/films.json', 'w')
    f.write(json.dumps(data))
    f.close()
    return film_id


def delete_film(film_id):
    data = get_all()
    del data[str(film_id)]
    f = open('data/films.json', 'w')
    f.write(json.dumps(data))
    f.close()


def set_film_episode(film_id, episode):
    film_id = str(film_id)
    data = get_film(film_id)
    data["last_episode_watched"] = episode
    data["is_new"] = False
    set_film(film_id, data)


def get_film_row(film_id):
    films = get_all()
    film_id = str(film_id)
    n = 0
    for i in films:
        if i == film_id:
            return n
        n += 1
    return n


def get_film_episode(film_id):
    return get_film(film_id)["last_episode_watched"]
