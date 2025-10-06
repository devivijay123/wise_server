from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId

class AdminLogin(BaseModel):
    email: str
    password: str


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class CoreValue(BaseModel):
    icon: Optional[str] = None  # e.g., "FaHandshake"
    title: Optional[str] = None
    description: Optional[str] = None


class AboutBase(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: Optional[str] = None
    subtitle: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    coreValues: Optional[List[CoreValue]] = None
    image: Optional[str] = None  

class AboutCreate(AboutBase):
    pass


# --- Update model ---
class AboutUpdate(AboutBase):
    pass


# --- DB model ---
class AboutDB(AboutBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ---members ---
class MembersBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    image1: Optional[str] 
    image2: Optional[str] 
    community_title: Optional[str]
    community_subtitle: Optional[str]
    community_description: Optional[str]
    community_image: Optional[str] = None


class MembersCreate(MembersBase):
    pass

class MembersDB(MembersBase):
    id: Optional[str] = Field(alias="_id")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

# leadership


class LeadershipCreate(BaseModel):
    name: str
    designation: str
    title: str
    description: str
    linkedin: Optional[str]
    instagram: Optional[str]
    image_base64: Optional[str]

class LeadershipDB(LeadershipCreate):
    id: str
    model_config = {
        "from_attributes": True
    }