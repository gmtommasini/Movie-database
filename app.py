from flask import Flask
from flask_bootstrap import Bootstrap
from database import db
from api import api_bp
from views import views_bp
# import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
Bootstrap(app)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(views_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("APP IS RUNNING.....")
    app.run(debug=True)
