from flask import Flask, render_template, redirect, url_for, request, Blueprint
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from database import Movie, db
from tmdb import IMAGE_BASE_URL, search_movie, get_directors

views_bp = Blueprint('views', __name__)


tmdb_movies = []


@views_bp.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating.desc()).all()
    for i, movie in enumerate(all_movies):
        movie.ranking = i + 1
    db.session.commit()
    return render_template("index.html", movies=all_movies)


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = TextAreaField("Your Review")
    submit = SubmitField("Done")

@views_bp.route("/edit", methods=["POST", "GET"])
def edit():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        if form.rating.data:
            movie.rating = float(form.rating.data)
        if form.review.data:
            movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("edit.html", movie=movie, form=form)

@views_bp.route("/delete", methods=["GET"])
def delete():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('views.home'))

class AddMovieForm(FlaskForm):
    title = StringField("Movie title", validators=[DataRequired()])
    submit = SubmitField("Search")

@views_bp.route("/search", methods=["GET", "POST"])
def search():
    global tmdb_movies
    form = AddMovieForm()
    if form.validate_on_submit():
        tmdb_movies = search_movie(title=form.title.data)
        print(tmdb_movies)
        return render_template('select.html', movies=tmdb_movies, img_base_url=IMAGE_BASE_URL)
    return render_template('add.html', form=form)

@views_bp.route("/add", methods=["POST"])
def add():
    global tmdb_movies
    data = request.form
    for value in data.getlist('movie_id'):
        movie_directors = ', '.join(get_directors(value))
        movie_data = next(movie for movie in tmdb_movies if str(movie["id"]) == str(value))
        new_movie = Movie(
            title=movie_data["original_title"],
            director=movie_directors,
            year=movie_data["release_date"].split('-')[0],
            synopsis=movie_data["overview"],
            img_url="https://image.tmdb.org/t/p/w500/" + movie_data["poster_path"]
        )
        db.session.add(new_movie)
        db.session.commit()
    return redirect(url_for('views.home'))

# ... (rest of the routes)
