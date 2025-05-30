from flask import Blueprint, render_template, jsonify, request
import json

from routes.constants import DATA_FILE, RISHONIM_FILE
from routes.web_function import build_rishonim_category_tree

search_by_rishon_bp = Blueprint('search_by_rishon', __name__)

@search_by_rishon_bp.route('/search_by_rishon_home')
def search_by_rishon_home():
    with open(DATA_FILE, encoding="utf-8") as f:
        rishonim_with_books = json.load(f)

    # קריאה ל־rishonim.json
    with open(RISHONIM_FILE, encoding="utf-8") as f:
        rishonim_list = json.load(f)

    # הוספת כינוי ואזור לכל ראשון
    for r in rishonim_with_books:
        name = r.get("author_name", "")
        r.update(rishonim_list.get(name, {"fullname": "", "region": ""}))

    rishonim_category_tree = build_rishonim_category_tree(rishonim_with_books)
    return render_template('search_by_rishon_home.html', category_tree=rishonim_category_tree, rishonim=rishonim_with_books)

@search_by_rishon_bp.route('search_by_rishon_home/search')
def search_by_rishon():
    with open(DATA_FILE, encoding="utf-8") as f:
        rishonim = json.load(f)

    with open(RISHONIM_FILE, encoding="utf-8") as f:
        rishonim_extra = json.load(f)

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
            enriched = r.copy()
            enriched.update(rishonim_extra.get(r.get("author_name", ""), {"fullname": "", "region": ""}))
            filtered.append(enriched)

    return jsonify(filtered)
