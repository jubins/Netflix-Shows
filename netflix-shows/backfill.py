from requests import request
from csv import DictReader
from datetime import datetime
import os

# BASE_URL = 'http://localhost:9001'
BASE_URL = 'https://netflix-shows-api.herokuapp.com'
DATA_URL = os.environ.get('DATA_URL', 'https://raw.githubusercontent.com/jubins/Netflix-Shows/dev/netflix-shows/netflix_titles.csv')
FILE_PATH = os.environ.get('DATA_FILE_PATH', './data/netflix_titles.csv')


def convert_to_date(str_date):
    if not str_date:
        return None
    fd = datetime.strptime(str_date.strip(), '%B %d, %Y')
    return fd.strftime('%Y-%m-%d')


def import_data_from_local(file_path):
    with open(file_path, mode='r', encoding='utf-8') as in_csv:
        reader = DictReader(in_csv)
        count_200 = 0
        total = 0
        for idx, row in enumerate(reader):
            d = {k: v for k, v in row.items()}
            fmtdate = convert_to_date(d['date_added'])
            d['date_added'] = fmtdate
            if not fmtdate:
                del d['date_added']
            url = f'{BASE_URL}/api/addShow'
            r = request(method='POST', url=url, json=d)
            total += 1
            if r.status_code == 200:
                count_200 += 1
            print(f'Status: {r.status_code}. Message: {r.text}')
    return f"{count_200} rows inserted into the database. Attempted: {total}."


import_data_from_local(FILE_PATH)
