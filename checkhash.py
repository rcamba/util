from subprocess import Popen, PIPE
from sys import argv, exit as sys_exit
from hashlib import md5, sha256, sha512
from string import lower


def raise_invalid_args():

    err_msg = "Usage: checkhash.py file [hash] [checksum]\n"
    err_msg += "Hash is set to MD5 if no argument is provided\n"
    err_msg += "If checksum is provided then display if it matches " \
               "the calculated checksum"
    print err_msg
    sys_exit(1)


def check_hash_certutil(file_, hash_, checksum_val=None):
    check_hash_command = "CertUtil -hashfile {file} {hash}".format(
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

    else:
        # feed it to certuil as backup
        print "Hash: {} not found. Feeding to Certutil.".format(hash_)
        check_hash_certutil(file_, hash_, checksum_val)

    if hash_func is not None:
        with open(file_, "rb") as reader:
            for chunk in iter(lambda: reader.read(bytes_to_read), b""):
                hash_func.update(chunk)
        checksum = hash_func.hexdigest()

        print checksum
        if checksum_val is not None:
            print checksum == checksum_val


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
    check_hash(file_, hash_, checksum_val)
    # check_hash_certutil(file_, hash_, checksum_val)
