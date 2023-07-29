from sideloader import startstore
import sys

if __name__ == '__main__':
    if len(sys.argv) >1:
        startstore(sys.argv[1])
    else:
        startstore()