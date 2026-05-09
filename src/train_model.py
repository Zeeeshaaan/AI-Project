import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load cleaned dataset
data = pd.read_csv("../dataset/cleaned_dataset.csv")

# Features
X = data[[
    'danceability',
    'energy',
    'valence',
    'tempo',
    'popularity'
]]

# Target
y = data['mood']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = DecisionTreeClassifier()

# Train model
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

# Save model
pickle.dump(model, open("../models/music_model.pkl", "wb"))

print("Model saved successfully")