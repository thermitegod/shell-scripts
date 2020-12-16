# -*- coding: utf-8 -*-
# 2.7.0
# 2020-11-15

# Original
# https://github.com/JLDevOps/ChanDL

# Copyright (C) 2017 Gian Sass <gian.sass@outlook.de>
# Copyright (C) 2019,2020 Brandon Zorn <brandonzorn@cock.li>
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.


import argparse
import base64
import copy
import hashlib
import multiprocessing
import re
import sys
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from loguru import logger

from python.utils.check_env import CheckEnv


class Chandl:
    def __init__(self):
        self.board = None
        self.chan = None
        self.datapath = None
        self.dest = None
        self.ext = None
        self.hashlist = []
        self.thread = None
        self.orig_filenames = False
        self.url_folder_regex = '.*\\/([.\\w+]+[^.html])'
        self.update_interval = 60

    @staticmethod
    def chunks(seq, num):
        # Split a sequence into num chunks
        avg = len(seq) / float(num)
        last = 0.0

        while last < len(seq):
            yield seq[int(last):int(last + avg)]
            last += avg

    def parse_url(self, url):
        parseurl = urlparse(url)
        logger.debug(parseurl)
        urldef = parseurl[2].split('/')[1:]

        self.board = urldef[0]

        if urldef[1] == 'thread':
            self.chan = '4chan'
        elif urldef[1] == 'res':
            self.chan = '8kun'
        else:
            self.chan = None

        if self.chan == '4chan' and len(urldef) == 4:
            del urldef[3]

        if self.chan == '8kun':
            threadurl = 'https://8kun.top/'
        else:
            threadurl = 'https://a.4cdn.org/'

        threadurl += '/'.join(urldef)

        if threadurl.endswith('.html'):
            threadurl = threadurl.replace('.html', '.json')
        elif not threadurl.endswith('.json'):
            threadurl += '.json'

        return self.board, threadurl

    def download_images_thread(self, images):
        for i in images:
            if not i['md5'] in self.hashlist:
                self.download_image(i)
                self.hashlist.append(i['md5'])

    def download_image(self, post):
        if post['md5'] in self.hashlist:
            return

        filename = post['filename'] if self.orig_filenames else str(post['tim'])
        extension = post['ext']

        if '*' not in self.ext:
            if not any(e in extension for e in self.ext):
                return

        post_time = str(post['tim'])
        if self.chan == '8kun':
            url = f'https://media.8kun.top/file_store/{post_time}{extension}'
        else:
            url = f'https://i.4cdn.org/{self.board}/{post_time}{extension}'
        path = Path() / str(self.dest) / f'{filename}{extension}'

        i = 1
        # Prevent duplicate filenames
        while Path.is_file(path):
            path = Path() / str(self.dest) / f'{filename}_{str(i)}{extension}'
            i += 1

        logger.info(f'{url} -> \'{path}\'')
        with open(path, 'wb') as file:
            file.write(requests.get(url).content)

    def write_hashlist(self):
        hashlist_path = Path() / self.datapath / 'hashlist'
        with Path.open(hashlist_path, 'w') as f:
            for filehash in self.hashlist:
                f.write('%s\n' % str(filehash))

    @staticmethod
    def gen_md5(path):
        hash_md5 = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return base64.b64encode(hash_md5.digest()).strip()

    def gen_hashlist(self, d):
        for f in Path(d).iterdir():
            if not str(f).lower().endswith(('.png', '.jpg', '.jpeg', '.webm', '.gif', '.mp4', '.mkv')):
                continue
            self.hashlist.append(self.gen_md5(Path() / d / f))
        self.write_hashlist()

    def download_thread_data(self):
        plain_url = self.thread.strip('.json')
        r = requests.get(self.thread)
        if r.status_code == 404:
            logger.warning(f'API returned 404: \'{plain_url}\'')
            raise SystemExit
        else:
            logger.info(f'Downloading thread: \'{plain_url}\'')
            return r

    def init_datapath(self, top_dir):
        self.datapath = Path() / top_dir / '.chandl'
        if not Path.exists(Path(top_dir)):
            Path(top_dir).mkdir(parents=True, exist_ok=True)
            self.datapath.mkdir(parents=True, exist_ok=True)

    def thread_watcher(self):
        i = 0
        logger.info(f'Entering watch mode (update interval = {self.update_interval}s)')
        while True:
            i += 1
            logger.info(f'Number of times watch loop has run: {i}')

            images = []

            r = self.download_thread_data()
            posts = r.json()['posts']
            # if posts[0].has_key('closed') and posts[0]['closed'] == 1:
            if 'closed' in posts[0] and posts[0]['closed'] == 1:
                logger.info('Thread is closed. Exiting.')
                raise SystemExit

            for post in posts:
                if 'filename' in post:
                    if post['md5'] not in self.hashlist:
                        images.append(copy.deepcopy(post))
                if 'extra_files' in post:
                    for f in post['extra_files']:
                        if post['md5'] not in self.hashlist:
                            images.append(copy.deepcopy(f))

            self.download_images_thread(images)
            self.write_hashlist()
            time.sleep(float(self.update_interval))

    def run(self, args):
        url = args.url

        if args.destination is None:
            self.dest = (re.findall(self.url_folder_regex, url))[0]
            logger.info(self.dest)
        else:
            self.dest = args.destination

        threadcount = args.threads
        self.ext = str(args.extension).lower().split(',')
        self.orig_filenames = args.original_filenames
        watch = args.watch

        if args.gen_hashlist is not None:
            self.init_datapath(args.gen_hashlist)
            logger.info('here-gen_hashlist')
            self.gen_hashlist(args.gen_hashlist)
            raise SystemExit

        if url is None:
            logger.error('Missing url')
            raise SystemExit

        if args.update_interval:
            self.update_interval = args.update_interval
            if self.update_interval <= 0:
                logger.error('Invalid update interval')
                raise SystemExit

        self.board, self.thread = self.parse_url(url)

        if self.thread.endswith('.html'):
            self.thread = self.thread.replace('.html', '.json')
        elif not self.thread.endswith('.json'):
            logger.error('Invalid URL')
            raise SystemExit

        r = self.download_thread_data()

        self.init_datapath(self.dest)

        hashlist_path = Path() / self.datapath / 'hashlist'
        if not Path.exists(hashlist_path):
            Path.open(hashlist_path, 'w').close()
        else:
            # Read hashlist
            with Path.open(hashlist_path, 'r') as f:
                self.hashlist = [line.rstrip('\n') for line in f.readlines()]

        # Collect all images into this array
        images = []

        for post in r.json()['posts']:
            if 'filename' in post:
                images.append(copy.deepcopy(post))
            if 'extra_files' in post:
                for f in post['extra_files']:
                    images.append(copy.deepcopy(f))

        threads = []
        for c in self.chunks(images, threadcount):
            t = threading.Thread(target=self.download_images_thread, args=(c,))
            threads.append(t)
            t.daemon = True
            t.start()

        while threading.active_count() - 1 > 0:
            time.sleep(0.1)

        for t in threads:
            t.join()

        self.write_hashlist()

        if watch:
            self.thread_watcher()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', '--url',
                        help='The URL of the thread you want to download (4chan and 8kun supported)')
    parser.add_argument('-d', '--destination',
                        help='Where the files are to be stored')
    parser.add_argument('-ext', '--extension',
                        default='*',
                        help='What file extensions to download, format: ext1,ext2;...')
    parser.add_argument('-t', '--threads',
                        default=multiprocessing.cpu_count(),
                        help='How many threads to utilise')
    parser.add_argument('-w', '--watch',
                        action='store_true',
                        help='Continually search for new images to download')
    parser.add_argument('-u', '--update-interval',
                        type=int,
                        nargs=1,
                        help='Interval in seconds after which to trigger a new poll update when enabled with -w')
    parser.add_argument('-o', '--original-filenames',
                        action='store_true',
                        help='Whether to use the original filename of the uploaded images')
    parser.add_argument('-gh', '--gen-hashlist',
                        default=None,
                        type=str,
                        help='Generate hashlist from directory')
    debug = parser.add_argument_group('DEBUG')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    CheckEnv.args_required_else_help()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    run = Chandl()
    run.run(args)
