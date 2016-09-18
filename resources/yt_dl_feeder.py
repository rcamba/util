from time import sleep
from os import listdir, path, remove
from sys import argv
from clean_filenames import clean_string
from urllib2 import quote
from subprocess import Popen
from random import randint

from root import screeningDir, musicDir, switchParser, getAllPageLinks, \
    yt_dls_dir, yt_amv_dir, outputFromCommand, errorAlert, deletedScreenedLog

"""
-m: single music
no switches: multiple music
-s; single video
-v: multiple video
"""


def rand_sleep():
    sleep(randint(2, 6))


def get_dry_title(_vid_link):
    yt_dl_opts = ("-q -s --get-filename --extract-audio "
                  "--restrict-filenames --output ").split()
    output_format = "%(title)s_%(id)s.%(ext)s"
    title_cmd = [YT_DL_PROG, _vid_link] + yt_dl_opts + [output_format]
    title = outputFromCommand(title_cmd)
    return title


def get_vid_list(links_list):
    vid_list = []

    for link in links_list:

        print "Retrieving video list from: ", link

        i = 0
        page_links = getAllPageLinks(link)

        while len(page_links) <= 1 and i < MAX_TRIES:
            page_links = getAllPageLinks(link)
            i += 1
            print "Retry #", i
            rand_sleep()

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
                v_ID = page_links[i][page_links[i].index("v="):]
                page_links[i] = base_url + v_ID

                # try and slice off '&' options in the link
                # e.g: watch?v=IDHERE&list=PLAYLIST
                # slices off "&list=PLAYLIST"
                if page_links[i].find('&') > -1:
                    page_links[i] = page_links[i][:page_links[i].index('&')]

                # prevent duplicates
                if v_ID not in v_id_list:
                    v_id_list.append(v_ID)
                else:
                    page_links.remove(page_links[i])

            except (ValueError, IndexError):
                page_links.remove(page_links[i])

    return page_links


def already_downloaded(title, targ_dir):
    ret_val = False
    f_list = listdir(targ_dir)
    t = path.splitext(title)[0].lower()
    for f in f_list:
        if t == path.splitext(f)[0].lower():
            ret_val = True
            break

    return ret_val


def apply_convert_command(song_path):
    if path.splitext(song_path)[1] in [".mp4", ".mp3", ".m4a"]:
        convert_prog = "ffmpeg"
        convert_args = ("-y -loglevel panic -i {in_file} -f mp3 " +
                        "-ab 192000 -vn {out_file}").split()

        out_pos = convert_args.index("{out_file}")
        convert_args[out_pos] = convert_args[out_pos].format(
            out_file=song_path.replace(".mp4", ".mp3").replace(".m4a", ".mp3"))

        in_pos = convert_args.index("{in_file}")
        convert_args[in_pos] = convert_args[in_pos].format(in_file=song_path)

        print "Converting :", song_path

        convert_args.insert(0, convert_prog)
        convert_cmd = convert_args

        proc = Popen(convert_cmd, shell=True)
        proc.communicate()
        if proc.returncode == 0:
            try:
                remove(song_path)
            except WindowsError:
                errorAlert("Can't delete " + song_path)

    else:
        errorAlert(("Unable to convert file {}\n" +
                    "  Extension not accepted\n").format(song_path))


def dl_single_song(vid_link, target_dir):
    deleted_music_list = open(deletedScreenedLog).read().split('\n')

    yt_dl_opts = ("--quiet --restrict-filenames --no-mtime --no-overwrites " +
                  "--extract-audio --output").split()
    yt_dl_output_file = "{target_dir}\\%(title)s_%(id)s.%(ext)s".format(
        target_dir=target_dir)

    dl_music_cmd = [YT_DL_PROG, vid_link] + yt_dl_opts + [yt_dl_output_file]

    title = get_dry_title(vid_link)

    if len(title) > 0:

        title = clean_string(title)
        if already_downloaded(title, musicDir) is False:
            if path.splitext(title.lower())[0] not in deleted_music_list:
                print "\nDownloading:", title
                song_full_path = "{t1}\\{t2}".format(t1=target_dir, t2=title)

                proc = Popen(dl_music_cmd)
                proc.wait()

                apply_convert_command(song_full_path)

            else:
                errorAlert(title + " already screened and deleted before")
        else:
            errorAlert(title + " already in main music directory")
    else:
        errorAlert("Empty title for " + vid_link)


def dl_multi_song(vid_links=["https://www.reddit.com/r/japanesemusic",
                             "https://www.reddit.com/r/animemusic/",
                             "https://www.reddit.com/r/vocaloid"]):
    print "Downloading multiple songs from {}".format(vid_links)

    vid_list = get_vid_list(vid_links)

    for vid_link in vid_list:
        if vid_link is not None:
            dl_single_song(vid_link, screeningDir)


def dl_single_video(vid_link, target_dir):
    yt_dl_opts = ("--quiet --rate-limit 100m  "
                  "--no-mtime --no-overwrites --output").split()
    yt_dl_output_file = "{target_dir}\\%(title)s_%(id)s.%(ext)s".format(
        target_dir=target_dir)

    dl_vid_cmd = [YT_DL_PROG, vid_link] + yt_dl_opts + [yt_dl_output_file]

    title = get_dry_title(vid_link)
    print "Downloading:", title

    proc = Popen(dl_vid_cmd)
    proc.wait()


def dl_multi_video(_vid_link="http://www.reddit.com/r/amv"):
    print "Downloading multiple videos from {}".format(_vid_link)

    vid_list = get_vid_list([_vid_link])

    for vid in vid_list:
        if vid is not None:
            dl_single_video(vid, yt_amv_dir)


if __name__ == "__main__":

    MAX_TRIES = 10
    YT_DL_PROG = "C:\\Users\\Kevin\\Downloads\\youtube-dl.exe"
    AVAILABLE_SWITCHES = ['s', 'v', 'm']

    switches = switchParser(argv, AVAILABLE_SWITCHES)
    if len(switches) > 1:
        raise Exception("More than one switch found: {}. ".format(switches) +
                        "Only one switch at a time.")

    char_func_mapping = {
        's': lambda: dl_single_video(vid_link, yt_dls_dir),

        'v': lambda:
        dl_multi_video(vid_link) if len(vid_link) > 0 else dl_multi_video(),

        'm': lambda: dl_single_song(vid_link, musicDir),

        '': lambda:
        dl_multi_song([vid_link]) if len([vid_link]) > 0 else dl_multi_song()
    }

    opt = ""
    vid_link = ""
    if len(switches) > 0:
        opt = switches.keys()[0]
        if len(argv) > 1:
            vid_link = quote(argv[1], safe="%/:=&?~#+!$,;'@()*[]")

    elif len(argv) > 1:
        vid_link = quote(argv[1], safe="%/:=&?~#+!$,;'@()*[]")

    char_func_mapping[opt]()
