"""
Using .py because .bat reads commas as a separator/delimiter
"""


if __name__ == "__main__":
    from prandom import setup_argparser, play_random
    parser_ = setup_argparser()
    play_random(parser_)
