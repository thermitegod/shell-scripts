#!/usr/bin/env python3
# 1.0.0
# 2019-10-23

# Original
# https://github.com/JLDevOps/ChanDL

# Copyright (C) 2017 Gian Sass <gian.sass@outlook.de>
# Copyright (C) 2019 Brandon Zorn <brandonzorn@cock.li>
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
import os
import re
import requests
import threading
import time

from urllib.parse import urlparse


board = None
chan = None
datapath = None
dest = None
ext = None
hashlist = []
thread = None
orig_filenames = False
url_folder_regex = '.*\\/([.\\w+]+[^.html])'

# Split a sequence into num chunks


def chunks(seq, num):
    avg = len(seq) / float(num)
    last = 0.0

    while last < len(seq):
        yield seq[int(last):int(last + avg)]
        last += avg


def parse_url(url):
    global chan
    parseurl = urlparse(url)
    print(parseurl)
    urldef = parseurl[2].split("/")[1:]

    board = urldef[0]

    if urldef[1] == "thread":
        chan = "4chan"
    elif urldef[1] == "res":
        chan = "8chan"
    else:
        chan = None

    if chan == "4chan" and len(urldef) == 4:
        del urldef[3]

    if chan == "8chan":
        threadurl = "https://8ch.net/"
    else:
        threadurl = "https://a.4cdn.org/"

    threadurl += "/".join(urldef)

    if threadurl.endswith(".html"):
        threadurl = threadurl.replace(".html", ".json")
    elif not threadurl.endswith(".json"):
        threadurl += ".json"

    return board, threadurl


def download_images_thread(images):
    for i in images:
        if not i["md5"] in hashlist:
            download_image(i)
            hashlist.append(i["md5"])


def download_image(post):
    global board, chan, dest, ext, orig_filenames, thread

    if post["md5"] in hashlist:
        return

    filename = post["filename"] if orig_filenames else str(post["tim"])
    extension = post["ext"]

    if "*" not in ext:
        if not any(e in extension for e in ext):
            return

    if chan == "8chan":
        url = "https://media.8ch.net/file_store/%s" % str(post["tim"]) + extension
    else:
        url = "https://i.4cdn.org/%s/%s" % (board, str(post["tim"]) + extension)
    path = os.path.join(dest, filename + extension)

    i = 1
    # Prevent duplicate filenames
    while os.path.isfile(path):
        path = os.path.join(dest, filename + "_" + str(i) + extension)
        i += 1

    print("%s -> '%s'" % (url, path))
    with open(path, "wb") as file:
        file.write(requests.get(url).content)


def write_hashlist():
    global datapath, hashlist

    with open(os.path.join(datapath, "hashlist"), "w") as f:
        for hash in hashlist:
            f.write("%s\n" % str(hash))


def gen_md5(path):
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return base64.b64encode(hash_md5.digest()).strip()


def gen_hashlist(d):
    for f in os.listdir(d):
        if not f.lower().endswith(('.png', '.jpg', '.jpeg', '.webm', '.gif', '.mp4', '.mkv')):
            continue
        hashlist.append(gen_md5(os.path.join(d, f)))
    write_hashlist()


def download_thread_data(url):
    r = requests.get(thread)
    if r.status_code == 404:
        print("API returned 404.")
        exit(0)
    else:
        return r


def mkdir_p(path):
    print(path)
    os.makedirs(path)


def init_datapath(top_dir):
    global datapath
    datapath = os.path.join(top_dir, ".chandl")
    if not os.path.exists(top_dir):
        mkdir_p(top_dir)
        mkdir_p(datapath)


def main():
    global board, datapath, dest, ext, hashlist, orig_filenames, thread, url_folder_regex

    parser = argparse.ArgumentParser()
    parser.add_argument('-url', "--url",
                        help="The URL of the thread you want to download (4chan and 8chan supported)")
    parser.add_argument('-d', "--destination",
                        help="Where the files are to be stored")
    parser.add_argument('-ext', "--extension",
                        default="*",
                        help="What file extensions to download, format: ext1,ext2;...")
    parser.add_argument('-t', "--threads",
                        default=multiprocessing.cpu_count(),
                        type=int,
                        help="How many threads to utilise",)
    parser.add_argument('-w', "--watch",
                        action='store_true',
                        help="Continually search for new images to download")
    parser.add_argument('-u', "--update-interval",
                        default=60,
                        type=int,
                        help="Interval in seconds after which to trigger a new poll update when enabled with -w")
    parser.add_argument('-o', "--original-filenames",
                        action='store_true',
                        help="Whether to use the original filename of the uploaded images")
    parser.add_argument('-gh', "--gen-hashlist",
                        default=None,
                        type=str,
                        help="Generate hashlist from directory")
    args = parser.parse_args()

    url = args.url

    if args.destination is None:
        dest = (re.findall(url_folder_regex, url))[0]
        print(dest)
    else:
        dest = args.destination

    threadcount = args.threads
    ext = str(args.extension).lower().split(',')
    orig_filenames = args.original_filenames
    watch = args.watch
    update_interval = args.update_interval

    if args.gen_hashlist is not None:
        init_datapath(args.gen_hashlist)
        print('here-gen_hashlist')
        gen_hashlist(args.gen_hashlist)
        exit(0)

    if url is None:
        print("Missing url")
        exit(1)

    if update_interval <= 0:
        print("Invalid update interval")
        exit(1)

    board, thread = parse_url(url)

    if thread.endswith(".html"):
        thread = thread.replace(".html", ".json")
    elif not thread.endswith(".json"):
        print("Invalid URL")
        exit(1)

    r = download_thread_data(thread)

    init_datapath(dest)

    if not os.path.exists(os.path.join(datapath, "hashlist")):
        open(os.path.join(datapath, "hashlist"), 'w').close()
    else:
        # Read hashlist
        with open(os.path.join(datapath, "hashlist"), "r") as f:
            hashlist = [line.rstrip('\n') for line in f.readlines()]

    # Collect all images into this array
    images = []

    for post in r.json()["posts"]:
        if "filename" in post:
            images.append(copy.deepcopy(post))
        if "extra_files" in post:
            for f in post["extra_files"]:
                images.append(copy.deepcopy(f))

    threads = []
    for c in chunks(images, threadcount):
        t = threading.Thread(target=download_images_thread, args=(c,))
        threads.append(t)
        t.daemon = True
        t.start()

    while threading.active_count() - 1 > 0:
        time.sleep(0.1)

    for t in threads:
        t.join()

    write_hashlist()

    if not watch:
        exit(0)

    print("Entering watch mode (update interval = %us)" % update_interval)

    while True:
        images = []

        r = download_thread_data(thread)
        posts = r.json()["posts"]
        # if posts[0].has_key("closed") and posts[0]["closed"] == 1:
        if "closed" in posts[0] and posts[0]["closed"] == 1:
            print("Thread is closed. Exiting.")
            exit(0)

        for post in posts:
            if "filename" in post:
                if post["md5"] not in hashlist:
                    images.append(copy.deepcopy(post))
            if "extra_files" in post:
                for f in post["extra_files"]:
                    if post["md5"] not in hashlist:
                        images.append(copy.deepcopy(f))

        download_images_thread(images)
        write_hashlist()
        time.sleep(float(update_interval))


if __name__ == "__main__":
    main()
