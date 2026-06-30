import os 
from datetime import datetime
#pyrefly:ignore
from dotenv import load_dotenv
#pyrefly: ignore
from pymongo import MongoClient

load_dotenv()

USER_ID = "default"  # single user so no auth needed

def get_collection():
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client[os.getenv("MONGO_DB",'contextcore')]
    return db["user_profiles"]

def get_profile()->dict:
    """Fetch the user's profile document. Returns empty dict if none exits yet."""
    col = get_collection()
    doc = col.find_one({"user_id":USER_ID})
    if doc:
        doc.pop("_id",None)
    return doc or {}


def update_profile(new_preferences:dict):
    """
    Merge new preferences into the existing profile.
    Creates the document if it doesnot exist yet (upsert).
    """

    col = get_collection()
    # $set with dot notation merges into nested fields without overwriting others
    updates = {f"preferences.{k}": v for k, v in new_preferences.items()}
    updates["updated_at"] = datetime.utcnow().isoformat()
    col.update_one(
        {"user_id": USER_ID},
        {"$set":updates},
        upsert=True  # create if doesnot exist update if it does
        )