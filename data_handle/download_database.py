import json

from data_handle.database import BASE_DATA_PATH


def get_download(directory):
    with open(BASE_DATA_PATH + '/download.json') as f:
        data = json.load(f)
    return data.get(directory)


def get_download_all():
    with open(BASE_DATA_PATH + '/download.json') as f:
        data = json.load(f)
    return data


def set_download(directory, value):
    with open(BASE_DATA_PATH + '/download.json') as f:
        data = json.load(f)
    data[directory] = value

    w = json.dumps(data)
    f = open(BASE_DATA_PATH + '/download.json', 'w')
    f.write(w)
    f.close()


def get_download_init():
    return {
        "link": "",
        "total": 0,
        "query": "",
    }


def is_downloading(directory):
    f = get_download(directory)
    if f and f["is_downloading"]:
        return True
    return False


def set_download_status(directory, value):
    f = get_download(directory)
    if f:
        f["is_downloading"] = value
        set_download(directory, f)


def remove_download(directory):
    d = get_download_all()
    del d[directory]
    f = open(BASE_DATA_PATH + '/download.json', 'w')
    f.write(json.dumps(d))
    f.close()