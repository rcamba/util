import argparse
import json
# from collections import OrderedDict
import collections
import os
import random
import sys
import subprocess
import ast

import root
import tag


valid_extensions = [
    ".aac", ".aiff", ".flac", ".m4a", ".m4b", ".mka", ".mp3", ".mpc", ".ogg", ".oga", ".mogg",
    ".opus", ".wav", ".wma", ".wv", ".webm"]


def remove_invalid_ext(file_list):
    for song in file_list:
        if not os.path.isfile(song) or os.path.splitext(song)[1] not in valid_extensions:
            file_list.remove(song)
    return file_list


def get_song_list(targ_dir=root.music_dir):
    file_list = [os.path.join(targ_dir, song).lower() for song in os.listdir(targ_dir)]
    song_list = remove_invalid_ext(file_list)
    return song_list


def get_song_list_from_tag(tag_list, mix_tags=False):
    if mix_tags:
        print "Mixed tags enabled"
        song_list = tag.get_mixed_files_from_tags(tag_list)  # TODO even out distrib?
    else:
        song_list = tag.get_files_from_tags(tag_list)

    if len(song_list) == 0:
        root.error_alert("No file list available for given tag(s)", raise_exception=True)

    return song_list


def prune_exceptions(song_list, use_default_exceptions=True):

    exception_tag_list = []
    exception_song_list = []

    if use_default_exceptions:
        exception_tag_list.extend(ast.literal_eval(open(root.prandom_exceptions_log).read()))

    if len(args.exception_tags) > 0:
        exception_tag_list.extend(args.exception_tags)

    for exception in exception_tag_list:
        exception_song_list.extend(tag.get_files_from_tags(exception))

    for exception_song in exception_song_list:
        # if tag is given, song_list_ may not have exception_song
        # when no tag is given, all songs are in songList so
        # exceptionSong will always be in it
        if exception_song in song_list:
            song_list.remove(exception_song)

    return song_list


def load_song_log_dict():
    with open(root.song_log_file) as reader:
        song_log_dict = json.load(reader)
    return song_log_dict


def update_song_log(song_list):
    song_log_dict = load_song_log_dict()
    for song in song_list:
        if song in song_log_dict:  # should by default have play_count key
            song_log_dict[song]["play_count"] += 1
        else:
            song_log_dict[song] = {
                "play_count": 1
            }

    # noinspection PyArgumentList
    ordered_song_dict = collections.OrderedDict(sorted(song_log_dict.items(), key=lambda item: item[1], reverse=True))

    with open(root.song_log_file, 'w') as writer:
        json.dump(ordered_song_dict, writer, indent=2)


def play_songs(song_list):
    for song in song_list:
        subprocess.Popen(song, shell=True)


def random_distrib_select(song_list, songs_limit):
    song_log_dict = load_song_log_dict()
    song_list.sort(key=lambda k: song_log_dict[k]["play_count"] if k in song_log_dict else -1, reverse=True)

    final_song_list_ = []
    select_low_play_count_chance = 0.80
    for i in range(0, min(len(song_list), songs_limit)):
        chance = random.random()
        if chance <= select_low_play_count_chance:
            selected_index = random.randint(int(len(song_list) * select_low_play_count_chance), len(song_list) - 1)
        else:
            selected_index = random.randint(0, len(song_list) - 1)

        song = song_list[selected_index]
        final_song_list_.append(song)
        song_list.pop(selected_index)

        if args.verbose:
            pc = 0
            if song in song_log_dict:
                pc = song_log_dict[song]["play_count"]

            print os.path.split(song)[1], "=", pc
            print args
            print "# of songs", len(final_song_list_)

    return final_song_list_


def handle_piping():
    item_list = root.list_from_piped(sys.stdin.readlines())
    song_list = remove_invalid_ext(item_list)
    return song_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tags", type=str, nargs='*', help="tags split by comma")

    parser.add_argument("-n", "--num", type=int, default=30, help="number of songs to play", dest="num_of_songs")
    parser.add_argument("-m", "--mix", action="store_true", help="mix tags", dest="mix_tags")
    parser.add_argument("-e", "--except", nargs='+', default=[], help="mix tags", dest="exception_tags")
    parser.add_argument("-v", "--verbose", action="store_true", help="display play count info")

    args = parser.parse_args()
    args.tags = [t.strip() for t in " ".join(args.tags).split(",") if len(t) > 0]
    args.exception_tags = [et for et in " ".join(args.exception_tags).split(",") if len(et) > 0]

    num_of_songs = args.num_of_songs

    if sys.stdin.isatty() is False:
        print "Processing pipes"
        pruned_song_list = handle_piping()
        print "Playing " + str(len(pruned_song_list)) + " piped songs"

    else:
        if len(args.tags) > 0:
            song_list_ = get_song_list_from_tag(args.tags, args.mix_tags)
            pruned_song_list = prune_exceptions(song_list_, use_default_exceptions=False)

        else:
            song_list_ = get_song_list(root.music_dir)
            pruned_song_list = prune_exceptions(song_list_)

    final_song_list = random_distrib_select(pruned_song_list, num_of_songs)
    update_song_log(final_song_list)
    play_songs(final_song_list)
