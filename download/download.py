import os
import shutil

import requests
import zipfile, rarfile
import patoolib
from os import listdir
from os.path import isfile, join, isdir
from mimetypes import guess_extension

import time
from io import BytesIO
import subprocess

import data_handle.download_database
from data_handle import database
import sys
from bs4 import BeautifulSoup
import threading

proxyDict = database.get_proxy()


def get_init_header():
    return {
        # 'Host': 'anime-list16.site',
        # 'Sec-Ch-Ua': '\\" Not A;Brand\\";v=\\"99\\", \\"Chromium\\";v=\\"90\\"',
        # 'Sec-Ch-Ua-Mobile': '?0',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.212 Safari/537.36',
        # 'Sec-Fetch-Site': 'same-origin',
        # 'Sec-Fetch-Mode': 'navigate',
        'Referer': 'https://anime-list16.site/anime/sub/18437/%D8%AF%D8%A7%D9%86%D9%84%D9%88%D8%AF-%D8%B2%DB%8C%D8%B1'
                   '%D9%86%D9%88%DB%8C%D8%B3-nanatsu-no-taizai-fundo-no-shinpan-%D9%82%D8%B3%D9%85%D8%AA-23',
        'Connection': 'close',
    }


def get_init_cookie():
    return {
        '$size_window': '0',
        'hit_anime_7863': '1',
        'XSRF-TOKEN': 'ns38Lbc3ZvGYI2by7iZbk3RcTQCyRpYZYCZ42UqY',
        'animecms_session': 'oTjITfRghYLGvdQNaukzpbBNijPNteVzdxJ9qL0K',
        'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': '371964%7CzvD0o3qMucDvipPgyMiuxHYxY6UmjEKgtVXzSVuv6a6nR9VLxUTAmKnkQ238%7C%242y%2410%24ekS4N.XZkAAdMrNq5nL0k.TFT3Pacq1rJml3KN5CsaG2YTe0Yuz3W',
        '_ga': 'GA1.2.1589712303.1627456235',
        '_gid': 'GA1.2.1057930631.1627456235',
        'zrpv2': '1',
    }


def check_wifi_connection():
    info = str(subprocess.Popen("netsh wlan show interfaces", shell=True, stdout=subprocess.PIPE).stdout.read())
    for wifi in database.get_config('trusted_wifi'):
        if wifi in info:
            return True
    return False


def download_file(link, directory, use_proxy=False, times=0, callback=lambda: None):
    headers = get_init_header()
    if not check_wifi_connection():
        database.log('wifi not connected')
        return False
    try:
        if use_proxy and proxyDict:
            response = requests.get(link, stream=True, timeout=30, proxies=proxyDict, headers=headers,
                                    cookies=get_init_cookie())
            response.close()
        else:
            response = requests.get(link, stream=True, timeout=30)
            response.close()
        total_length = response.headers.get('content-length')

        if total_length is None:
            f = open(directory, 'wb')
            response.raise_for_status()
            if use_proxy:
                response = requests.get(link, stream=True, proxies=proxyDict, headers=headers,
                                        cookies=get_init_cookie())
            else:
                response = requests.get(link, stream=True)
            f.write(response.content)
        else:
            f_data = data_handle.download_database.get_download(directory)
            if not f_data:
                f_data = data_handle.download_database.get_download_init()
            content = b''
            if os.path.exists(directory):
                with open(directory, 'rb') as f:
                    content = f.read()

            total_length = int(total_length)

            f_data["total"] = total_length
            f_data["dl"] = len(content)
            f_data["link"] = link
            if len(content) >= total_length or f_data["stop"]:
                if len(content) >= total_length:
                    data_handle.download_database.remove_download(directory)
                response.close()
                return False
            data_handle.download_database.set_download(directory, f_data)
            dl = f_data["dl"]
            headers = {'Range': f'bytes={dl}-{total_length}'}

            if use_proxy:
                response = requests.get(link, stream=True, proxies=proxyDict, headers=headers)
            else:
                response = requests.get(link, stream=True, headers=headers)
            if data_handle.download_database.is_downloading(directory):
                response.close()
                while data_handle.download_database.is_downloading(directory) and database.get_app():
                    time.sleep(0.5)
                data_handle.download_database.set_download_status(directory, False)
                return True
            f = open(directory, 'wb')
            f.write(content)
            data_handle.download_database.set_download(directory, f_data)
            data_handle.download_database.set_download_status(directory, True)

            for data in response.iter_content(chunk_size=2097152):
                f_data = data_handle.download_database.get_download(directory)
                dl += len(data)
                f_data['dl'] = dl + 1
                f.write(data)
                data_handle.download_database.set_download(directory, f_data)
                if f_data["stop"] or not database.get_app():
                    data_handle.download_database.set_download_status(directory, False)
                    response.close()
                    f.close()
                    return False
            data_handle.download_database.set_download_status(directory, False)

        response.close()
        f.close()
        f_data = data_handle.download_database.get_download(directory)
        if f_data["dl"] < f_data["total"] - 1:
            return download_file(link, directory, False, times, callback)

        data_handle.download_database.remove_download(directory)
        return True

    except Exception as e:
        database.log(str(e))
        time.sleep(5)
        data_handle.download_database.set_download_status(directory, False)
        if times == 0:
            return download_file(link, directory, False, times + 1, callback)
        elif times == 1:
            return download_file(link, directory, False, times + 1, callback)
        else:
            return False


