import pandas as pd
import re

# =========================
# LOAD DATASET
# =========================

data = pd.read_csv("../dataset/dataset.csv")

# =========================
# SELECT IMPORTANT COLUMNS
# =========================

data = data[[
    'track_name',
    'artists',
    'track_genre',
    'danceability',
    'energy',
    'valence',
    'tempo',
    'popularity'
]]

# =========================
# REMOVE NULL VALUES
# =========================

data.dropna(inplace=True)

# =========================
# REMOVE DUPLICATES
# =========================

data.drop_duplicates(
    subset=['track_name', 'artists'],
    inplace=True
)

# =========================
# KEEP MOSTLY ENGLISH SONGS
# =========================

def is_english(text):

    text = str(text)

    # Allow English letters, numbers and common symbols
    return bool(
        re.match(
            r"^[A-Za-z0-9 .,!?&()'\"-]+$",
            text
        )
    )

# Filter English songs
data = data[
    data['track_name'].apply(is_english)
]

# =========================
# REMOVE LOW POPULARITY SONGS
# =========================

data = data[data['popularity'] > 40]

# =========================
# MOOD LABELING FUNCTION
# =========================

def assign_mood(row):

    # Happy
    if row['valence'] > 0.6 and row['energy'] > 0.6:
        return "Happy"

    # Sad
    elif row['valence'] < 0.4 and row['energy'] < 0.5:
        return "Sad"

    # Energetic
    elif row['energy'] > 0.75 and row['tempo'] > 120:
        return "Energetic"

    # Relaxed
    elif row['energy'] < 0.5 and row['danceability'] < 0.5:
        return "Relaxed"

    # Calm
    else:
        return "Calm"

# =========================
# CREATE MOOD COLUMN
# =========================

data['mood'] = data.apply(assign_mood, axis=1)

# =========================
# SAVE CLEANED DATASET
# =========================

data.to_csv(
    "../dataset/cleaned_dataset.csv",
    index=False
)

# =========================
# OUTPUT
# =========================

print("Dataset cleaned successfully")

print("Total songs after cleaning:", len(data))

print(data.head())