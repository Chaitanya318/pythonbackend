import os
import pickle
import numpy as np
import pandas as pd

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


# ==============================
# FIX PATH ISSUE (IMPORTANT)
# ==============================

# Get current file directory (app folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute paths
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "goemotions_1.csv")
MODEL_PATH = os.path.join(BASE_DIR, "..", "saved_model", "emotion_model.h5")
TOKENIZER_PATH = os.path.join(BASE_DIR, "..", "saved_model", "tokenizer.pkl")


# ==============================
# LOAD FILES SAFELY
# ==============================

# Load emotion labels
df = pd.read_csv(DATA_PATH)
emotion_columns = df.columns[9:]

# Load model
model = load_model(MODEL_PATH)

# Load tokenizer
with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

max_length = 100


# ==============================
# PREDICTION FUNCTION
# ==============================

def predict_emotion(text):

    seq = tokenizer.texts_to_sequences([text])

    padded = pad_sequences(seq, maxlen=max_length)

    prediction = model.predict(padded, verbose=0)[0]

    emotions = {}

    for i, emotion in enumerate(emotion_columns):
        emotions[emotion] = round(float(prediction[i]) * 100, 2)

    # Confidence
    confidence = round(float(np.max(prediction)) * 100, 2)

    # Dominant emotion
    dominant = emotion_columns[np.argmax(prediction)]

    # Sentiment logic
    positive = ['joy', 'love', 'optimism', 'gratitude', 'excitement']
    negative = ['anger', 'sadness', 'fear', 'disgust', 'remorse']

    if dominant in positive:
        sentiment = "Positive"
    elif dominant in negative:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "emotions": emotions,
        "dominant_emotion": dominant,
        "confidence": confidence,
        "sentiment": sentiment,
        "tone": dominant
    }
