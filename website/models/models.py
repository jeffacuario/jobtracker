class Application:
    def __init__(self, company, position, type, date, status):
        self.company = company
        self.position = position
        self.type = type
        self.date = date
        self.status = status


class Skill:
    def __init__(self, skill, position, company):
        self.skill = skill
        self.position = position
        self.company = company