def send_request(link, show=False, use_proxy=False, times=0, headers=None, cookies=None):
    if not headers:
        headers = get_init_header()
    if not cookies:
        cookies = get_init_cookie()
    database.log(f"time {times} to send request")
    if not check_wifi_connection():
        database.log('wifi is not connected')
        return False, False

    try:
        if not show:
            if use_proxy and proxyDict:
                response = requests.get(link, headers=headers, cookies=cookies)
            else:
                response = requests.get(link, headers=headers, cookies=cookies)
            response.raise_for_status()

            content = response.content
        else:
            if use_proxy and proxyDict:
                response = requests.get(link, stream=True, proxies=proxyDict, headers=headers, cookies=cookies,
                                        verify=False)
            else:
                response = requests.get(link, stream=True, headers=headers, cookies=cookies)
            total_length = response.headers.get('content-length')
            if total_length is None:  # no content length header
                response.raise_for_status()
                content = response.content
            else:
                dl = 0
                content = b''
                total_length = int(total_length)
                d = float(1 << 20)
                total_dl = int((total_length / d))
                len_ = len(str(total_dl))
                for data in response.iter_content(chunk_size=2097152):
                    content += data
                    dl += len(data)
                    done = int(50 * dl / total_length)
                    show_dl = int((dl / d))
                    sys.stdout.write("\r[%s%s] %s%s / %s MB" % (
                        '=' * done, ' ' * (50 - done), show_dl, ' ' * (len_ - len(str(show_dl))), total_dl))
                    sys.stdout.flush()
        response.close()
        return content, response.cookies, response.headers
    except Exception as e:
        database.log(str(e))
        time.sleep(5)
        if times == 0:
            return send_request(link, False, False, times + 1)
        elif times == 1:
            return send_request(link, False, False, times + 1)
        else:
            return False


def check_files_downloaded(directory, episode):
    directory = directory.format(episode)
    if not (os.path.exists(directory + '.ass') or os.path.exists(directory + '.srt')):
        return False
    if os.path.exists(directory + '.mkv') or os.path.exists(directory + '.mp4'):
        ext = 'mkv'
        if os.path.exists(directory + '.mp4'):
            ext = 'mp4'
        d = data_handle.download_database.get_download(f"{directory}.{ext}")

        if d:
            return False
        return True

    return False


def check_is_exist(subs, episode):
    headers, cookies = get_init_header(), get_init_cookie()
    if isinstance(subs, list):
        for sub in subs:
            sub_link = sub["link"].format(episode)
            try:
                response = requests.get(sub_link, cookies=cookies, headers=headers, stream=True, timeout=30)
                sc = response.status_code
                response.close()
            except Exception as e:
                database.log(e)
                sc = 503

            if 200 <= sc < 300:
                return True
        return False
    elif isinstance(subs, str):
        sub_link = subs.format(episode)
        try:
            response = requests.get(sub_link, cookies=cookies, headers=headers, stream=True, timeout=30)
            sc = response.status_code
            response.close()
        except Exception as e:
            database.log(e)
            sc = 503

        if 200 <= sc < 300:
            return True
        return False
    else:
        sub_link = subs["link"].format(episode)
        try:
            response = requests.get(sub_link, cookies=cookies, headers=headers, stream=True, timeout=30)
            sc = response.status_code
            response.close()
        except Exception as e:
            database.log(e)
            sc = 503

        if 200 <= sc < 300:
            return True
    return False


def get_tree_files(out, base_dir=''):
    dirs = listdir(base_dir)
    for i in dirs:
        real_dir = join(base_dir, i)
        if isfile(real_dir):
            out += [real_dir]
        elif isdir(real_dir):
            out += get_tree_files(out, real_dir)
    return out


