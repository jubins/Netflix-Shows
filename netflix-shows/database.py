from sqlalchemy import create_engine
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

db_user = config['database'].get('user')
db_password = config['database'].get('password')
db_port = config['database'].getint('port')

database_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:{db_port}/'
engine = create_engine(database_url)
