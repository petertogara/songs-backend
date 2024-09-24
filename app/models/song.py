class Song:
    def __init__(self, artist, title, difficulty, level, released):
        self.artist = artist
        self.title = title
        self.difficulty = difficulty
        self.level = level
        self.released = released

    def to_dict(self):
        return {
            "artist": self.artist,
            "title": self.title,
            "difficulty": self.difficulty,
            "level": self.level,
            "released": self.released,
        }

    @staticmethod
    def from_dict(data):
        return Song(
            artist=data.get('artist'),
            title=data.get('title'),
            difficulty=data.get('difficulty'),
            level=data.get('level'),
            released=data.get('released'),
        )
