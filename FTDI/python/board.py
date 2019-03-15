import subprocess
from glob import glob
from data import Data
import pandas as pd
import sqlalchemy


class Board:
    def __init__(self, ID):
        self.ID = ID

    def __uploadToBoardTable(self, df, dbname):
        engine = sqlalchemy.create_engine(
            'sqlite:///'+dbname, echo=True)
        self.df.to_sql('board_' + self.ID,
                       con=engine, if_exists='append',
                       index=False)

    def measure(self):
        # TODO: Make this command dynamic
        subprocess.call(
            ['sudo',
             'LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH',
             '/home/dmonk/serenity-test-board/FTDI/bin/main', '-l']
        )
        files = glob('data/*.dat')
        data = Data(self.ID, files[-1])
        data.getDataFrame()
        data.uploadDataToDB('data/db.sqlite')
        cols = ['timestamp'] + list(data.df.columns)
        row = [data.timestring] + list(data.df.mean().values)
        self.df = pd.DataFrame([row], columns=cols)
        self.__uploadToBoardTable(self.df, 'data/db.sqlite')

    def listMeasurements(self):
        engine = sqlalchemy.create_engine(
            'sqlite:///data/db.sqlite', echo=True)
        df = pd.read_sql("SELECT * FROM board_%s" % self.ID, con=engine)
        print(df)
