from flask import Blueprint, render_template, request, jsonify
from supabase_client import supabase

search_by_beit_midrash_bp = Blueprint("search_by_beit_midrash", __name__)

@search_by_beit_midrash_bp.route('/search_by_beit_midrash')
def search_by_beit_midrash_home():
    # שליפת כל בתי המדרש הייחודיים מהטבלה
    response = supabase.table("Rishonim").select("beit_midrash").execute()
    data = response.data
    beit_midrash_list = sorted(set(r['beit_midrash'] for r in data if r['beit_midrash']))
    return render_template("search_by_beit_midrash_home.html", beit_midrash_list=beit_midrash_list)

@search_by_beit_midrash_bp.route('/search_by_beit_midrash/search')
def search_by_beit_midrash():
    beit_midrash = request.args.get("beit_midrash")
    if not beit_midrash:
        return jsonify([])

    # שליפת כל הראשונים מבית המדרש הזה
    rishonim_res = supabase.table("Rishonim").select("*").eq("beit_midrash", beit_midrash).execute()
    rishonim = rishonim_res.data
    rishon_map = {r['id']: r for r in rishonim}
    rishon_ids = list(rishon_map.keys())

    # שליפת כל הספרים של אותם ראשונים
    books_res = supabase.table("Books").select("*").in_("rishon_id", rishon_ids).execute()
    books = books_res.data

    # בניית התוצאה
    results = []
    for book in books:
        rishon = rishon_map.get(book.get("rishon_id"), {})
        results.append({
            "book_name": book.get("book_name", ""),
            "publication_place": book.get("publication_place", ""),
            "name": rishon.get("name", ""),
            "full_name": rishon.get("full_name", ""),
            "beit_midrash": rishon.get("beit_midrash", "")
        })

    return jsonify(results)

@search_by_beit_midrash_bp.route('/search_by_beit_midrash/update_publication_place/<book_id>', methods=['POST'])
def update_publication_place(book_id):
    data = request.json
    new_place = data.get('publication_place', '')
    try:
        supabase.table("Books").update({"publication_place": new_place}).eq("id", book_id).execute()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
