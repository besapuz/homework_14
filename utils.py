import sqlite3
from collections import Counter
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
        if executed_query:
            return {
                "title": executed_query[0][0],
                "country": executed_query[0][1],
                "release_year": executed_query[0][2],
                "genre": executed_query[0][3],
                "description": executed_query[0][4]
            }
        else:
            return "Список пустой"

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
            list_release.append({"title": i[0],
                                 "release_year": i[1]})
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
            json_listed_in.append({"title": i[0],
                                   "description": i[1]})
        return json_listed_in

    def get_rating_movie(self, rating):
        cursor = self.get_sql()
        rating_list = {
            "children": "'G'",
            "family": "'G', 'PG', 'PG-13'",
            "adult": "'R', 'NC-17'"
        }
        if rating not in rating_list:
            return "Нет такого рейтинга"
        query = f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ({rating_list[rating]})
                    """
        cursor.execute(query)
        executed_query = cursor.fetchall()
        json_rating = []
        for i in executed_query:
            json_rating.append({
                "title": i[0],
                "rating": i[1],
                "description": i[2]
            })
        return json_rating

    def cast_partner(self, actor_1, actor_2):
        cursor = self.get_sql()
        query = f"""
                SELECT "cast"
                FROM netflix
                WHERE "cast" LIKE '%{actor_1}%'
                AND "cast" LIKE '%{actor_2}%'"""
        cursor.execute(query)
        executed_query = cursor.fetchall()
        actor_list = []
        for cast in executed_query:
            actor_list.extend(cast[0].split(', '))
        counter = Counter(actor_list)
        result_list = []
        for actor, count in counter.items():
            if actor not in [actor_1, actor_2] and count > 2:
                result_list.append(actor)
        return result_list

    def get_list_movie(self, type_, year, genre):
        cursor = self.get_sql()
        query = f"""select title, description 
        from netflix 
        where type = '{type_}' COLLATE NOCASE
        and listed_in = '{year}' COLLATE NOCASE
        and release_year = '{genre}' COLLATE NOCASE
        """
        cursor.execute(query)
        executed_query = cursor.fetchall()
        list_movie = []
        for i in executed_query:
            list_movie.append({
                "title": i[0],
                "description": i[1]
            })
        return list_movie


ade = SqlSearch("netflix.db")

if __name__ == "__main__":
    pp(ade.get_list_movie('movie', 'dramas', '2002'))
