import os

class Config(object):
    WTF_CSRF_ENABLED = False # Currently Isn't requiring Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fake secret key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db'
