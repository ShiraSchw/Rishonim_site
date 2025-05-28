from flask import Blueprint, render_template, jsonify, request
import json


home_bp = Blueprint('home', __name__)

with open("categories.json", encoding="utf-8") as f:
    category_tree = json.load(f)

with open("data.json", encoding="utf-8") as f:
    rishonim = json.load(f)

@home_bp.route('/')
def index():
    return render_template('index.html', category_tree=category_tree, rishonim=rishonim)

@home_bp.route('/search')
def search():
    category_path = request.args.get('category', '')
    path_parts = category_path.split('/')

    filtered = []
    for r in rishonim:
        cat_path = [r['main_category'], r['sub_category'], r['tractate']]
        if path_parts == cat_path[:len(path_parts)]:
            filtered.append(r)

    return jsonify(filtered)