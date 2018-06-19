

class Course:
    def __init__(self, name, credit):
        self.name = name
        self.credit = credit
        self.score = 0

    def set_score(self, score):
        self.score = score