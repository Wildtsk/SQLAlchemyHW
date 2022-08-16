from flask import jsonify, Flask

from utils import get_by_title_release_year, get_by_title

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.get('/movie/<title_name>/')
def search_by_title_page(title_name):
    try:
        return jsonify(get_by_title(title_name))
    except TypeError:
        return f'Фильм с назвнаием {title_name} я не нашел('


@app.get('/movie/<int:release_year_one>/to/<int:release_year_two>.')
def search_by_release_year_page(release_year_one, release_year_two):
    try:
        return jsonify(get_by_title_release_year(release_year_one, release_year_two))
    except TypeError:
        return f'Фильм с годами {release_year_one, release_year_two} я не нашел('


if __name__ == "__main__":
    app.run()