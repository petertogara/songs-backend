from flask_restx import Namespace, Resource, fields
from flask import request
from ..services.song_service import SongService

api = Namespace('songs', description="Yousicians Songs API")
song_service = SongService()

# Model for Swagger UI - Song
song_model = api.model('Song', {
    'artist': fields.String(required=True, description="Artist of the song"),
    'title': fields.String(required=True, description="Title of the song"),
    'difficulty': fields.Float(required=True, description="Difficulty level of the song"),
    'level': fields.Integer(required=True, description="Skill level of the song"),
    'released': fields.String(required=True, description="Release date of the song in YYYY-MM-DD format")
})

# Model for Swagger UI - Rating
rating_model = api.model('Rating', {
    'song_id': fields.String(required=True, description="ID of the song being rated"),
    'rating': fields.Integer(min=1, max=5, required=True, description="Rating value between 1 and 5")
})

@api.route('/')
class SongList(Resource):
    @api.doc(params={'page': 'Page number (default: 1)', 'per_page': 'Number of songs per page (default: 10)'})
    @api.marshal_list_with(song_model)
    def get(self):
        """Return a list of paginated songs"""
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        return song_service.fetch_songs(page, per_page), 200

@api.route('/difficulty')
class SongDifficulty(Resource):
    @api.doc(params={'level': 'Optional filter by song level'})
    def get(self):
        """Return average difficulty of songs, optionally filtered by level"""
        level = request.args.get('level')
        return song_service.get_average_difficulty(level), 200

@api.route('/search')
class SongSearch(Resource):
    @api.doc(params={'message': 'Search string for song title or artist'})
    @api.marshal_list_with(song_model)
    def get(self):
        """Search for songs by artist or title"""
        message = request.args.get('message')
        return song_service.search_songs(message), 200

@api.route('/rate')
class SongRating(Resource):
    @api.expect(rating_model)
    def post(self):
        """Add rating for a song"""
        data = request.get_json()
        song_service.add_rating(data['song_id'], data['rating'])
        return {'message': 'Rating added successfully'}, 201

@api.route('/ratings/<string:song_id>')
class SongRatings(Resource):
    def get(self, song_id):
        """Return average, highest, and lowest rating for a song"""
        return song_service.get_ratings(song_id), 200

