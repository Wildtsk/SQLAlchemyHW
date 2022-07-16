from flask import Flask

from utils import get_all_candidates, get_candidate_by_id, get_candidate_by_skill, \
    get_candidates_by_name, format_all_candidates

app = Flask(__name__)


@app.route('/')
def page_main():
    """Главная страница"""
    candidates: list[dict] = get_all_candidates()
    result = '<pre>'
    res: str = format_all_candidates(candidates)
    result += res
    result += '</pre>'
    return result


@app.route('/candidate/<int:uid>')
def page_candidate(uid):
    """Поиск кандидата по id"""
    candidate: dict = get_candidate_by_id(uid)
    candidate_id = candidate
    result = '<pre>'f'<h1>Имя кандидата: {candidate_id["name"]}</h1>'
    result += f'<p>Позиция кандидата:{candidate_id["id"]}</p>'
    result += f'<img src="{candidate_id["picture"]}">'
    result += f'<p>Навыки кандидата: {candidate_id["skills"]}</p></pre>'
    return result


@app.route('/skills/<skill>')
def page_skills(skill):
    """Поиск кандидата по навыку"""
    candidate: list[dict] = get_candidate_by_skill(skill)
    result = '<pre>' f"<h2>найдено со скилом {skill}: {len(candidate)}</h2>"
    result += format_all_candidates(candidate)
    result += '</pre>'
    return result


@app.route('/search/<candidate_name>')
def page_candidate_name(candidate_name):
    """Поиск кандидата по имени"""
    candidates: list[dict] = get_candidates_by_name(candidate_name)
    result = '<pre>'f'<p>Найдено {len(candidates)}</p>'
    for candidate in candidates:
        result += f'<p><a href="/candidate/{candidate["id"]}">{candidate["name"]}</a></p>'
    result += '</pre>'
    return result


app.run()
