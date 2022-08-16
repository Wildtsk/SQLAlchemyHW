import sqlite3


def get_by_title(title_name):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""
                SELECT title, country, release_year, listed_in, description
                FROM netflix
                WHERE title LIKE '%{title_name}%'
                ORDER BY release_year DESC
        """
        cursor.execute(query)
        result = cursor.fetchone()
        film = {
            'title' : result[0],
            'country' : result[1],
            'release_year': result[2],
            'listed_in': result[3],
            'description': result[4],
        }
    return film


def get_by_title_release_year(release_year_one, release_year_two):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""
                SELECT title, release_year
                FROM netflix
                WHERE release_year BETWEEN '{release_year_one}' AND '{release_year_two}'
        """
        cursor.execute(query)
        result = cursor.fetchall()
        film = {
            'title' : result[0],
            'release_year' : result[1],
        }
    return film
