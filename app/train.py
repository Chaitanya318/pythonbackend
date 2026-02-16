import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from model import create_dcnn_model

# Load dataset
df = pd.read_csv("../data/goemotions_1.csv")

# Text column
texts = df['text']

# Emotion columns
emotion_columns = df.columns[9:]

labels = df[emotion_columns].values

# Tokenizer
tokenizer = Tokenizer(num_words=20000)
tokenizer.fit_on_texts(texts)

sequences = tokenizer.texts_to_sequences(texts)

max_length = 100

X = pad_sequences(sequences, maxlen=max_length)
y = labels

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2
)

# Create model
model = create_dcnn_model(
    vocab_size=20000,
    max_length=max_length,
    num_classes=len(emotion_columns)
)

# Train
model.fit(
    X_train,
    y_train,
    epochs=5,
    batch_size=32,
    validation_data=(X_test, y_test)
)

# Save model
model.save("../saved_model/emotion_model.h5")

# Save tokenizer
with open("../saved_model/tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("Training Complete")
