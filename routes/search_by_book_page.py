from flask import Blueprint, render_template, request, jsonify

from routes.web_function import build_category_tree
from supabase_client import supabase
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

    return render_template("search_by_book.html", category_tree=category_tree)


# שליפת תוצאות לפי נתיב קטגוריה
@search_by_book_bp.route('/search_by_book/search')
def search_by_book():
    path = request.args.get('category', '')
    parts = path.strip('/').split('/')  # למשל: ["category", "sub", "subsub"]

    # יצירת תנאים דינמיים לפי מספר החלקים בנתיב
    filters = []
    if len(parts) >= 1:
        filters.append(f"category.eq.{parts[0]}")
    if len(parts) >= 2:
        filters.append(f"sub_category.eq.{parts[1]}")
    if len(parts) == 3:
        filters.append(f"sub_sub_category.eq.{parts[2]}")

    filter_query = '&'.join(filters)

    # שליפת category_id לפי הנתיב
    url = f"https://{SUPABASE_PROJECT_ID}.supabase.co/rest/v1/Categories?select=id&{filter_query}"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    }

    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    categories = response.json()

    if not categories:
        return jsonify([])

    category_id = categories[0]['id']

    # שליפת ספרים עם category_id מתאים
    books = supabase.table("Books").select("*").eq("category_id", category_id).execute().data

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
