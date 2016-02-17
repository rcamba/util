from os import listdir, path, getcwd
from string import rstrip, strip, lower
from random import randint
from operator import attrgetter
from sys import argv, stdin
from subprocess import Popen

from root import musicDir, switchParser, songLogFile, pipedList, errorAlert, \
    prandomExceptions
from tag import getFilenameList, getMixedFilenameList

VALID_EXTENSIONS = ["mp3", "m4a", "flac", "ogg", "mka"]
AVAILABLE_SWITCHES = ['#', 'e', 'm']


class SongLogHandler:

    def __init__(self, songs_log_file):
        self.songs_log_file = songs_log_file
        self.load_log(songs_log_file)
        self.song_log_list = []

    def log_songs(self, song_list):
        song_list = map(lower, song_list)
        for song in song_list:
            for songLog in self.song_log_list[:]:
                if song == songLog.filename:
                    songLog.playCount = int(songLog.playCount) + 1
                    break
            else:  # song not found in songLogList i.e first time played
                new_song_log = SongLog(song, 1)
                self.song_log_list.append(new_song_log)

        self.song_log_list.sort(key=attrgetter("playCount"), reverse=True)

        writer = open(self.songs_log_file, 'w')
        for songLog in self.song_log_list:
            writer.write(songLog + "\n")
        writer.close()

    def load_log(self, songs_log_file):
        reader = open(songs_log_file)
        self.song_log_list = map(rstrip, reader.readlines())
        for i in range(0, len(self.song_log_list)):
            token = self.song_log_list[i].split('=')
            self.song_log_list[i] = SongLog(token[0], token[1])

    def reload(self):
        self.load_log(self.songs_log_file)


class SongLog:

    def __init__(self, new_filename, new_play_count):
        self.filename = new_filename
        self.playCount = int(new_play_count)

    def __add__(self, other):
        if type(other) == int:
            self.playCount = self.playCount + other
            return self.__str__()
        else:
            return self.__str__() + str(other)

    def __str__(self):
        return self.filename + "=" + str(self.playCount)


def prune_song_list(song_list):
    # Iterate through a copy to avoid skipping items or doing reverse iteration
    for song in song_list[:]:
        song_extension = path.splitext(song)[1][1:]
        if song_extension not in VALID_EXTENSIONS:
            song_list.remove(song)

    return song_list


def get_song_list(music_dir):
    """
    Return list of songs with full path
    :param music_dir: directory to list music from
    """

    def create_full_path(filename):  # helper function for map function
        return lower(music_dir + "\\" + filename)

    song_list = listdir(music_dir)

    song_list = prune_song_list(song_list)
    song_list = map(create_full_path, song_list)

    return song_list


def get_song_list_from_tag(tag_list):

    tag_list = map(strip, tag_list)

    if 'm' in switches:
        print "Getting mixed tags: ", tag_list
        song_list = getMixedFilenameList(tag_list)
    else:
        song_list = getFilenameList(tag_list)

    if len(song_list) == 0:
        errorAlert("No file list available for given tag(s)")

    return song_list


def prune_exceptions(song_list, switches, default=True):

    if default:
        # ... default exceptions
        # TODO probably get rid of this
        exec("exception_list=" + open(prandomExceptions).read())
    else:
        exception_list = []

    exception_song_list = []

    if 'e' in switches:  # exception, i.e don't play songs with this tag
        exception_list.extend(switches['e'].split(','))

    for exception in exception_list:
        exception_song_list.extend(getFilenameList(exception))

    for exceptionSong in exception_song_list:
        # if tag is given, songList may not have exceptionSong
        # when no tag is given, all songs are in songList so
        # exceptionSong will always be in it
        if exceptionSong in song_list:
            song_list.remove(exceptionSong)

    return song_list


def play_songs(song_list):

    for song in song_list:
        Popen(song, shell=True)


def random_select(song_list, max_songs):

    final_song_list = []

    for i in range(0, max_songs):
        sel = randint(0, len(song_list) - 1)
        final_song_list.append(song_list[sel])
        song_list.remove(song_list[sel])

    return final_song_list


def get_max_songs(argv, switches, song_list):

    if '#' in switches:
        max_songs = int(switches['#'])

    elif len(argv) > 1 and len(song_list) < 60:
        max_songs = len(song_list)

    else:
        max_songs = 60

    return max_songs


def handle_piping():

    song_list = pipedList("".join(map(str, stdin.readlines())))

    i = 0
    for f in song_list[:]:  # prune
        if path.isabs(f) is False:
            song_list[i] = getcwd() + "\\" + song_list[i]
        ext = path.splitext(f)[1][1:]
        if ext not in VALID_EXTENSIONS:
            print "{} not a valid extension. Removing {} from list".format(
                ext, song_list[i])
            song_list.remove(f)
        i += 1
    return song_list


def main():

    if stdin.isatty() is False:  # for using with nf/search
        print "Playing piped songs"
        pruned_song_list = handle_piping()
        max_songs = len(pruned_song_list)
    else:
        if len(argv) > 1:
            song_list = get_song_list_from_tag(
                " ".join(map(str, argv[1:])).split(','))
            pruned_song_list = prune_exceptions(song_list, switches,
                                                default=False)
        else:
            song_list = get_song_list(musicDir)
            pruned_song_list = prune_exceptions(song_list, switches)

        max_songs = get_max_songs(argv, switches, pruned_song_list)

    final_song_list = random_select(pruned_song_list, max_songs)

    slh = SongLogHandler(songLogFile)
    slh.log_songs(final_song_list)

    play_songs(final_song_list)

if __name__ == "__main__":

    switches = switchParser(argv)
    main()
