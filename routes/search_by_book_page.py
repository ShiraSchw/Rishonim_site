import httpx
from flask import Blueprint, render_template, request, jsonify
from supabase_client import supabase, KEY_TABLE
import os

search_by_book_bp = Blueprint('search_by_book', __name__)

# דף הבית עם עץ קטגוריות
@search_by_book_bp.route('/search_by_book')
def search_by_book_home():
    # שליפת כל הקטגוריות מהטבלה
    categories = supabase.table("Categories").select("*").execute().data

    # בניית עץ הקטגוריות
    category_tree = {}
    for row in categories:
        cat = row.get("category")
        sub = row.get("sub_category")
        subsub = row.get("sub_sub_category")

        if not cat:
            continue

        category_tree.setdefault(cat, {})

        if sub:
            category_tree[cat].setdefault(sub, [])

            if subsub:
                category_tree[cat][sub].append(subsub)

    return render_template("search_by_book_home.html", category_tree=category_tree)


# שליפת תוצאות לפי נתיב קטגוריה
@search_by_book_bp.route('/search_by_book/search')
def search_by_book():
    path = request.args.get('category', '')
    parts = path.strip('/').split('/')  # למשל: ["category", "sub", "subsub"]

    query = supabase.table("Categories").select("id")

    if len(parts) >= 1:
        query = query.eq("category", parts[0])
    if len(parts) >= 2:
        query = query.eq("sub_category", parts[1])
    if len(parts) >= 3:
        query = query.eq("sub_sub_category", parts[2])

    res = query.execute()
    categories = res.data

    if not categories:
        return jsonify([])

    category_id = categories[0]['id']

    # שליפת ספרים
    books_res = supabase.table("Books").select("*").eq("category_id", category_id).execute()
    books = books_res.data

    if not books:
        return jsonify([])

    # שליפת כל הראשונים הרלוונטיים לפי rishon_id
    rishon_ids = list(set(book['rishon_id'] for book in books if book.get('rishon_id')))
    rishon_map = {}
    if rishon_ids:
        rishon_query = supabase.table('Rishonim').select("*").in_("id", rishon_ids).execute()
        rishon_map = {r['id']: r for r in rishon_query.data}

    # בניית התוצאה
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
