import sqlite3


def get_value_from_db(sql): #Читает таблицу и выносит определенные результаты
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()

        return result


def get_by_title(title_name):#Поиск фильмов по названию, выводит один результат
    sql = f"""
          SELECT title, country, release_year, listed_in, description
          FROM netflix
          WHERE title LIKE '{title_name}'
          ORDER BY release_year DESC
    """
    result = get_value_from_db(sql)
    for item in result:
        return dict(item)


def get_by_title_release_year(release_year_one, release_year_two):#Поиск фильмов по релизу. Временной диапазон
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


def get_by_rating(rating): #Поиск фильмов по рейтингу, по умолчанию "G"
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


def get_by_genre(genre): #Поиск фильмов по жанрам

    sql = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{str(genre).title()}%'
    """
    result = get_value_from_db(sql)
    dict_result = []
    for item in result:
        dict_result.append(dict(item))
    return dict_result


def get_by_name(name1="Jack Black", name2="Dustin Hoffman"):#Поиск актеров которые снимались с 2 определенными, больше 2 раз

    sql = f"""
            SELECT "cast"
            FROM netflix
            WHERE "cast" LIKE '%{name1}%' AND "cast" LIKE '%{name2}%'
    """
    result = get_value_from_db(sql)
    names_list = []
    dict_result = {}
    for item in result:
        names = set(dict(item).get("cast").split(", ")) - set([name1, name2])

        for name in names:
            dict_result[name.strip()] = dict_result.get(name.strip(), 0) + 1

    for key, value in dict_result.items():
        if value > 2:
            names_list.append(key)

    return names_list


def get_by_type(type_movie, release, genre):#Поиск фильмов по 3 параментрам: жанр, тип, релиз

    sql = f"""
            SELECT title, description
            FROM netflix
            WHERE type like '{type_movie}'
            AND release_year = '{release}'
            AND listed_in LIKE '%{str(genre).title()}%'
    """
    result = get_value_from_db(sql)
    dict_result = []
    for item in result:
        dict_result.append(dict(item))
    return dict_result


