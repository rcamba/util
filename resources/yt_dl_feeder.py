import argparse
import json
import os
import io
import time
import random
import subprocess
import urllib2

import requests
import clean_filenames

from bs4 import BeautifulSoup
from root import screening_dir, music_dir, get_all_page_links, \
    yt_dls_dir, yt_amv_dir, error_alert, deleted_screened_log, yt_dl_defaults_log, home_dir, \
    yt_dled_log


MAX_TRIES = 10
YT_DL_PROG = os.path.join(home_dir, "Downloads", "youtube-dl.exe")


def get_vid_title(vid_link):
    content = requests.get(vid_link).text
    soup = BeautifulSoup(content)
    vid_title = soup.title.string[:-len(" - YouTube")]
    return vid_title


def get_vid_list(links_list):
    vid_list = []

    for link in links_list:

        print "Retrieving video list from:", link

        i = 0
        page_links = get_all_page_links(link)

        while len(page_links) <= 1 and i < MAX_TRIES:
            page_links = get_all_page_links(link)
            i += 1
            print "Retry #", i
            time.sleep(random.randint(2, 6))

        if len(page_links) > 1:
            vid_list.extend(parse_yt_links(page_links))

    print "Found", len(vid_list), "links"

    return vid_list


def parse_yt_links(page_links):
    v_id_list = []
    for i in range(len(page_links) - 1, -1, -1):

        page_links[i] = page_links[i].get("href")
        if page_links[i] is not None:

            if "youtube" not in page_links[i]:
                page_links[i] = "youtube.com" + page_links[i]

            if "http" not in page_links[i]:
                page_links[i] = "http://" + page_links[i]

            try:
                base_url = page_links[i][:page_links[i].index("watch?") + 6]
                v_id = page_links[i][page_links[i].index("v="):]
                page_links[i] = base_url + v_id

                # try and slice off '&' options in the link
                # e.g: watch?v=IDHERE&list=PLAYLIST
                # slices off "&list=PLAYLIST"
                if page_links[i].find('&') > -1:
                    page_links[i] = page_links[i][:page_links[i].index('&')]

                # prevent duplicates
                if v_id not in v_id_list:
                    v_id_list.append(v_id)
                else:
                    page_links.remove(page_links[i])

            except (ValueError, IndexError):
                page_links.remove(page_links[i])

        else:
            page_links.remove(page_links[i])

    return page_links


def already_downloaded(title, targ_dir):
    ret_val = False
    f_list = [os.path.splitext(f)[0].lower() for f in os.listdir(unicode(targ_dir))]

    yt_dled_music_list = [y.lower() for y in io.open(yt_dled_log, encoding="utf-8").read().split('\n')]
    screened_music_list = [s.lower() for s in io.open(deleted_screened_log, encoding="utf-8").read().split('\n')]

    t = title.lower()
    if t in f_list or t in yt_dled_music_list or t in screened_music_list:
        ret_val = True
    return ret_val


def log_dled_song(title):
    with io.open(yt_dled_log, 'a', encoding="utf-8") as writer:
        writer.write(title)
        writer.write(u'\n')


def dl_single_song(vid_link, target_dir):
    yt_dl_opts = ("--quiet --no-mtime --audio-format best --audio-quality 0 --no-overwrites " +
                  "--extract-audio --output").split()
    vid_title = get_vid_title(vid_link)
    cleaned_vid_title = clean_filenames.clean_string(vid_title)
    vid_id = vid_link[vid_link.rindex("=") + 1:]

    file_title = "{t} {id}".format(t=cleaned_vid_title, id=vid_id)
    log_title = u"{t} {id}".format(t=vid_title, id=vid_id)

    clean_filenames.append_line_to_log(log_title.encode("utf-8") + ": " + file_title)

    yt_dl_output_file = "{td}\\{t}.%(ext)s".format(
        td=target_dir, t=file_title.encode("mbcs"))  # prev sys.getfilesystemencoding()

    dl_music_cmd = [YT_DL_PROG, vid_link] + yt_dl_opts + [yt_dl_output_file]

    if not already_downloaded(log_title, music_dir):
        print "Downloading:", file_title, "\n"
        proc = subprocess.Popen(dl_music_cmd)
        proc.wait()
        log_dled_song(log_title)

    else:
        error_alert(file_title + " already downloaded")


def load_default_multi_song_links():
    with open(yt_dl_defaults_log) as reader:
        d = json.load(reader)
    return d["default_multi_song_links"]


def dl_multi_song(vid_links=None):
    if vid_links is None:
        vid_links = load_default_multi_song_links()

    print "Downloading multiple songs from {}".format(vid_links)

    vid_list = get_vid_list(vid_links)

    for vid_link in vid_list:
        dl_single_song(vid_link, screening_dir)


def dl_single_video(vid_link, target_dir):
    yt_dl_opts = ("--quiet --rate-limit 100m  "
                  "--no-mtime --no-overwrites --output").split()
    yt_dl_output_file = "{target_dir}\\%(title)s_%(id)s.%(ext)s".format(
        target_dir=target_dir)

    dl_vid_cmd = [YT_DL_PROG, vid_link] + yt_dl_opts + [yt_dl_output_file]

    title = get_vid_title(vid_link)
    print "Downloading:", title

    proc = subprocess.Popen(dl_vid_cmd)
    proc.wait()


def load_default_multi_vid_links():
    with open(yt_dl_defaults_log) as reader:
        d = json.load(reader)
    return d["default_multi_vid_links"]


def dl_multi_video(vid_link=None):
    if vid_link is None:
        vid_link = load_default_multi_vid_links()

    print "Downloading multiple videos from {}".format(vid_link)

    vid_list = get_vid_list(vid_link)

    for vid in vid_list:
        dl_single_video(vid, yt_amv_dir)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-ss", "--single-song")
    group.add_argument("-sv", "--single-video")
    group.add_argument("-mv", "--multi-video", const="", nargs="?")
    group.add_argument("-ms", "--multi-song", const="", nargs="?")

    args = parser.parse_args()
    switches = []

    if args.single_song is not None:
        vid_link_ = urllib2.quote(args.single_song, safe="%/:=&?~#+!$,;'@()*[]")
        dl_single_song(vid_link_, music_dir)

    elif args.single_video is not None:
        vid_link_ = urllib2.quote(args.single_video, safe="%/:=&?~#+!$,;'@()*[]")
        dl_single_video(vid_link_, yt_dls_dir)

    elif args.multi_video is not None:
        if len(args.multi_video) > 0:
            vid_link_ = urllib2.quote(args.multi_video, safe="%/:=&?~#+!$,;'@()*[]")
            dl_multi_video(vid_link_)
        else:
            dl_multi_video()
    else:
        if args.multi_song is not None and len(args.multi_song) > 0:
            vid_link_ = urllib2.quote(args.multi_song, safe="%/:=&?~#+!$,;'@()*[]")
            dl_multi_song([vid_link_])
        else:
            dl_multi_song()
