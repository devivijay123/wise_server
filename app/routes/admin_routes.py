from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from app.models.user_model import  AdminLogin, AboutCreate, AboutUpdate, AboutDB, LeadershipCreate, MembersDB, MembersCreate, LeadershipDB
from app.database import admin_collection
from app.services import admin_service
from app.utils.tokens import create_access_token, verify_password
from typing import List
import base64

router = APIRouter(prefix="/admin", tags=["admin"])

# @router.post("/", response_model=dict)
# async def create_user(user: User):
#     return await user_service.create_user(user)

# @router.get("/", response_model=list)
# async def get_users():
#     return await user_service.get_users()

# @router.get("/{user_id}", response_model=dict)
# async def get_user(user_id: str):
#     user = await user_service.get_user_by_id(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.delete("/{user_id}")
# async def delete_user(user_id: str):
#     deleted = await user_service.delete_user(user_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"message": "User deleted successfully"}


@router.post("/login")
def admin_login(credentials: AdminLogin):

    admin = admin_collection.find_one({"email": credentials.email})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    print("Stored password hash:", admin["password"])
    if not verify_password(credentials.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(credentials.email)
    return {"access_token": token, "token_type": "bearer"}



@router.post("/hero")
async def create_hero(
    title: str = Form(...),
    subtitle: str = Form(...),
    description: str = Form(...),
    button1_text: str = Form(None),
    button1_link: str = Form(None),
    button2_text: str = Form(None),
    button2_link: str = Form(None),
    images: List[UploadFile] = File(...)
):
    # Convert images into base64 array
    image_base64_list = []
    for img in images[:3]:  # max 3 images
        content = await img.read()
        image_base64 = base64.b64encode(content).decode("utf-8")
        image_base64_list.append(image_base64)

    data = {
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "button1_text": button1_text,
        "button1_link": button1_link,
        "button2_text": button2_text,
        "button2_link": button2_link,
        "images": image_base64_list
    }

    hero_id = admin_service.create_hero(data)
    return {"message": "Hero created successfully", "id": hero_id}


@router.put("/hero/{hero_id}")
async def update_hero(
    hero_id: str,
    title: str = Form(...),
    subtitle: str = Form(...),
    description: str = Form(...),
    button1_text: str = Form(None),
    button1_link: str = Form(None),
    button2_text: str = Form(None),
    button2_link: str = Form(None),
    images: List[UploadFile] = File(None)
):
    data = {
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "button1_text": button1_text,
        "button1_link": button1_link,
        "button2_text": button2_text,
        "button2_link": button2_link,
    }

    if images:
        image_base64_list = []
        for img in images[:3]:
            content = await img.read()
            image_base64 = base64.b64encode(content).decode("utf-8")
            image_base64_list.append(image_base64)
        data["images"] = image_base64_list

    updated_hero = admin_service.update_hero(hero_id, data)
    return {"message": "Hero updated successfully", "hero": updated_hero}


@router.get("/hero")
async def get_hero():
    hero = admin_service.get_hero()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

#aboutus
@router.get("/about", response_model=AboutDB)
def read_about():
    doc = admin_service.get_about()
    if not doc:
        raise HTTPException(status_code=404, detail="About not found")
    return doc

@router.post("/about", response_model=AboutDB)
def create_about(payload: AboutCreate):
    # if you want a single document only: delete existing and insert or raise
    existing = admin_service.get_about()
    if existing:
        raise HTTPException(status_code=400, detail="About already exists. Use PUT to update.")
    doc = admin_service.create_about(payload)
    return doc

@router.put("/about/{id}", response_model=AboutDB)
def update_about(id: str, payload: AboutUpdate):
    updated = admin_service.update_about(id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="About not found")
    return updated

@router.delete("/about/{id}")
def delete_about(id: str):
    deleted = admin_service.delete_about(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="About not found")
    return {"deleted": True}

# members
@router.get("/members", response_model=MembersDB)
def get_members():
    data = admin_service.get_members()
    if not data:
        raise HTTPException(status_code=404, detail="Members data not found")
    return data



@router.post("/members", response_model=MembersDB)
def create_members(payload: MembersCreate):
    existing = admin_service.get_members()
    if existing:
        raise HTTPException(status_code=400, detail="Members data already exists — use PUT to update.")
    return admin_service.create_members(payload)



@router.put("/members/{id}", response_model=MembersDB)
def update_members(id: str, payload: MembersCreate):
    updated = admin_service.update_members(id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Members data not found for update")
    return updated


# leadership
@router.get("/leadership", response_model=list[LeadershipDB])
def get_all_members():
    return admin_service.get_all_members()

@router.get("/leadership/{member_id}", response_model=LeadershipDB)
def get_member(member_id: str):
    member = admin_service.get_member_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@router.post("/leadership", response_model=dict)
def create_member(payload: LeadershipCreate):
    member_id = admin_service.create_member(payload)
    return {"id": member_id}

@router.put("/leadership/{member_id}", response_model=dict)
def update_member(member_id: str, payload: LeadershipCreate):
    success = admin_service.update_member(member_id, payload)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"status": "updated"}

@router.delete("/leadership/{member_id}", response_model=dict)
def delete_member(member_id: str):
    success = admin_service.delete_member(member_id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"status": "deleted"}
