class AccountInfo():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getUsername(self):
        return self.username

    def setUsername(self, username):
        self.username = username

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = self.password

class BasicInfo(object):

    def __init__(self, name, dob, sex):
        self.name = name
        self.dob = dob
        self.sex = sex

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getDOB(self):
        return self.dob

    def setDOB(self, dob):
        self.dob = dob

    def getSex(self):
        return self.sex

    def setSex(self, sex):
        self.sex = sex

class PersonalInfo(object):

    def __init__(self, height, weight):
        self.height = height
        self.weight = weight

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

class HealthBackground(object):

    def __init__(self, smoker, blood_pressure, diabetes):
        self.smoker = smoker
        self.blood_pressure = blood_pressure
        self.diabetes = diabetes

    def getSmoker(self):
        return self.smoker

    def setSmoker(self, smoker):
        self.smoker = smoker

    def getBloodPressure(self):
        return self.blood_pressure

    def setBloodPressure(self, smoker):
        self.smoker = smoker

    def getDiabetes(self):
        self.diabetes = diabetes

    def setDiabetes(self, diabetes):
        return self.diabetes

class User(object):

    # comprehensive initialization.
    def __init__(self, account_info, basic_info, personal_info, health_background):
        self.account_info = account_info
        self.basic_info = basic_info
        self.personal_info = personal_info
        self.health_background = health_background

    def getAccountInfo(self):
        return self.account_info

    def getBasicInfo(self):
        return self.basic_info

    def getPersonalInfo(self):
        return self.personal_info

    def getHealthBackground(self):
        return self.health_background

    def setAccountInfo(self, account_info):
        self.account_info = account_info

    def setBasicInfo(self, basic_info):
        self.basic_info = basic_info

    def setPersonalInfo(self, personal_info):
        self.personal_info = personal_info

    def setHealthBackground(self, health_background):
        self.health_background = health_background
