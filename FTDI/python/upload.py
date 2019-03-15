import subprocess
import pandas as pd
import numpy as np
from glob import glob
import sqlalchemy
import re
import datetime


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
        self.timestring = re.match(
            '[0-9]*',
            re.search('[0-9]*\.dat', filename).group()).group()
        self.timestamp = datetime.datetime.strptime(
            self.timestring, "%Y%m%d%H%M%S")
        return datastring

    def getDataFrame(self):
        self.df = pd.DataFrame(
            self.data[1:], columns=self.data[0]).astype(float)
        return self.df

    def uploadDataToDB(self, dbname):
        if not hasattr(self, 'df'):
            self.getDataFrame()
        engine = sqlalchemy.create_engine(
            'sqlite:///'+dbname, echo=True)
        try:
            self.df.to_sql(self.timestring, con=engine)
        except ValueError:
            pass


def buildCCode(clean=False):
    if clean:
        subprocess.call(['make', 'clean'])
    subprocess.call(['make'])


def listTables(dbname):
    engine = sqlalchemy.create_engine('sqlite:///'+dbname, echo=True)
    return engine.table_names()


def dropTable(dbname, table):
    engine = sqlalchemy.create_engine('sqlite:///'+dbname, echo=True)
    engine.execute("DROP TABLE IF EXISTS '%s'" % table)


def main():
    buildCCode(clean=True)
    # # TODO: Make this command dynamic
    subprocess.call(['sudo',
                     'LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH',
                     '/home/dmonk/serenity-test-board/FTDI/bin/main', '-l'])
    files = glob('data/*.dat')
    data = Data(files[0])
    data.uploadDataToDB('data/db.sqlite')
    # for i in listTables('data/db.sqlite'):
    #     dropTable('data/db.sqlite', i)
    print(listTables('data/db.sqlite'))


if __name__ == '__main__':
    main()
