from utils import *
from flask import Flask

if __name__ == '__main__':
    File_candidates = 'candidates.json'
    data_candidates = load_candidates(File_candidates)

candidates = get_all(data_candidates)
candidat = '\n'.join(candidates)

main = Flask(__name__)


@main.route("/")
def page_index():
    return f"Главная страница"


@main.route('/pre/')
def page_profile():
    return f"{candidat}"


@main.route('/cand/<int:pk>')
def profile(pk):
    if pk > len(data_candidates):
        return 'Кандидат не найден'
    candidat_index = get_by_pk(pk, data_candidates)
    name = f"Имя кандидата: {candidat_index['name']}\n"
    position = f"Позиция кандидата: {candidat_index['position']}\n"
    skills = f"Навыки через запятую: {candidat_index['skills']}"
    img_src = f"Ссылка на фото: {candidat_index['picture']}\n"
    return f'{img_src}{name}{position}{skills}'


@main.route('/skills/<skill>')
def skills_candidat(skill):
    candidates_skills = get_by_skill(skill.lower(), data_candidates)
    candidates_skills = '\n'.join(candidates_skills)
    return f'{candidates_skills}'


main.run(host='0.0.0.0', port=8000)
