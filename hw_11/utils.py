from __future__ import annotations

import json


def load_json() -> list[dict]:
    """Фарматирование из json в список"""
    with open('candidates.json', 'r', encoding='utf-8') as file:
        candidates = json.load(file)
        return candidates


def format_candidates(candidates: list[dict]) -> str:
    """Фарматирование списка кандидатов"""
    result = '<pre>'

    for candidate in candidates:
        result += f"""
            {candidate["name"]}\n
            {candidate["position"]}\n
            {candidate["skills"]}\n
        """
    result += '</pre>'
    return result


def get_all_candidates() -> list[dict]:
    """все кандидаты"""
    return load_json()


def get_candidate_by_id(uid: int) -> dict | None:
    """поиск кандидата по id"""
    candidates = get_all_candidates()
    for candidate in candidates:
        if candidate['id'] == uid:
            return candidate
    return None


def get_candidate_by_skill(skill: str) -> list[dict]:
    """Поиск кандидатов по скилам"""
    candidates = get_all_candidates()
    result = []
    for candidate in candidates:
        if skill in candidate['skills'].lower().split(', '):
            result.append(candidate)
    return result


def get_candidates_by_name(candidate_name: str) -> list[dict]:
    """Поиск кандидатов по именам"""
    candidates = get_all_candidates()
    result = []
    for candidate in candidates:
        if candidate_name in candidate["name"]:
            result.append(candidate)
    return result


def format_all_candidates(candidates: list[dict]) -> str:
    """Фарматирование списка кандидатов"""
    result = f"<h1>Все кандидаты</h1>"
    for candidate in candidates:
        result += f"""
            <p><a href="/candidate/{candidate["id"]}">{candidate["name"]}</a></p>
        """
    return result