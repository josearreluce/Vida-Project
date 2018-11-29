import sys
sys.path.append('../../')
from app import models
from app.models import DatabaseConnection, UserSession

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
        self.password = password

class BasicInfo(object):

    def __init__(self, age, sex):
        self.age = age
        self.sex = sex

    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = age

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

    def setBloodPressure(self, blood_pressure):
        self.blood_pressure = blood_pressure

    def getDiabetes(self):
        return self.diabetes

    def setDiabetes(self, diabetes):
        self.diabetes = diabetes

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

def dbUsertoUser(userschema):

    # Account Info
    acc_info = AccountInfo(userschema.username, userschema.pswd)

    # Basic Info
    basic_info = BasicInfo(userschema.age, userschema.sex)

    # Personal Info
    personal_info = PersonalInfo(userschema.height, userschema.weight)

    # Health Background
    blood_pressure = (userschema.blood_pressure_low, userschema.blood_pressure_high)
    health_background = HealthBackground(userschema.smoker, blood_pressure, userschema.diabetes)

    return User(acc_info, basic_info, personal_info, health_background)
