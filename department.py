import json

from dataclasses import dataclass


@dataclass
class Department(object):
    name: str
    description: str
    video_url: str = None
    search_system_url: str = None
    guide_url: str = None
    rules_url: str = None

    def __init__(self, json_data: dict):
        self.__dict__.update(json_data)

    def __repr__(self):
        return f"{self.name}\n\n{self.description}"


departments = [Department(obj) for obj in json.loads(open("department_data.json", encoding="utf-8").read())]
departments_dict = {i: departments[i] for i in range(len(departments))}
