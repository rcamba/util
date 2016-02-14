from subprocess import Popen, PIPE
from sys import argv


def raise_invalid_args():

    err_msg = "Invalid arguments.\n"
    err_msg += "Usage checkhash.py file [[hash] or [checksum]]\n"
    err_msg += "Hash is set to MD5 if no argument is provided\n"
    raise ValueError(err_msg)


def check_hash(file, hash, checksum_val=None):
    check_hash_command = "CertUtil -hashfile {file} {hash}".format(
        file=file, hash=hash)

    proc = Popen(check_hash_command, stdout=PIPE, stderr=PIPE)
    output, err = proc.communicate()

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


if __name__ == "__main__":

    hash = "MD5"  # default
    checksum_val = None

    if len(argv) == 1:
        raise_invalid_args()

    elif len(argv) == 3:
        if len(argv[2]) >= 32:  # if it's long assume it's a checksum...
            checksum_val = argv[2]
        else:
            hash = argv[2]

    elif len(argv) == 4:
        hash = argv[2]
        checksum_val = argv[3]

    elif len(argv) > 4:
        raise_invalid_args()

    file = argv[1]
    check_hash(file, hash, checksum_val)
