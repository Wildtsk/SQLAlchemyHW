import sqlite3


def get_value_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()

        return result


def get_by_title(title_name):
    sql = f"""
          SELECT title, country, release_year, listed_in, description
          FROM netflix
          WHERE title LIKE '{title_name}'
          ORDER BY release_year DESC
    """
    result = get_value_from_db(sql)
    for item in result:
        return dict(item)


def get_by_title_release_year(release_year_one, release_year_two):
    sql = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {release_year_one} AND {release_year_two}
    """
    result = get_value_from_db(sql)
    dict_result = []
    for item in result:
        dict_result.append(dict(item))
    return dict_result


def get_by_rating(rating):
    my_rating = {
        "children": ("G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    sql = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating in {my_rating.get(rating, ("G"))}
    """
    result = get_value_from_db(sql)
    dict_result = []
    for item in result:
        dict_result.append(dict(item))
    return dict_result


def get_by_genre(genre):

    sql = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '{genre}'
    """
    result = get_value_from_db(sql)
    dict_result = []
    for item in result:
        dict_result.append(dict(item))
    return dict_result


print(get_by_genre("Movies"))
