from fastapi import APIRouter, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from bson import ObjectId
from app.database import blacklist_collection

from app.schemas import UserSignup, UserLogin, EmotionInput
from app.database import users_collection, emotion_collection
from app.auth import hash_password, verify_password, create_token
from app.predict import predict_emotion
from jose import jwt, JWTError

router = APIRouter()

security = HTTPBearer()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


# ==========================
# SIGNUP
# ==========================
@router.post("/signup")
def signup(user: UserSignup):

    existing = users_collection.find_one({"email": user.email})

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = hash_password(user.password)

    users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed
    })

    return {"message": "User created successfully"}


# ==========================
# LOGIN
# ==========================
@router.post("/login")
def login(user: UserLogin):

    db_user = users_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_token({
        "user_id": str(db_user["_id"]),
        "email": db_user["email"]
    })

    return {
        "message": "Login successful",
        "token": token
    }


# ==========================
# HELPER FUNCTION
# ==========================
def get_current_user(Authorization: str = Header(None)):

    if Authorization is None:
        raise HTTPException(status_code=401, detail="Token missing")

    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = Authorization.replace("Bearer ", "")

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/predict")
def predict(input: EmotionInput,
            credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    if blacklist_collection.find_one({"token": token}):
        raise HTTPException(status_code=401, detail="Token expired. Please login again.")

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user_id = decoded["user_id"]
    email = decoded["email"]

    result = predict_emotion(input.text)

    emotion_collection.insert_one({
        "user_id": user_id,
        "email": email,
        "text": input.text,
        "result": result
    })

    return result



# ==========================
# GET USER HISTORY
# ==========================
@router.get("/history")
def get_history(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user_id = decoded["user_id"]

    data = []

    cursor = emotion_collection.find({"user_id": user_id})

    for doc in cursor:

        data.append({
            "id": str(doc["_id"]),
            "text": doc["text"],
            "result": doc["result"]
        })

    return data


@router.delete("/history/{item_id}")
def delete_single_history(
    item_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user_id = decoded["user_id"]

    emotion_collection.delete_one({
        "_id": ObjectId(item_id),
        "user_id": user_id
    })

    return {"message": "Deleted"}

@router.delete("/history")
def delete_all_history(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user_id = decoded["user_id"]

    emotion_collection.delete_many({
        "user_id": user_id
    })

    return {"message": "All deleted"}







# ==========================
# LOGOUT
# ==========================
@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    # add token to blacklist
    blacklist_collection.insert_one({
        "token": token
    })

    return {
        "message": "Logout successful"
    }
