from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["emotionDB"]

users_collection = db["users"]

# FIX: use emotion_history collection
emotion_collection = db["emotion_history"]

blacklist_collection = db["blacklist_tokens"]


