from os import listdir, path, stat
from sys import argv
from root import musicDir
from tag import getFilenameList
from subprocess import Popen


class AttributeContainer:
    pass


VALID_EXTENSIONS = ["mp3", "m4a", "flac", "ogg", "mka", "opus"]


def get_songs():

    if len(argv) > 1:
        return getFilenameList(argv[1])
    else:
        return [path.join(musicDir, f) for f in listdir(musicDir)]


def play_recent_songs(sorted_song_list):

    for sorted_song in sorted_song_list:
        if path.splitext(sorted_song)[1][1:].lower() in VALID_EXTENSIONS:
            Popen(path.normpath(sorted_song))


if __name__ == "__main__":

    SONG_LIMIT = 10
    initSongList = get_songs()

    acList = []
    for song in initSongList:
        ac = AttributeContainer()
        ac.song = song
        ac.stat = stat(song)
        acList.append(ac)

    sortedAcList = sorted(acList,
                          key=lambda AttributeContainer:
                          AttributeContainer.stat.st_ctime,
                          reverse=True)

    sortedSongList = [s.song for s in sortedAcList][:SONG_LIMIT]

    play_recent_songs(sortedSongList)
