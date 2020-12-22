from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
from databases import Database
import os

# DB_USER = os.environ.get('LOCAL_DB_USER')
# DB_PASSWORD = os.environ.get('LOCAL_DB_PASWORD')
# DB_HOST = os.environ.get('LOCAL_DB_HOST')
# DB_PORT = os.environ.get('LOCAL_DB_PORT')
# DB_NAME = os.environ.get('LOCAL_DB_NAME')
# DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

DATABASE_URL = os.environ.get('HEROKU_DB_URL')


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



