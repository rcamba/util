from subprocess import Popen, PIPE
from sys import argv, stdout, exit as sys_exit
from hashlib import md5, sha256, sha512
from string import lower
from zlib import crc32 as z_crc32
from os import path as os_path


# https://stackoverflow.com/a/5061842
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
        self.__digest = z_crc32(arg, self.__digest) & 0xffffffff


def raise_invalid_args():
    err_msg = "Usage: checkhash.py file [hash] [checksum]\n"
    err_msg += "Hash is set to MD5 if no argument is provided\n"
    err_msg += "If checksum is provided then display if it matches " \
               "the calculated checksum"
    print err_msg
    sys_exit(1)


def check_hash_certutil(file_, hash_, checksum_val=None):
    check_hash_command = "CertUtil -hashfile \"{file}\" {hash}".format(
        file=file_, hash=hash_)

    proc = Popen(check_hash_command, stdout=PIPE, stderr=PIPE)
    output, _ = proc.communicate()

    if "Error" in output:  # since error doesn't get sent to stderr
        raise Exception(output)

    else:
        checksum_line = output.split('\n')[1]
        checksum_line = checksum_line.replace(' ', '').strip()
        print checksum_line

        if checksum_val is not None:
            print checksum_val
            if checksum_val == checksum_line:
                print "Checksum matches"
            else:
                print "Checksum does not match"


def check_hash(file_, hash_, checksum_val=None):
    hash_func = None
    bytes_to_read = 4096

    if lower(hash_) == "md5":
        hash_func = md5()

    elif lower(hash_) == "sha256":
        hash_func = sha256()

    elif lower(hash_) == "sha512":
        hash_func = sha512()

    elif lower(hash_) == "crc32":
        hash_func = crc32()

    else:
        # feed it to certuil as backup
        print "Hash: {} not found. Feeding to Certutil.".format(hash_)
        check_hash_certutil(file_, hash_, checksum_val)

    file_size = os_path.getsize(file_)
    total_processed = 0
    prev_pct = 0

    if hash_func is not None:
        with open(file_, "rb") as reader:
            for chunk in iter(lambda: reader.read(bytes_to_read), b""):
                total_processed += len(chunk)
                hash_func.update(chunk)

                curr_pct = int(round(total_processed/(file_size * 1.0), 2) * 100)
                if prev_pct != curr_pct:
                    prev_pct = curr_pct
                    update_pct(str(curr_pct) + (1 - len(str(curr_pct))) * " " + "%")
        stdout.write("\b" * 4)
        checksum = hash_func.hexdigest()

        # print checksum
        if checksum_val is not None:
            print checksum == checksum_val

    return checksum


def update_pct(w_str):
    w_str = str(w_str)
    stdout.write("\b" * len(w_str))
    stdout.write(" " * len(w_str))
    stdout.write("\b" * len(w_str))
    stdout.write(w_str)
    stdout.flush()


if __name__ == "__main__":
    hash_ = "MD5"  # default
    checksum_val = None

    if len(argv) == 1 or any(map(lambda arg: "help" in arg, argv)):
        raise_invalid_args()

    elif len(argv) == 3:
        if len(argv[2]) >= 32:  # if it's long assume it's a checksum...
            checksum_val = argv[2]
        else:
            hash_ = argv[2]

    elif len(argv) == 4:
        hash_ = argv[2]
        checksum_val = argv[3]

    elif len(argv) > 4:
        raise_invalid_args()

    file_ = argv[1]
    print check_hash(file_, hash_, checksum_val)
    # check_hash_certutil(file_, hash_, checksum_val)
