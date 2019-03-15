import subprocess
import pandas as pd
import sqlalchemy
from databasing import dropTable, listTables, viewTable
from board import Board


def buildCCode(clean=False):
    if clean:
        subprocess.call(['make', 'clean'])
    subprocess.call(['make'])


def createBoard(metadata):
    cols = ['ID', 'Version', 'Date Built']
    row = metadata
    df = pd.DataFrame([row], columns=cols)
    engine = sqlalchemy.create_engine(
        'sqlite:///data/db.sqlite', echo=True)
    df.to_sql('boards', con=engine, if_exists='append', index=False)


def main():
    # buildCCode(clean=True)
    board = Board('0')
    board.measure()
    print(listTables('data/db.sqlite'))
    # print(viewTable('data/db.sqlite', 'board_0'))
    board.listMeasurements()


if __name__ == '__main__':
    main()
