from dotenv import load_dotenv
import os
import redis

load_dotenv()

uri = os.getenv('SQLALCHEMY_DATABASE_URI')
if uri:
    if uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
else:
    uri = 'postgresql://bett:2019@localhost:10000/bett'

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://plrvnfnhmkfxmq:ebca9231c476d7d75eadf248e024f74f65e319f416d6357e6cde977c7b2ea790@ec2-44-205-41-76.compute-1.amazonaws.com:5432/d238lfqrimedtp'

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")