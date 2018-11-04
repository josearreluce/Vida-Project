class User(object):

    # comprehensive initialization.
    def __init__(self, username, password, name, id, sex, date_of_birth, age, height, weight, preexisting_conditions):
        self.username = username
        self.password = password
        self.name = name
        self.id = id
        self.sex = sex
        self.date_of_birth = date_of_birth
        self.age = age
        self.height = height
        self.weight = weight
        self.preexisting_conditions = preexisting_conditions

    # Bare minimum initialization
    def __init__(self, username, password, sex, age):
        self.username = username
        self.password = password
        self.sex = sex
        self.age = age
        self.name = ""
        self.id = -1
        self.date_of_birth = -1
        self.height = -1
        self.weight = -1
        self.preexisting_conditions = []

    def startAssessment(self):
        # TODO
        return 0

    def logout(self):
        # TODO
        return 0

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def getDateOfBirth(self):
        return self.date_of_birth

    def getHeight(self):
        return self.height

    def getWeight(self):
        return self.weight

    def getPreExistingConditions(self):
        return self.preexisting_conditions

    def setName(self, name):
        self.name = name

    def setId(self, id):
        self.id = id

    def setDateOfBirth(self, date_of_birth):
        self.date_of_birth = date_of_birth

    def setHeight(self, height):
        self.height = height

    def setWeight(self, weight):
        self.weight = weight

    def addPreExistingCondition(self, condition):
        self.preexisting_conditions.append(condition)
