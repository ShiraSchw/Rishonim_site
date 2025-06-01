from flask import Blueprint, render_template, request, jsonify
from supabase_client import supabase
import os

search_by_book_bp = Blueprint('search_by_book', __name__)

# דף הבית עם עץ קטגוריות
@search_by_book_bp.route('/search_by_book')
def search_by_book_home():
    # שליפת כל הקטגוריות
    categories = supabase.table('Categories').select("*").execute().data

    # בניית עץ קטגוריות בפורמט מתאים
    category_tree = {}
    for cat in categories:
        caterory = cat['caterory']
        sub_caterory = cat.get('sub_caterory', '')
        sub_sub_caterory = cat.get('sub_sub_caterory', '')
        pointer = category_tree.setdefault(caterory, {})
        if sub_caterory:
            pointer = pointer.setdefault(sub_caterory, {})
        if sub_sub_caterory:
            pointer = pointer.setdefault(sub_sub_caterory, {})

    return render_template('search_by_book_home.html', category_tree=category_tree)

# שליפת תוצאות לפי נתיב קטגוריה
@search_by_book_bp.route('/search_by_book/search')
def search_by_book():
    path = request.args.get('category', '')
    parts = path.split('/')

    # שליפת הקטגוריה המתאימה כדי לדעת את ה-id
    categories = supabase.table("Category").select("*").execute().data
    category_id = None
    for cat in categories:
        if [
            cat['caterory'],
            cat.get('sub_caterory', ''),
            cat.get('sub_sub_category', ''),
        ][:len(parts)] == parts:
            category_id = cat['id']
            break

    if category_id is None:
        return jsonify([])

    # שליפת ספרים מתאימים
    books = supabase.table("Books").select("*").eq("category_id", category_id).execute().data()

    # שליפת רשימת כל הראשונים (לפי id)
    rishon_ids = list(set(book['rishon_id'] for book in books if book.get('rishon_id')))
    rishon_query = supabase.table('Rishonim').select("*").execute()
    rishon_map = {r['id']: r for r in rishon_query.data}

    results = []
    for book in books:
        rishon = rishon_map.get(book.get('rishon_id'), {})
        results.append({
            "book_name": book.get("book_name", ""),
            "publication_place": book.get("publication_place", ""),
            "name": rishon.get("name", ""),
            "full_name": rishon.get("full_name", ""),
            "beit_midrash": rishon.get("beit_midrash", "")
        })

    return jsonify(results)
