import subprocess
from glob import glob
from databasing import dropTable, listTables
from data import Data
from board import Board


def buildCCode(clean=False):
    if clean:
        subprocess.call(['make', 'clean'])
    subprocess.call(['make'])


def main():
    buildCCode(clean=True)
    board = Board('0')
    board.measure()
    print(listTables('data/db.sqlite'))


if __name__ == '__main__':
    main()
