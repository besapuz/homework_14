import sqlite3


def search_title(path):
    with sqlite3.connect("netflix.db") as connect:
        cursor = connect.cursor()
        sqlite_query = f"""
            SELECT title, country, release_year,  listed_in, description
            FROM netflix
            WHERE title LIKE '%{path}%'
            ORDER BY release_year DESC 
            """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        ex_query = {
            "title": executed_query[0][0],
            "country": executed_query[0][1],
            "release_year": executed_query[0][2],
            "genre": executed_query[0][3],
            "description": executed_query[0][4]
        }
    return ex_query


if __name__ == "__main__":
    print(search_title("path"))