def download_sub(sub, directory, episode, offset=0):
    cookies = get_init_cookie()
    sub_query = sub["query"]
    sub_link = sub["link"]
    directory = directory.format(episode)
    if os.path.exists(directory + '.ass') or os.path.exists(directory + '.srt'):
        return True
    if not sub_link or sub_link == "No":
        return False
    link = sub_link.format(episode + offset)
    if not check_is_exist(link, episode):
        return False
    while True:
        if not link or link == "No":
            return False
        response, r_cookie, r_header = send_request(link, cookies=cookies)
        if not response:
            return False

        if not sub_query:
            break
        s_qs = sub_query.split('|')
        soup = BeautifulSoup(response, 'html.parser')
        links = soup.select(s_qs[0].format(episode + offset).strip())
        link = ''
        for l in links:
            link = l.get("href")
        for arg in r_cookie:
            cookies[arg.name] = arg.value
        sub_query = '|'.join(s_qs[1:])

    BASE_TEMP_DIR = '/\\temp'
    if not os.path.exists(BASE_TEMP_DIR):
        os.mkdir(BASE_TEMP_DIR)

    # g = BytesIO(response)
    # if zipfile.is_zipfile(g):
    #     archive_dir = BASE_TEMP_DIR + '\\subtitle_temp.zip'
    # else:
    #     archive_dir = BASE_TEMP_DIR + '\\subtitle_temp.rar'

    archive_dir = BASE_TEMP_DIR + '\\subtitle_temp' + guess_extension(
        r_header['content-type'].partition(';')[0].strip())

    with open(archive_dir, 'wb') as f:
        f.write(response)
    patoolib.extract_archive(archive_dir, outdir=BASE_TEMP_DIR + '\\')

    # if zipfile.is_zipfile(f):
    #     z = zipfile.ZipFile(f)
    # else:
    #     rarfile.RarFile.UNRAR_TOOL = 'D:\\programming\\scripts\\one_peace_video_player\\download\\UnRARDLL.exe'
    #     z = rarfile.RarFile(f)
    # names = z.namelist()

    # names = [f for f in listdir(BASE_TEMP_DIR) if isfile(join(BASE_TEMP_DIR, f))]

    names = []
    names = get_tree_files(names, BASE_TEMP_DIR)
    ext = 'ass'
    index = 0
    for i in range(len(names)):
        if names[i].endswith('.ass'):
            ext = 'ass'
            index = i
            break
        elif names[i].endswith('.srt'):
            ext = 'srt'
            index = i
            break
    with open(names[index], 'rb') as sub:
        with open(f'{directory}.{ext}', 'wb') as f:
            f.write(sub.read())
    shutil.rmtree(BASE_TEMP_DIR)

    return True


def download_video(video, directory, episode, callback=lambda: None, sync=False, offset=0):
    video_link = video["link"]
    directory = directory.format(episode) + '.' + video_link[-3:]
    link = video_link.format(episode + offset)
    if os.path.exists(directory):
        d = data_handle.download_database.get_download(directory)
        if not d:
            return True

    database.log(f"downloading start {link}")
    video = DownloadManager.new(directory, link)
    video.set_callback(callback)
    return video.start(sync)


def download_all(video_link, sub_link, directory, episode, callback=lambda: None, sync=False):
    if check_files_downloaded(directory, episode):
        return True

    # elif not check_is_exist(video_link, episode):
    #     return False
    for sub in sub_link:
        offset = sub.get("offset")
        if not offset:
            offset = 0
        if download_sub(sub, directory, episode, offset=offset):
            database.log(f'{sub["link"].format(episode)} downloaded')
            break
    for video in video_link:
        offset = video.get("offset")
        if not offset:
            offset = 0
        if download_video(video, directory, episode, callback, sync, offset=offset):
            return True
    return False


def download_all_callback(video_link, sub_link, directory, episode, callback):
    return download_all(video_link, sub_link, directory, episode, callback=callback)


