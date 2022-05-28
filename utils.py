import sqlite3
from pprint import pprint as pp


class SqlSearch:

    def __init__(self, path):
        self.path = path

    def get_sql(self):
        with sqlite3.connect(self.path) as connect:
            cursor = connect.cursor()
        return cursor

    def search_title(self, title):
        cursor = self.get_sql()
        sqlite_query = f"""
                SELECT title, country, release_year,  listed_in, description
                FROM netflix
                WHERE title LIKE '%{title}%'
                ORDER BY release_year DESC 
                """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        return {
            "title": executed_query[0][0],
            "country": executed_query[0][1],
            "release_year": executed_query[0][2],
            "genre": executed_query[0][3],
            "description": executed_query[0][4]
        }

    def search_range_years(self, one_year, two_year):
        cursor = self.get_sql()
        sqlite_query = f"""
                        SELECT title, release_year
                        FROM netflix
                        WHERE release_year BETWEEN {one_year} AND {two_year}
                        LIMIT 100
                        """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        list_release = []
        for i in executed_query:
            list_release.append({"title": i[0], "release_year": i[1]})
        return list_release

    def get_genre(self, genre):
        cursor = self.get_sql()
        sqlite_query = f"""
                        SELECT title, description
                        FROM netflix
                        WHERE listed_in LIKE '%{genre}%'
                        ORDER BY release_year DESC
                        LIMIT 10
                        """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        json_listed_in = []
        for i in executed_query:
            json_listed_in.append({"title": i[0], "description": i[1]})
        return json_listed_in


"""ade = SqlSearch("netflix.db")

if __name__ == "__main__":
    pp(ade.get_genre("Shows"))"""
