from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    director = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    synopsis = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(1000), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)
    __table_args__ = (db.UniqueConstraint('title', 'director', 'year'),)

    def __repr__(self):
        return f'{self.title} ({self.year}) - {self.director}'