import argparse
import os
import prandom


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tags", type=str, nargs='*', help="tags split by comma")
    parser.add_argument("-n", "--num", type=int, default=10, help="number of songs to play", dest="num_of_songs")
    parser.add_argument("-v", "--verbose", action="store_true", help="display play count info")

    args = parser.parse_args()
    args.tags = [t.strip() for t in " ".join(args.tags).split(",") if len(t) > 0]

    if len(args.tags) > 0:
        song_list = prandom.get_song_list_from_tag(args.tags)
    else:
        song_list = prandom.get_song_list()

    sorted_song_list = sorted(song_list,
                              key=lambda song:
                              os.stat(song).st_ctime,
                              reverse=True)
    sliced_sorted_song_list = sorted_song_list[:args.num_of_songs]
    if args.verbose:
        for s in sliced_sorted_song_list[:args.num_of_songs]:
            print s + ", " + str(os.stat(s).st_ctime)
        print args
        print "# of songs", len(sliced_sorted_song_list)

    prandom.update_song_log(sliced_sorted_song_list)
    prandom.play_songs(sliced_sorted_song_list)
