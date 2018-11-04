class Symptom(object):
    def __init__(self, name, id, sex, conditions, related_symptoms, desc):
        self.name = name
        self.id = id
        self.sex = sex # 1 for male, 2 for female, 0 for doesn't matter
        self.conditions = conditions
        self.related_symptoms = related_symptoms
        self.desc = desc

    def getRelatedSymptoms(self):
        return self.related_symptoms

    def getConditions(self):
        return self.conditions

    def getDesc(self):
        return self.desc
