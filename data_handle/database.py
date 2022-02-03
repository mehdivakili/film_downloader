import json
import os
from globals.globals import Communicate

config = False
BASE_DATA_PATH = 'data'


def get_config(key):
    global config
    if not config:
        with open('data/config.json') as f:
            config = json.load(f)
    return config.get(key)


def set_config(key, value):
    global config
    if not config:
        with open('data/config.json') as f:
            config = json.load(f)
    config[key] = value
    f = open('data/config.json', 'w')
    f.write(json.dumps(config))
    f.close()


def log(log_text):
    f = open('logs/log.log', 'a')
    g = open('logs/all_log.log', 'a')
    f.write(str(log_text) + '\n')
    g.write(str(log_text) + '\n')
    f.close()
    g.close()
    c = Communicate.getInstance()
    c.log_changed.emit()



def get_app():
    if os.path.exists('app.lock'):
        return True
    return False


def get_proxy():
    return get_config('proxy')


def get_log():
    lines = []
    if os.path.exists('logs/log.log'):
        with open('logs/log.log', 'r') as f:
            lines = f.readlines()
    return lines


def remove_log():
    if os.path.exists('logs/log.log'):
        os.remove('logs/log.log')


def window_should_open():
    with open('data/config.json') as f:
        return json.load(f)["main_run"]
