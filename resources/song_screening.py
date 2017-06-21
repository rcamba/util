from os import path, remove as os_remove
from msvcrt import kbhit, getch
from shutil import move, copy, Error as Shutil_error
from random import shuffle
from subprocess import Popen

from tag import get_files_from_tags, add_tags, remove_file_from_tags
from root import music_dir, deleted_screened_log, error_alert, get_media_player_path

from psutil import process_iter


def kill_vlc():
    vlc_killed = False
    for proc in process_iter():
        if proc.pid == glob_vlc_proc_pid:
            proc.kill()
            proc.wait()

            vlc_killed = True
            break

    if not vlc_killed:
        raise Exception(
            "Failed to kill VLC process. PID: {} not found".format(
                glob_vlc_proc_pid))


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
            input_char = ord(result)
            if input_char == 224 or input_char == 0:
                getch()

    result = result.lower()
    return result


def confirmation_resume():
    print "Type 'continue' and press enter to resume"
    user_input = raw_input().lower()
    if user_input == "continue":
        return True
    else:
        print "You typed : ", user_input
        error_alert("Type 'continue' and press enter to resume")
        return False


def slice_off_dir(fname):
    return path.split(fname)[1]


def log_deleted_song(targ):
    writer = open(deleted_screened_log, 'a')
    filename_only = slice_off_dir(targ)
    filename_only_no_ext = path.splitext(filename_only)[0]
    writer.write(filename_only_no_ext)
    writer.write('\n')
    writer.close()


def handle_tagging(screen_fname):

    try:
        copy(screen_fname, music_dir)

        music_fname = path.join(music_dir, slice_off_dir(screen_fname))
        tag_list = raw_input("Enter tag(s). Separate with commas\n").split(',')
        tag_list = map(str.strip, tag_list)
        add_tags(tag_list, music_fname, verbose=True)
        kill_vlc()
        handle_delete(screen_fname)

    except Shutil_error:
        error_alert(("{m} already exists in music directory." +
                     "\nDeleting {m}").format(m=screen_fname))
        handle_delete(screen_fname)


def handle_delete(music_filename):

    try:
        remove_file_from_tags(["screen"], music_filename)
        os_remove(music_filename)
        print "Deleted {mf}\n".format(mf=music_filename)
        log_deleted_song(music_filename)

    except OSError, e:
        error_alert("Failed to delete file {}. No changes have been made.".format(
            music_filename))
        print e.message
        raise


def handle_keep(music_filename):

    try:
        remove_file_from_tags(["screen"], music_filename)
        move(music_filename, music_dir)
        print "Moving complete\n"

    except Shutil_error:
        error_alert("{m} already exists in music directory.\nDeleting {m}".format(
            m=music_filename))
        handle_delete(music_filename)


def screen_songs(song_list):

    global glob_vlc_proc_pid

    stop_screening = False
    for song in song_list:

        invalid_key_press = 0
        if stop_screening is False:

            play_music_command = ([MEDIA_PLAYER_PROGRAM] +
                                  MEDIA_PLAYER_OPTIONS + [song])

            glob_vlc_proc_pid = Popen(play_music_command).pid

            print "Playing: ", song

            key_press = get_key_press()
            while key_press not in [KEEP_KEY, TAG_KEY, DELETE_KEY, QUIT_KEY]:
                print "Invalid selection"
                invalid_key_press += 1
                if invalid_key_press > 2:
                    confirm_resume = False
                    error_alert("Too many invalid keypresses; Pausing")

                    while confirm_resume is False:
                        confirm_resume = confirmation_resume()

                key_press = get_key_press()

            else:
                char_func_mapping = {
                    KEEP_KEY: lambda: handle_keep(song),
                    DELETE_KEY: lambda: handle_delete(song),
                    TAG_KEY: lambda: handle_tagging(song),
                }

                if key_press != TAG_KEY:  # handle_tagging calls kill_vlc since vlc will be playing while tagging
                    kill_vlc()

                if key_press == QUIT_KEY:
                    stop_screening = True
                else:
                    char_func_mapping[key_press]()
                    song_list.remove(song)


if __name__ == "__main__":

    MEDIA_PLAYER_PROGRAM = get_media_player_path()

    MEDIA_PLAYER_OPTIONS = "--qt-start-minimized " \
                           "--playlist-enqueue --playlist-autostart --no-crashdump -L".split()

    KEEP_KEY = 'k'
    TAG_KEY = 't'
    DELETE_KEY = 'd'
    QUIT_KEY = 'q'

    glob_vlc_proc_pid = None

    song_list_ = get_files_from_tags(["screen"])
    shuffle(song_list_)

    if len(song_list_) > 0:
        screen_songs(song_list_)

    else:
        error_alert("No music to be screened available")
