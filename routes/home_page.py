from flask import Blueprint, render_template, jsonify, request
import json

from routes.constants import DATA_FILE
from routes.web_function import build_rishonim_category_tree

home_bp = Blueprint('home', __name__)

with open(DATA_FILE, encoding="utf-8") as f:
    rishonim = json.load(f)

rishonim_category_tree = build_rishonim_category_tree(rishonim)

@home_bp.route('/')
def index():
    return render_template('index.html', category_tree=rishonim_category_tree, rishonim=rishonim)

@home_bp.route('/search')
def search():
    category_path = request.args.get('category', '')
    path_parts = category_path.split('/')

    filtered = []
    for r in rishonim:
        cat_path = [
            r['main_category'],
            r['sub_category'],
            r['sub_sub_category'],
            r.get('sub_sub_sub_category', '')
        ]
        if path_parts == cat_path[:len(path_parts)]:
            filtered.append(r)

    return jsonify(filtered)