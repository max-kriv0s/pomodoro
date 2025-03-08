import os

from dotenv import load_dotenv

bind = "0.0.0.0:8000"
workers = 4

enviroment = os.getenv("ENVIROMENT")

env = os.path.join(os.getcwd(), f".{enviroment}.env")
if os.path.exists(env):
    load_dotenv(env)
