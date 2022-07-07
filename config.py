from dotenv import load_dotenv
import os
import redis

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'postgres://eciedalfztrvcw:ba7f7e0f48a69ca3592a7853299d9c9d9316cfef946175edb9b3d1a7fc688fbe@ec2-34-233-115-14.compute-1.amazonaws.com:5432/da5dm56kmuk5c7'
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://bett:2019@localhost/bett'
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")