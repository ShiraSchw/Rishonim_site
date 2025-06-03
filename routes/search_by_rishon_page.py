from flask import Blueprint, render_template, request, jsonify

from supabase_client import supabase
import logging

search_by_rishon_bp = Blueprint('search_by_rishon', __name__)
logging.basicConfig(level=logging.INFO)

# דף הבית עם עץ קטגוריות
@search_by_rishon_bp.route('/search_by_rishon')
def search_by_rishon_home():
    # שליפת כל הראשונים (name + full_name)
    rishonim = supabase.table("Rishonim").select("id, name, full_name").order("name", desc=False).execute().data

    return render_template("search_by_rishon_home.html", rishonim=rishonim)


# שליפת תוצאות לפי נתיב קטגוריה
@search_by_rishon_bp.route('/search_by_rishon/search')
def search_by_rishon():
    rishon_id = request.args.get("rishon_id")
    if not rishon_id:
        return jsonify([])

    books_res = supabase.table("Books").select("*").eq("rishon_id", rishon_id).execute()
    books = books_res.data

    rishon = supabase.table("Rishonim").select("*").eq("id", rishon_id).single().execute().data

    results = []
    for book in books:
        results.append({
            "book_name": book.get("book_name", ""),
            "publication_place": book.get("publication_place", ""),
            "name": rishon.get("name", ""),
            "full_name": rishon.get("full_name", ""),
            "beit_midrash": rishon.get("beit_midrash", "")
        })

    return jsonify(results)

@search_by_rishon_bp.route('/search_by_rishon/update_publication_place/<book_id>', methods=['POST'])
def update_publication_place(book_id):
    data = request.json
    new_place = data.get('publication_place', '')
    try:
        supabase.table("Books").update({"publication_place": new_place}).eq("id", book_id).execute()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
