from sideloader import start
import sys

if __name__ == '__main__':
    if len(sys.argv) >1:
        start(sys.argv[1])
    else:
        start()