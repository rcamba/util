import os
import re
import sys
import zlib
import hashlib
import subprocess


# https://stackoverflow.com/a/5061842
# noinspection PyPep8Naming
class crc32(object):
    name = 'crc32'
    digest_size = 4
    block_size = 1

    def __init__(self, arg=''):
        self.__digest = 0
        self.update(arg)

    def copy(self):
        copy = super(self.__class__, self).__new__(self.__class__)
        copy.__digest = self.__digest
        return copy

    def digest(self):
        return self.__digest

    def hexdigest(self):
        return '{:08x}'.format(self.__digest)

    def update(self, arg):
        self.__digest = zlib.crc32(arg, self.__digest) & 0xffffffff


def raise_invalid_args():
    err_msg = "Usage: checkhash.py file [hash] [checksum]\n"
    err_msg += "Hash is set to MD5 if no argument is provided\n"
    err_msg += "If checksum is provided then display if it matches " \
               "the calculated checksum"
    print err_msg
    sys.exit(1)


def get_hash_value_certutil(fname, hash_algorithm):
    check_hash_command = "CertUtil -hashfile \"{file}\" {hash}".format(
        file=fname, hash=hash_algorithm)

    proc = subprocess.Popen(check_hash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = proc.communicate()

    if "Error" in output:  # since error doesn't get sent to stderr
        raise Exception(output)

    else:
        checksum_line = output.split('\n')[1]
        checksum = checksum_line.replace(' ', '').strip()

    return checksum


def get_hash_value(fname, hash_algorithm):

    hash_func = None
    bytes_to_read = 32768  # 2 ** 15
    hash_algorithm = hash_algorithm.lower()

    if hash_algorithm in hashlib.algorithms:
        hash_func = getattr(hashlib, hash_algorithm)()

    elif hash_algorithm == "crc32":
        hash_func = crc32()

    file_size = os.path.getsize(fname) * 1.0
    total_processed = 0
    prev_pct = 0

    if hash_func is not None:
        with open(fname, "rb") as reader:
            for chunk in iter(lambda: reader.read(bytes_to_read), b""):
                total_processed += len(chunk)
                hash_func.update(chunk)

                curr_pct = int((total_processed / file_size) * 100)
                if prev_pct != curr_pct:
                    prev_pct = curr_pct
                    update_pct(str(curr_pct) + "%")
        checksum = hash_func.hexdigest()

    else:
        # feed it to certuil as backup
        print "Hash: {} not found. Feeding to Certutil.".format(hash_algorithm)
        checksum = get_hash_value_certutil(fname, hash_algorithm)

    return checksum


def update_pct(w_str):
    w_str = str(w_str)
    print " " * len(w_str) + "\r",
    print w_str + "\r",


def check_hash_in_dir(directory_, hash_algorithm="crc32"):
    f_list = [os.path.join(directory_, f) for f in os.listdir(directory_)]
    all_matched = True
    for f in f_list:

        hash_value = get_hash_value(f, hash_algorithm)

        sq_bracket_list = re.findall("\[\w+\]", os.path.split(f)[1])
        if len(sq_bracket_list) > 0:
            expected_hash = sq_bracket_list[-1].lower().replace("[", "").replace("]", "")
            match_str = get_match_str(hash_value, expected_hash)
            if all_matched and hash_value != expected_hash:
                all_matched = False

        else:
            match_str = ""
            all_matched = "N/A"

        print "{f}, {ha}: {hv}{m}".format(f=os.path.split(f)[1],
                                          ha=hash_algorithm.upper(), hv=hash_value.upper(), m=match_str)

    print "All matched:", all_matched


def get_match_str(hash_value, expected_hash_value):
    match = ""
    if expected_hash_value is not None:
        if expected_hash_value == hash_value:
            match += " match"
        else:
            match += " doesn't match " + expected_hash_value.upper()
    return match


if __name__ == "__main__":
    import time
    s = time.time()
    hash_algorithm_ = "MD5"  # default
    expected_hash_value_ = None

    if len(sys.argv) == 1 or any(map(lambda arg: "help" in arg, sys.argv)) or len(sys.argv) > 4:
        raise_invalid_args()
    elif len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
        check_hash_in_dir(sys.argv[1])

    else:
        # if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        #     hash_value_ = get_hash_value(sys.argv[1], hash_algorithm_)

        if len(sys.argv) == 3:
            if len(sys.argv[2]) > 6:  # hash_algorithmn_ names max len currently is 6 SHA___
                expected_hash_value_ = sys.argv[2].lower()
            else:
                hash_algorithm_ = sys.argv[2]

        elif len(sys.argv) == 4:
            hash_algorithm_ = sys.argv[2]
            expected_hash_value_ = sys.argv[3].lower()

        fname_ = sys.argv[1]
        hash_value_ = get_hash_value(fname_, hash_algorithm_)
        match_ = get_match_str(hash_value_, expected_hash_value_)

        print "{ha}: {hv}{m}".format(ha=hash_algorithm_.upper(), hv=hash_value_.upper(), m=match_)
