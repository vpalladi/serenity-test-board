import subprocess
from glob import glob
from data import Data


class Board:
    def __init__(self, ID):
        self.ID = ID

    def measure(self):
        # TODO: Make this command dynamic
        subprocess.call(
            ['sudo',
             'LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH',
             '/home/dmonk/serenity-test-board/FTDI/bin/main', '-l']
        )
        files = glob('data/*.dat')
        data = Data(self.ID, files[-1])
        data.uploadDataToDB('data/db.sqlite')
