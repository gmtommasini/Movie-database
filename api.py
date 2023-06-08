from flask import Blueprint, jsonify, request
from database import Movie, db
from tmdb import IMAGE_BASE_URL, search_movie, get_directors

api_bp = Blueprint('api', __name__)

@api_bp.route("/movies", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    movies_data = []
    for movie in movies:
        movie_data = {
            'id': movie.id,
            'title': movie.title,
            'director': movie.director,
            'year': movie.year,
            'synopsis': movie.synopsis,
            'rating': movie.rating,
            'ranking': movie.ranking,
            'review': movie.review,
            'img_url': movie.img_url
        }
        movies_data.append(movie_data)
    return jsonify(movies_data)

@api_bp.route("/movies", methods=["POST"])
def add_movie():
    movie_data = request.get_json()
    new_movie = Movie(
        title=movie_data['title'],
        director=movie_data['director'],
        year=movie_data['year'],
        synopsis=movie_data['synopsis'],
        rating=movie_data['rating'],
        ranking=movie_data['ranking'],
        review=movie_data['review'],
        img_url=movie_data['img_url']
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'message': 'Movie added successfully'})

@api_bp.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        movie_data = {
            'id': movie.id,
            'title': movie.title,
            'director': movie.director,
            'year': movie.year,
            'synopsis': movie.synopsis,
            'rating': movie.rating,
            'ranking': movie.ranking,
            'review': movie.review,
            'img_url': movie.img_url
        }
        return jsonify(movie_data)
    else:
        return jsonify({'message': 'Movie not found'})

# ... (other API routes)
