from pymongo import MongoClient
from bson.objectid import ObjectId
from ..models.song_model import SongModel
from ..models.song import Song

class SongService:
    def __init__(self):
        # Connect DB service running in Docker
        self.client = MongoClient('mongodb://mongo:27017/')
        self.db = self.client['songs_db']
        self.song_model = SongModel() 
        self.ratings_collection = self.db['ratings']

    def fetch_songs(self, page=1, per_page=10):
        skip = (page - 1) * per_page
        songs_data = self.song_model.find_songs(limit=per_page, skip=skip)
        return [song.to_dict() for song in songs_data]

    def get_average_difficulty(self, level=None):
        query = {}
        if level:
            query['level'] = int(level)
        songs = self.song_model.find_songs(query=query)
        if not songs:
            return {"message": "No songs found"}
        avg_difficulty = sum([song.difficulty for song in songs]) / len(songs)
        return {"average_difficulty": avg_difficulty}

    def search_songs(self, message):
        query = {
            '$or': [
                {'artist': {'$regex': message, '$options': 'i'}},
                {'title': {'$regex': message, '$options': 'i'}}
            ]
        }
        songs_data = self.song_model.find_songs(query=query)
        return [song.to_dict() for song in songs_data]

    def add_rating(self, song_id, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.ratings_collection.insert_one({'song_id': ObjectId(song_id), 'rating': rating})

    def get_ratings(self, song_id):
        ratings = list(self.ratings_collection.find({'song_id': ObjectId(song_id)}))
        if not ratings:
            return {"message": "No ratings found"}
        avg_rating = sum([r['rating'] for r in ratings]) / len(ratings)
        return {
            "average_rating": avg_rating,
            "highest_rating": max([r['rating'] for r in ratings]),
            "lowest_rating": min([r['rating'] for r in ratings])
        }

