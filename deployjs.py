import subprocess

GULP_CMD = 'cd webapp && gulp deploy && cd ..'


def build_with_gulp():
    if subprocess.call(GULP_CMD, shell=True) != 0:
        print "!!!"
        print "Run the command '{}' from root manually, and fix the error".format(GULP_CMD)
        print "!!!"
        exit(1)


def kick_off():
    build_with_gulp()


if __name__ == "__main__":
    kick_off()
