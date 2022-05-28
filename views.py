from flask import Flask, jsonify

from utils import SqlSearch

app = Flask(__name__)

get_netflix = SqlSearch("netflix.db")


@app.route('/movie/<title>')
def return_title(title):
    try:
        return jsonify(get_netflix.search_title(title))
    except:
        return "Совпадений не найдено"


@app.route('/movie/<int:one_year>/to/<int:two_year>')
def return_release_year(one_year, two_year):
    try:
        return jsonify(get_netflix.search_range_years(one_year, two_year))
    except:
        "Фильмы не найдены"


if __name__ == "__main__":
    app.run(port=80)
