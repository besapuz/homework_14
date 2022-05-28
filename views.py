from flask import Flask, jsonify

from run import search_title

app = Flask(__name__)


@app.route('/movie/<title>')
def return_title(title):
    return jsonify(search_title(title))


if __name__ == "__main__":
    app.run(port=80)
