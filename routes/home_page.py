from flask import Blueprint, app, render_template

home_bp = Blueprint('home', __name__)

@app.route('/')
def home():
    return render_template('home.html')
