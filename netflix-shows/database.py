from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
from databases import Database
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

DB_USER = config['database'].get('user')
DB_PASSWORD = config['database'].get('password')
DB_HOST = config['database'].get('host')
DB_PORT = config['database'].getint('port')
DB_NAME = config['database'].get('name')
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class ShowsDB(object):
    def __init__(self):
        self.database = Database(url=DATABASE_URL)
        self.metadata = MetaData()
        self.shows = Table(
            'shows',
            self.metadata,
            Column('show_id', Integer, primary_key=True),
            Column('type', String, nullable=True),
            Column('title', String, nullable=True),
            Column('director', String, nullable=True),
            Column('cast', String, nullable=True),
            Column('country', String, nullable=True),
            Column('date_added', Date, nullable=True),
            Column('release_year', Integer, nullable=True),
            Column('rating', String, nullable=True),
            Column('duration', String, nullable=True),
            Column('listed_in', String, nullable=True),
            Column('description', String, nullable=True)
        )

    def initialize(self):
        engine = create_engine(DATABASE_URL)
        self.metadata.create_all(engine)
        return self

    def connect(self):
        return self.database.connect()

    def disconnect(self):
        return self.database.disconnect()

    def execute(self, query, get='all'):
        if get != 'all':
            return self.database.fetch_one(query)
        return self.database.fetch_all(query)

    def fetch_all(self, query):
        return self.database.fetch_all(query)