class Download:
    def __init__(self, directory, link):
        global headers
        global cookies
        self.dir = directory
        self.link = link
        self.callback = lambda: None
        self.is_stopped = True
        self.is_downloading = False
        self.times = -1
        self.use_proxy = False
        self.total = 0
        self.dl = 0
        self.headers = get_init_header()
        self.cookies = get_init_cookie()
        self.response = None
        self.file = None
        self.downloading_thread = None
        self.download_result = None
        self.set_pre_start_request()

    def cancel_download(self):
        self.stop()
        if self.downloading_thread and self.downloading_thread.is_alive():
            self.downloading_thread.join()
        data_handle.download_database.remove_download(self.dir)
        DownloadManager.remove_download(self.dir, self.link)

    def set_pre_start_request(self):
        if os.path.exists(self.dir):
            self.dl = os.path.getsize(self.dir)
        self.headers["Range"] = f'bytes={self.dl}-'

    def init_request(self):
        self.set_pre_start_request()
        if self.use_proxy:
            self.response = requests.get(self.link, stream=True, timeout=30, headers=self.headers, cookies=self.cookies,
                                         proxies=proxyDict)
        else:
            self.response = requests.get(self.link, headers=self.headers, cookies=self.cookies, stream=True, timeout=30)

        self.response.raise_for_status()
        self.total = self.response.headers.get('content-length')
        if self.total is None:
            self.response.close()
            raise RuntimeError("response is not file")

        self.total = int(self.total) + self.dl
        DownloadManager.set_download(self.dir, self.link)
        DownloadManager.set_download_len(self.dir, self.total)

    def start(self, sync=False):
        if self.downloading_thread and self.downloading_thread.is_alive():
            if sync:
                return
            self.downloading_thread.join()
            return self.download_result
        self.is_stopped = False
        self.times = -1
        self.downloading_thread = threading.Thread(target=self.download_file)
        self.downloading_thread.start()
        if sync:
            return
        self.downloading_thread.join()
        return self.download_result

    def real_download_file(self):
        try:
            self.init_request()
            self.is_downloading = True
            for data in self.response.iter_content(chunk_size=262144):
                self.file = open(self.dir, "ab")
                self.file.write(data)
                self.file.close()
                self.dl += len(data)
                if self.is_stopped or not database.get_app():
                    self.is_downloading = False
                    self.response.close()
                    return False
            if self.dl < self.total - 2:
                self.response.close()
                if self.file and not self.file.closed:
                    self.file.close()
                return self.download_file()

            self.response.close()
            self.file.close()
            data_handle.download_database.remove_download(self.dir)
            self.callback()
            return True
        except Exception as e:
            database.log(str(e))
            self.times += 1
            if self.file and not self.file.closed:
                self.file.close()
            if self.times in [0, 1]:
                self.download_file()
            else:
                self.stop()
                return False

    def download_file(self):
        self.download_result = self.real_download_file()

    def stop(self):
        self.is_stopped = True

    def set_callback(self, callback):
        self.callback = callback


class DownloadManager:
    downloads_data = {}
    download_list = []

    @staticmethod
    def init():
        DownloadManager.downloads_data = data_handle.download_database.get_download_all()
        for directory in DownloadManager.downloads_data:
            DownloadManager.download_list.append(Download(directory, DownloadManager.downloads_data[directory]["link"]))

    @staticmethod
    def new(directory, link):
        for download in DownloadManager.download_list:
            if download.dir == directory:
                if download.link == link:
                    return download
                else:
                    if download.dl == 0:
                        DownloadManager.download_list.remove(download)
                    else:
                        return download
        download = Download(directory, link)
        DownloadManager.download_list.append(download)

        return download

    @staticmethod
    def get_all():
        return DownloadManager.download_list

    @staticmethod
    def get_download(directory, link=''):
        for download in DownloadManager.download_list:
            if download.dir == directory and (not link or link == download.link):
                return download
        return False

    @staticmethod
    def set_download_len(directory, total_len):
        if DownloadManager.downloads_data.get(directory) and not DownloadManager.downloads_data[directory].get("total"):
            DownloadManager.downloads_data[directory]["total"] = total_len
            data_handle.download_database.set_download(directory, DownloadManager.downloads_data[directory])
        return DownloadManager.downloads_data[directory]["total"]

    @staticmethod
    def is_downloading(directory):
        dl = DownloadManager.get_download(directory)
        return dl.downloading_thread and dl.downloading_thread.is_alive()

    @staticmethod
    def set_download(directory, link):
        if DownloadManager.downloads_data.get(directory):
            return
        download_data = data_handle.download_database.get_download_init()
        download_data["link"] = link
        download_data["total"] = 0
        data_handle.download_database.set_download(directory, download_data)
        DownloadManager.downloads_data[directory] = download_data

    @staticmethod
    def remove_download(directory, link):
        for download in DownloadManager.download_list:
            if download.dir == directory and download.link == link:
                DownloadManager.download_list.remove(download)
                del DownloadManager.downloads_data[directory]
