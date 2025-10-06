from app.database import db
from app.models.user_model import AboutCreate, AboutUpdate, LeadershipCreate
from bson import ObjectId
from app.database import hero_collection, about_collection, members_collection, leadership_collection
from typing import Optional, Dict, Any
#hero section
def create_hero(data: dict):
    # Allow only one hero document
    existing = hero_collection.find_one()
    if existing:
        return str(existing["_id"])
    result = hero_collection.insert_one(data)
    return str(result.inserted_id)
def convert_objectids(doc):
    if isinstance(doc, list):
        return [convert_objectids(d) for d in doc]
    if isinstance(doc, dict):
        return {k: convert_objectids(v) for k, v in doc.items()}
    if isinstance(doc, ObjectId):
        return str(doc)
    return doc

def update_hero(hero_id: str, data: dict):
    hero_collection.update_one({"_id": ObjectId(hero_id)}, {"$set": data})
    updated = hero_collection.find_one({"_id": ObjectId(hero_id)})  # include _id
    return convert_objectids(updated)


def get_hero():
    hero = hero_collection.find_one({})  # include _id
    if hero:
        hero["_id"] = str(hero["_id"])  # convert ObjectId to string
    return hero

#about section

def get_about() -> Optional[Dict[str, Any]]:
    doc = about_collection.find_one({})
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

def create_about(payload: AboutCreate) -> Dict[str, Any]:
    doc = payload.dict()
    result = about_collection.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc

def update_about(id: str, payload: AboutUpdate) -> Optional[Dict[str, Any]]:
    update_doc = {"$set": payload.dict(exclude_unset=True)}
    res = about_collection.find_one_and_update({"_id": ObjectId(id)}, update_doc, return_document=True)
    if not res:
        return None
    res["_id"] = str(res["_id"])
    return res

def delete_about(id: str) -> bool:
    res = about_collection.delete_one({"_id": ObjectId(id)})
    return res.deleted_count == 1

# members section
def get_members():
    doc = members_collection.find_one()
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def create_members(payload):
    data = payload.dict()
    result = members_collection.insert_one(data)
    return {**data, "_id": str(result.inserted_id)}


def update_members(id: str, payload):
    data = payload.dict()
    result = members_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count == 0:
        return None
    updated = members_collection.find_one({"_id": ObjectId(id)})
    updated["_id"] = str(updated["_id"])
    return updated

## leadership section
def serialize_member(member):
    return {
        "id": str(member["_id"]),
        "name": member["name"],
        "designation": member["designation"],
        "title": member["title"],
        "description": member["description"],
        "linkedin": member.get("linkedin"),
        "instagram": member.get("instagram"),
        "image_base64": member.get("image_base64"),
    }

def get_all_leaders():
    members = [serialize_member(m) for m in leadership_collection.find()]
    return members

def get_leader_by_id(member_id: str):
    member = leadership_collection.find_one({"_id": ObjectId(member_id)})
    return serialize_member(member) if member else None

def create_leader(payload: LeadershipCreate):
    data = payload.dict()
    result = leadership_collection.insert_one(data)
    return str(result.inserted_id)

def update_leader(member_id: str, payload: LeadershipCreate):
    result = leadership_collection.update_one(
        {"_id": ObjectId(member_id)}, {"$set": payload.dict()}
    )
    return result.matched_count > 0

def delete_leader(member_id: str):
    result = leadership_collection.delete_one({"_id": ObjectId(member_id)})
    return result.deleted_count > 0