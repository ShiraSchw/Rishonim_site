from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from supabase_client import supabase
import logging

add_book_bp = Blueprint('add_book', __name__)
logging.basicConfig(level=logging.INFO)

@add_book_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        id = len(supabase.table('Books').select("*").execute().data)+1
        category_id = request.form.get('category_id')
        rishon_id = request.form.get('rishon_id')
        book_name = request.form.get('book_name')
        publication_place = request.form.get('publication_place')

        supabase.table('Books').insert({
            "id" : id,
            "category_id": category_id,
            "rishon_id": rishon_id,
            "book_name": book_name,
            "publication_place": publication_place
        }).execute()

        return redirect(url_for('app_routes.add_book.add_book'))

    # שליפת אפשרויות לרשימות הנפתחות
    try:
        categories = supabase.table('Categories').select("*").execute().data
        rishonim = supabase.table("Rishonim").select("id, name, full_name").order("name", desc=False).execute().data

    except Exception as e:
        categories = []
        rishonim = []

    # בניית עץ קטגוריות
    category_tree = {}
    for row in categories:
        cat = row.get("category")
        sub = row.get("sub_category")
        subsub = row.get("sub_sub_category")

        if not cat:
            continue

        category_tree.setdefault(cat, {})

        if sub:
            category_tree[cat].setdefault(sub, {})

            if subsub:
                category_tree[cat][sub].setdefault(subsub, {})

    return render_template('add_book.html', category_tree=category_tree, rishonim=rishonim)

@add_book_bp.route('/add_book/get_category_id')
def get_category_id():
    path = request.args.get('path', '')
    parts = path.strip('/').split('/')

    query = supabase.table("Categories").select("id")

    if len(parts) >= 1:
        query = query.eq("category", parts[0])
    if len(parts) >= 2:
        query = query.eq("sub_category", parts[1])
    if len(parts) >= 3:
        query = query.eq("sub_sub_category", parts[2])

    res = query.execute()
    if res.data:
        return jsonify({"category_id": res.data[0]['id']})
    return jsonify({"category_id": None})

