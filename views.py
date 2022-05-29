from flask import Flask, jsonify

from utils import SqlSearch

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

get_netflix = SqlSearch("netflix.db")


@app.route('/movie/<title>')
def return_title(title):
    return jsonify(get_netflix.search_title(title))


@app.route('/movie/<int:one_year>/to/<int:two_year>')
def return_release_year(one_year, two_year):
    return jsonify(get_netflix.search_range_years(one_year, two_year))


@app.route('/genre/<genre>')
def return_genre(genre):
    return jsonify(get_netflix.get_genre(genre))


@app.route('/rating/<rating>')
def return_rating(rating):
    return jsonify(get_netflix.get_rating_movie(rating))


if __name__ == "__main__":
    app.run(port=80)
