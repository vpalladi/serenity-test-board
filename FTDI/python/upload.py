import subprocess
import pandas as pd
import numpy as np
from glob import glob


class Data:
    def __init__(self, filename):
        data = self.__openFile(filename).strip().split(',')
        data = [i for i in data if i]
        try:
            self.npoints = int(data[0])
            data = data[1:]
        except ValueError:
            pass
        self.data = np.array(data)
        self.data = self.data.reshape(int(self.data.size/(self.npoints+1)),
                                      int(self.npoints + 1))
        self.data = self.data.T

    def __openFile(self, filename):
        with open(filename) as f:
            datastring = f.read()
        return datastring

    def getDataFrame(self):
        self.df = pd.DataFrame(self.data[1:], columns=self.data[0])
        return self.df


def buildCCode(clean=False):
    if clean:
        subprocess.call(['make', 'clean'])
    subprocess.call(['make'])


def getData():
    files = glob('data/*.dat')
    data = Data(files[0])
    print(data.getDataFrame())


def main():
    buildCCode(clean=True)
    # TODO: Make this command dynamic
    subprocess.call(['sudo',
                     'LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH',
                     '/home/dmonk/serenity-test-board/FTDI/bin/main', '-l'])
    getData()


if __name__ == '__main__':
    main()
