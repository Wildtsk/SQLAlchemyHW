import json

from flask import jsonify, Flask

from utils import get_by_title_release_year, get_by_title, get_by_rating

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.get('/movie/<title_name>/')
def search_by_title_page(title_name):
    try:
        result = get_by_title(title_name)
        return app.response_class(
            response=json.dumps(result,
                                ensure_ascii=False,
                                indent=4),
            status=200,
            mimetype="application/json"
        )
    except TypeError:
        return f'Фильм с назвнаием {title_name} я не нашел('


@app.get('/movie/<int:release_year_one>/to/<int:release_year_two>')
def search_by_release_year_page(release_year_one, release_year_two):
    try:
        result = get_by_title_release_year(release_year_one, release_year_two)
        return app.response_class(
            response=json.dumps(result,
                                ensure_ascii=False,
                                indent=4),
            status=200,
            mimetype="application/json"
        )
    except TypeError:
        return f'Фильм с годами {release_year_one, release_year_two} я не нашел('


@app.get('/rating/<rating>')
def search_by_rating_page(rating):
    result = get_by_rating(rating)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False,
                            indent=4),
        status=200,
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)