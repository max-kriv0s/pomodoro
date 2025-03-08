import os

from dotenv import load_dotenv

bind = "0.0.0.0:8000"
workers = 4

enviroment = os.getenv("ENVIROMENT")
if enviroment is None:
    env = "local"

env = os.path.join(os.getcwd(), f".{enviroment}.env")
print(f"Current env - {env}")

if os.path.exists(env):
    load_dotenv(env)
