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
        rishonim = supabase.table('Rishonim').select("*").execute().data

    except Exception as e:
        categories = []
        rishonim = []

    return render_template('add_book.html', categories=categories, rishonim=rishonim)
