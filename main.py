from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from database import db, Movie
from tmdb import IMAGE_BASE_URL, search_movie, get_directors
# import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
Bootstrap(app)


tmdb_movies = []

@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating.desc()).all()
    #This line loops through all the movies
    for i in range(len(all_movies)):
        #This line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = i+1
    db.session.commit()
    return render_template("index.html", movies=all_movies)


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = TextAreaField("Your Review")
    submit = SubmitField("Done")
@app.route("/edit", methods=["POST", "GET"])
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
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

@app.route("/delete", methods=["GET"])
def delete():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)  
    # movie = db.session.get(movie_id)  
    db.session.delete(movie)
    print(" GOT HERE ")
    db.session.commit()
    return redirect(url_for('home'))
    
class AddMovieForm(FlaskForm):
    title = StringField("Movie title", validators=[ DataRequired() ])
    submit = SubmitField("Search")
@app.route("/search", methods=["GET", "POST"])
def search():
    global tmdb_movies
    form = AddMovieForm()
    if form.validate_on_submit():
        tmdb_movies = search_movie(title=form.title.data)
        print(tmdb_movies)
        return render_template('select.html', movies = tmdb_movies, img_base_url = IMAGE_BASE_URL )
    # db.session.commit()
    return render_template('add.html', form=form )


@app.route("/add", methods=["POST"])
def add():
    global tmdb_movies
    data = request.form
    # print(tmdb_movies)
    for value in data.getlist('movie_id'):
        print("ID VALUE: ", value)
        movie_directors = ', '.join(get_directors(value))
        for movie in tmdb_movies:
            print(str(movie["id"])==str(value))
        movie_data = next(movie for movie in tmdb_movies if str(movie["id"])==str(value))
        new_movie = Movie(
            title=movie_data["original_title"],
            director=movie_directors,
            year=movie_data["release_date"].split('-')[0],
            synopsis=movie_data["overview"],
            img_url="https://image.tmdb.org/t/p/w500/"+movie_data["poster_path"]
        )
        db.session.add(new_movie)
        db.session.commit()
    return redirect(url_for('home'))
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("APP IS RUNNING.....")
    app.run(debug=True)
