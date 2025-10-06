from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes import admin_routes



app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],   # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI + MongoDB project"}

app.include_router(admin_routes.router)
# @app.post("/admin/login")
# def admin_login(credentials: AdminLogin):
#     admin = admin_collection.find_one({"email": credentials.email})
#     if not admin:
#         raise HTTPException(status_code=404, detail="Admin not found")

#     if not verify_password(credentials.password, admin["password"]):
#         raise HTTPException(status_code=401, detail="Incorrect password")

#     token = create_access_token(credentials.email)
#     return {"access_token": token, "token_type": "bearer"}
