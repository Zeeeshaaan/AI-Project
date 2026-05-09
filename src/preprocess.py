import pandas as pd

# Load dataset
data = pd.read_csv("../dataset/dataset.csv")

# Select useful columns
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

# Remove missing values
data.dropna(inplace=True)

# Mood labeling function
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

    else:
        return "Calm"

# Create mood column
data['mood'] = data.apply(assign_mood, axis=1)

# Save cleaned dataset
data.to_csv("../dataset/cleaned_dataset.csv", index=False)

print("Dataset cleaned successfully")

print(data.head())