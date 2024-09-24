import unittest
from flask import json
from app import create_app
from unittest.mock import patch
from app.config import TestConfig

class SongsApiTestCase(unittest.TestCase):

    def setUp(self):
        
        self.app = create_app()
        self.app.config.from_object(TestConfig)  
        self.client = self.app.test_client()
        
       
        self.patcher = patch('app.services.song_service.MongoClient', return_value=MockMongoClient())
        self.patcher.start()
        
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.patcher.stop()
        self.app_context.pop()

    def test_post_rating(self):
        rating_data = {
            "song_id": "1",  
            "rating": 5
        }
        
        response = self.client.post('/songs/rate', json=rating_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('rating', json.loads(response.data))

    def test_search_songs(self):
        query = "Song A"
        response = self.client.get(f'/songs/search?message={query}')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], "Song A")

    def test_get_all_songs(self):
        response = self.client.get('/songs')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)  

    def test_get_song_by_id(self):
        response = self.client.get('/songs/1')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['title'], "Song A")

    def test_post_new_song(self):
        new_song = {
            "id": "4",
            "artist": "Artist D",
            "title": "Song D",
            "difficulty": "Medium",
            "level": 2,
            "released": "2024-01-01"
        }
        response = self.client.post('/songs', json=new_song)
        self.assertEqual(response.status_code, 201)

    def test_put_update_song(self):
        updated_song = {
            "artist": "Artist A Updated",
            "title": "Song A Updated",
            "difficulty": "Medium",
            "level": 2,
            "released": "2021-01-01"
        }
        response = self.client.put('/songs/1', json=updated_song)
        self.assertEqual(response.status_code, 200)

    def test_delete_song(self):
        response = self.client.delete('/songs/1')
        self.assertEqual(response.status_code, 204)

# Mock MongoDB client for testing
class MockMongoClient:
    def __init__(self):
        self.db = MockDatabase()

class MockDatabase:
    def __init__(self):
        self.songs_collection = [
            {
                "id": "1",
                "artist": "Artist A",
                "title": "Song A",
                "difficulty": "Easy",
                "level": 1,
                "released": "2021-01-01"
            },
            {
                "id": "2",
                "artist": "Artist B",
                "title": "Song B",
                "difficulty": "Medium",
                "level": 2,
                "released": "2022-01-01"
            },
            {
                "id": "3",
                "artist": "Artist C",
                "title": "Song C",
                "difficulty": "Hard",
                "level": 3,
                "released": "2023-01-01"
            }
        ]

    def songs(self):
        return self.songs_collection

    def insert_one(self, song):
        self.songs_collection.append(song)

    def find(self, *args, **kwargs):
        if 'message' in kwargs:
            return [song for song in self.songs_collection if kwargs['message'].lower() in song['title'].lower()]
        return self.songs_collection

    def find_one(self, song_id):
        for song in self.songs_collection:
            if song['id'] == song_id:
                return song
        return None

    def delete_one(self, song_id):
        self.songs_collection = [song for song in self.songs_collection if song['id'] != song_id]

if __name__ == '__main__':
    unittest.main()
