import sqlalchemy


def listTables(dbname):
    engine = sqlalchemy.create_engine('sqlite:///'+dbname, echo=True)
    return engine.table_names()


def dropTable(dbname, table):
    engine = sqlalchemy.create_engine('sqlite:///'+dbname, echo=True)
    engine.execute("DROP TABLE IF EXISTS '%s'" % table)


if __name__ == '__main__':
        for i in listTables('data/db.sqlite'):
            dropTable('data/db.sqlite', i)
