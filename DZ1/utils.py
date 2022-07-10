import json


def load_candidates(candidates):
    """загрузит данные из файла"""
    with open(candidates, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_all(data_candidates):
    """покажет всех кандидатов"""
    profils = []
    for items in data_candidates:
        nps = {}
        nps["name"] = items["name"]
        nps["position"] = items["position"]
        nps["skills"] = items["skills"]
        profils.append(items["name"])
        profils.append(items["position"])
        profils.append(items["skills"])
        profils.append(' ')
    return profils


def get_by_pk(pk, data_candidates):
    """вернет кандидата по pk"""
    for items in data_candidates:
        if items['pk'] == pk:
            return items


def get_by_skill(skill, data_candidates):
    """вернет кандидатов по навыку"""
    candidat_skill = {}
    profils = []
    for items in data_candidates:
        if skill in items["skills"].lower():
            candidat_skill["name"] = items["name"]
            candidat_skill["position"] = items["position"]
            candidat_skill["skills"] = items["skills"]
            profils.append(items["name"])
            profils.append(items["position"])
            profils.append(items["skills"])
            profils.append(' ')
    return profils
