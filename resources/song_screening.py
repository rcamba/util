from os import path, remove as os_remove
from string import lower
from msvcrt import kbhit, getch
from shutil import move, Error as shutil_error
from sys import argv
from random import shuffle
from subprocess import Popen

from tag import getFilenameList, addTags, removeTags
from root import screeningDir, musicDir, deletedScreenedLog, errorAlert

from psutil import process_iter


def kill_VLC():

    vlc_killed = False
    for proc in process_iter():

        if proc.pid == glob_vlc_proc.pid:
            proc.kill()
            proc.wait()

            vlc_killed = True
            break

    if not vlc_killed:
        raise Exception(
            "Failed to kill VLC process. PID: {} not found".format(
                glob_vlc_proc.pid))


def get_key_press():

    prompt = ("Type [{keep}] to keep, [{tag}] to keep and tag, " +
              "[{lete}] to delete or " + "[{quit}] for quit").format(
              keep=KEEP_KEY, tag=TAG_KEY, lete=DELETE_KEY,
              quit=QUIT_KEY)
    print prompt

    result = ""
    while result == "":

        if kbhit():
            result = (getch())
            inputChar = ord(result)
            if(inputChar == 224 or inputChar == 0):
                getch()

    result = lower(result)
    return result


def confirmation_resume():

    print "Type 'continue' and press enter to resume"
    user_input = raw_input().lower()
    if user_input == "continue":
        return True
    else:
        print "You typed : ", user_input
        errorAlert("Type 'continue' and press enter to resume")
        return False


def split_dir(fileName):
    return path.split(fileName)[1]


def log_deleted_song(targ):
    writer = open(deletedScreenedLog, 'a')
    targ = path.splitext(path.split(targ)[1])[0]
    writer.write(targ)
    writer.write('\n')
    writer.close()


def handle_tagging(music_filename):

    try:
        move(music_filename, musicDir)
        removeTags(["screen"], music_filename, validate=False)

        filename = path.join(musicDir, split_dir(music_filename))
        tagList = raw_input("Enter tag(s). Separate with commas\n").split(',')
        addTags(tagList, filename)
        print ""

    except shutil_error, e:

        errorAlert(("{m} already exists in music directory." +
                    "\nDeleting {m}").format(m=music_filename))
        handle_delete(music_filename)


def handle_delete(music_filename):

    try:

        os_remove(music_filename)
        removeTags(["screen"], music_filename, validate=False)
        print "Delete successful\n"
        log_deleted_song(music_filename)

    except OSError, e:
        errorAlert(
            "Failed to delete file {}. No changes have been made.".format(
                music_filename))
        print e.message
        raise


def handle_keep(music_filename):

    try:
        move(music_filename, musicDir)
        removeTags(["screen"], music_filename, validate=False)
        print "Move successful\n"

    except shutil_error, e:

        errorAlert(
            "{m} already exists in music directory.\nDeleting {m}".format(
                m=music_filename))
        handle_delete(music_filename)


def start_screening(song_list):

    global glob_vlc_proc

    class Quit:
        def __init__(self):
            self.quit = False

        def set_to_true(self):
            self.quit = True

    q = Quit()

    for song in song_list:

        invalid_key_press = 0

        if q.quit is False:

            playMusicCommand = ([MEDIA_PLAYER_PROGRAM] +
                                MEDIA_PLAYER_OPTIONS + [song])

            glob_vlc_proc = Popen(playMusicCommand)

            print "Playing: ", song

            key_press = get_key_press()

            while key_press not in [KEEP_KEY, TAG_KEY, DELETE_KEY, QUIT_KEY]:
                print "Invalid selection"
                invalid_key_press += 1
                if invalid_key_press > 2:
                    confirm_resume = False
                    errorAlert("Too many invalid keypresses->Pausing")

                    while(confirm_resume is False):
                        confirm_resume = confirmation_resume()

                key_press = get_key_press()

            else:
                kill_VLC()

                char_func_mapping = {
                    KEEP_KEY: lambda: handle_keep(song),
                    DELETE_KEY: lambda: handle_delete(song),
                    TAG_KEY: lambda: handle_tagging(song),
                    QUIT_KEY: q.set_to_true
                }

                char_func_mapping[key_press]()
                song_list.remove(song)


def get_songs():

    song_list = getFilenameList(["screen"])
    shuffle(song_list)
    return song_list


if __name__ == "__main__":

    MEDIA_PLAYER_PROGRAM = "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"

    MEDIA_PLAYER_OPTIONS = "--qt-start-minimized --one-instance \
    --playlist-enqueue --playlist-autostart --no-crashdump -L".split()

    KEEP_KEY = 'k'
    TAG_KEY = 't'
    DELETE_KEY = 'd'
    QUIT_KEY = 'q'

    glob_vlc_proc = None

    song_list = get_songs()

    if len(song_list) > 0:
        start_screening(song_list)

    else:
        errorAlert("No music to be screened available")
