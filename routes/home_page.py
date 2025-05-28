from flask import Blueprint, render_template
import json

home_bp = Blueprint('home', __name__)

with open("categories.json", encoding="utf-8") as f:
    category_tree = json.load(f)

with open("data.json", encoding="utf-8") as f:
    rishonim = json.load(f)

@home_bp.route('/')
def index():
    return render_template('index.html', category_tree=category_tree, rishonim=rishonim)
