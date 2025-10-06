
import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()
mongo_url = os.getenv("MONGODB_URI")

if not mongo_url:
    raise RuntimeError("MONGODB_URI not set in .env")

mongo_client = MongoClient(mongo_url)
db = mongo_client["wise"]
admin_collection = db["admins"]
hero_collection =db["hero"]
about_collection = db["about"]
members_collection = db["members"]
leadership_collection = db["leadership"]

