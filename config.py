from dotenv import load_dotenv
import os
import redis
from sqlalchemy import create_engine

load_dotenv()
uri=os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")

engine = create_engine(uri, echo=True)
redis_url=os.getenv("REDIS_URL")

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = uri or 'postgresql+psycopg2://bett:2019@localhost/bett'
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(redis_url)