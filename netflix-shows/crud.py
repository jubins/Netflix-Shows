from sqlalchemy import Table, text
from . database import ShowsDB
from datetime import datetime


class CRUDShowsDB(object):
    def __init__(self, db, table_name='shows'):
        self.db = db
        self.table = Table(table_name, ShowsDB().metadata)

    def create_show(self, show):
        query = self.table.insert().values(show_id=show.show_id, type=show.type, title=show.title,
                                           director=show.director, cast=show.cast, country=show.country,
                                           date_added=show.date_added,
                                           release_year=show.release_year, rating=show.rating, duration=show.duration,
                                           listed_in=show.listed_in, description=show.description)
        results = self.db.execute(query, get='one')
        return results

    def modify_show(self, show_id, type):
        show_exists = self.search_show_by_id(show_id)
        if show_exists:
            query = self.table.update().where(self.table.columns.show_id == show_id).values(type=type)
            results = self.db.execute(query, get='one')
            return results

    def delete_show(self, show_id):
        show_exists = self.search_show_by_id(show_id)
        if show_exists:
            query = self.table.delete().where(self.table.columns.show_id == show_id)
            results = self.db.execute(query, get='one')
            return results

    def search_show_by_id(self, show_id):
        query = self.table.select().where(self.table.columns.show_id == show_id)
        results = self.db.execute(query, get='all')
        return results

    def search_show_by_title(self, show_text, limit=10, offset=0):
        query = self.table.select().where(self.table.columns.title.like(f'%{show_text}%')).limit(limit).offset(offset)
        results = self.db.execute(query, get='all')
        return results

    def search_show_by_description(self, show_text, limit=10, offset=0):
        query = self.table.select().where(self.table.columns.description.like(f'%{show_text}%')).limit(limit).offset(offset)
        results = self.db.execute(query, get='all')
        return results

    @staticmethod
    def valid_date_format(str_date):
        try:
            fmt_date = datetime.strptime(str_date.strip(), '%Y-%m-%d')
            return fmt_date
        except Exception as e:
            return False

    def filter_show_by_date_added(self, start_date=None, end_date=None, limit=10, offset=0):
        if not start_date and not end_date:
            return list()
        elif start_date and not end_date:
            start_date = self.valid_date_format(start_date)
            query = self.table.select().where(self.table.columns.date_added >= start_date,
                                              ).limit(limit).offset(offset)
        elif not start_date and end_date:
            end_date = self.valid_date_format(end_date)
            query = self.table.select().where(self.table.columns.date_added <= end_date).limit(limit).offset(offset)
        else:
            start_date = self.valid_date_format(start_date)
            end_date = self.valid_date_format(end_date)
            query = self.table.select().where(self.table.columns.date_added >= start_date)\
                .where(self.table.columns.date_added <= end_date).limit(limit).offset(offset)
        results = self.db.execute(query, get='all')
        return results

    def filter_show_by_release_year(self, year, limit=10, offset=0):
        query = self.table.select().where(self.table.columns.release_year == year).limit(limit).offset(offset)
        results = self.db.execute(query, get='all')
        return results

    def filter_show_by_country(self, country, limit=10, offset=0):
        query = self.table.select().where(self.table.columns.country.like(f'%{country}%')).limit(limit).offset(offset)
        results = self.db.execute(query, get='all')
        return results
