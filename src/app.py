import tkinter as tk
from tkinter import ttk
import pandas as pd
import pickle
import webbrowser
import os
import subprocess
from urllib.parse import quote

# =========================
# LOAD DATASET
# =========================

data = pd.read_csv("../dataset/cleaned_dataset.csv")

# =========================
# LOAD MODEL
# =========================

model = pickle.load(open("../models/music_model.pkl", "rb"))

# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Mood-Based Music Recommendation System")
root.geometry("1000x700")
root.configure(bg="#1e1e1e")

# =========================
# TITLE
# =========================

heading = tk.Label(
    root,
    text="Mood-Based Music Recommendation System",
    font=("Arial", 22, "bold"),
    bg="#1e1e1e",
    fg="white"
)

heading.pack(pady=20)

# =========================
# RESULT LABEL
# =========================

result_label = tk.Label(
    root,
    text="Select Your Mood",
    font=("Arial", 16),
    bg="#1e1e1e",
    fg="#00ffcc"
)

result_label.pack(pady=10)

# =========================
# TABLE
# =========================

columns = ("Song", "Artist", "Genre")

song_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

song_table.heading("Song", text="Song")
song_table.heading("Artist", text="Artist")
song_table.heading("Genre", text="Genre")

song_table.column("Song", width=350)
song_table.column("Artist", width=250)
song_table.column("Genre", width=150)

song_table.pack(pady=20)

# =========================
# RECOMMEND FUNCTION
# =========================

def recommend_songs(mood):

    # Clear old songs
    for row in song_table.get_children():
        song_table.delete(row)

    # Filter songs
    songs = data[data['mood'] == mood]

    # Random recommendations
    songs = songs.sample(min(10, len(songs)))

    # Update result label
    result_label.config(text=f"Recommended {mood} Songs")

    # Insert into table
    for index, row in songs.iterrows():

        song_table.insert(
            "",
            tk.END,
            values=(
                row['track_name'],
                row['artists'],
                row['track_genre']
            )
        )

# =========================
# PLAY SONG FUNCTION
# =========================

def play_song():

    selected = song_table.selection()

    if not selected:
        result_label.config(text="Please select a song first")
        return

    item = song_table.item(selected[0])

    song_name = item['values'][0]
    artist_name = item['values'][1]

    # Create YouTube search query
    query = quote(f"{song_name} {artist_name}")

    # Open YouTube search
    url = f"https://www.youtube.com/results?search_query={query}"

    webbrowser.open(url)

# =========================
# SAVE SONG FUNCTION
# =========================

def save_song():

    selected = song_table.selection()

    if not selected:
        result_label.config(text="Please select a song first")
        return

    item = song_table.item(selected[0])

    song_name = item['values'][0]
    artist_name = item['values'][1]
    genre = item['values'][2]

    with open("saved_songs.txt", "a", encoding="utf-8") as file:

        file.write(f"Song: {song_name}\n")
        file.write(f"Artist: {artist_name}\n")
        file.write(f"Genre: {genre}\n")
        file.write("-------------------------\n")

    result_label.config(text="Song saved successfully")

# =========================
# OPEN SAVED SONGS FUNCTION
# =========================

def open_saved_songs():

    file_path = "saved_songs.txt"

    if not os.path.exists(file_path):
        result_label.config(text="No saved songs found")
        return

    try:

        # Windows
        os.startfile(file_path)

    except:

        try:
            subprocess.call(["open", file_path])

        except:
            subprocess.call(["xdg-open", file_path])

# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

# =========================
# MOOD BUTTONS
# =========================

happy_btn = tk.Button(
    button_frame,
    text="Happy",
    font=("Arial", 12, "bold"),
    bg="#FFD93D",
    width=12,
    command=lambda: recommend_songs("Happy")
)

happy_btn.grid(row=0, column=0, padx=10)

sad_btn = tk.Button(
    button_frame,
    text="Sad",
    font=("Arial", 12, "bold"),
    bg="#6C8CD5",
    fg="white",
    width=12,
    command=lambda: recommend_songs("Sad")
)

sad_btn.grid(row=0, column=1, padx=10)

energetic_btn = tk.Button(
    button_frame,
    text="Energetic",
    font=("Arial", 12, "bold"),
    bg="#FF6B6B",
    fg="white",
    width=12,
    command=lambda: recommend_songs("Energetic")
)

energetic_btn.grid(row=0, column=2, padx=10)

relaxed_btn = tk.Button(
    button_frame,
    text="Relaxed",
    font=("Arial", 12, "bold"),
    bg="#4ECDC4",
    width=12,
    command=lambda: recommend_songs("Relaxed")
)

relaxed_btn.grid(row=0, column=3, padx=10)

calm_btn = tk.Button(
    button_frame,
    text="Calm",
    font=("Arial", 12, "bold"),
    bg="#95A5A6",
    width=12,
    command=lambda: recommend_songs("Calm")
)

calm_btn.grid(row=0, column=4, padx=10)

# =========================
# PLAY BUTTON
# =========================

play_btn = tk.Button(
    root,
    text="Play Selected Song",
    font=("Arial", 12, "bold"),
    bg="#2ECC71",
    fg="white",
    width=22,
    command=play_song
)

play_btn.pack(pady=5)

# =========================
# SAVE BUTTON
# =========================

save_btn = tk.Button(
    root,
    text="Save Song",
    font=("Arial", 12, "bold"),
    bg="#3498DB",
    fg="white",
    width=22,
    command=save_song
)

save_btn.pack(pady=5)

# =========================
# OPEN SAVED SONGS BUTTON
# =========================

open_saved_btn = tk.Button(
    root,
    text="Open Saved Songs",
    font=("Arial", 12, "bold"),
    bg="#9B59B6",
    fg="white",
    width=22,
    command=open_saved_songs
)

open_saved_btn.pack(pady=5)

# =========================
# EXIT BUTTON
# =========================

exit_btn = tk.Button(
    root,
    text="Exit",
    font=("Arial", 12, "bold"),
    bg="red",
    fg="white",
    width=15,
    command=root.destroy
)

exit_btn.pack(pady=20)

# =========================
# RUN APP
# =========================

root.mainloop()