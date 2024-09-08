import os

from dotenv import load_dotenv


load_dotenv()

AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
BASE_URL = os.environ.get("BASE_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
