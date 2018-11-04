class Condition(object):
    def __init__(self, desc, symptoms, name, id, sex):
        self.desc = desc
        self.symptoms = symptoms
        self.name = name
        self.id = id
        self.sex = sex

    def getSymptoms(self):
        return self.symptoms
