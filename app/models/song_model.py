from pymongo import MongoClient
from bson.objectid import ObjectId
from .song import Song

class SongModel:
    """ Acts as our ORM"""

    def __init__(self):
        self.client = MongoClient('mongodb://mongo:27017/')
        self.db = self.client['songs_db']
        self.songs_collection = self.db['songs']

    def insert_song(self, song: Song):
        self.songs_collection.insert_one(song.to_dict())

    def find_songs(self, query={}, limit=10, skip=0):
        """Pagination."""
        cursor = self.songs_collection.find(query).skip(skip).limit(limit)
        return [Song.from_dict(song_data) for song_data in cursor]

    def get_song_by_id(self, song_id):
        song_data = self.songs_collection.find_one({'_id': ObjectId(song_id)})
        if song_data:
            return Song.from_dict(song_data)
        return None

    def update_song(self, song_id, song_data):
        self.songs_collection.update_one(
            {'_id': ObjectId(song_id)},
            {'$set': song_data}
        )

    def delete_song(self, song_id):
        self.songs_collection.delete_one({'_id': ObjectId(song_id)})
