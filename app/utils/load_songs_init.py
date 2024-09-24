import json
import os

def initialize_songs_into_db(db):
    """
    Loads songs from the 'resources/songs.json' file into MongoDB.
    Checks if the songs are already present to avoid duplication.
    """

    songs_file_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'songs.json')
    
    if not os.path.exists(songs_file_path):
        raise FileNotFoundError(f"songs.json not found at {songs_file_path}")

    with open(songs_file_path, 'r') as file:
        songs = json.load(file)

    existing_songs_count = db.songs.count_documents({})  
    if existing_songs_count > 0:
        print("Songs already initialized. Skipping insertion.")
        return  

    for song in songs:
        if not db.songs.find_one({'artist': song['artist'], 'title': song['title']}):
            db.songs.insert_one(song)
            print(f"Inserted song: {song['title']} by {song['artist']}")
        else:
            print(f"Song '{song['title']}' by {song['artist']}' already exists. Skipping.")

    print(f'{len(songs)} songs processed.')
