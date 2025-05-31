from flask import Blueprint, render_template, request, redirect, url_for, flash
from supabase_client import supabase
import logging

add_book_bp = Blueprint('add_book', __name__)

@add_book_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    logging.basicConfig(level=logging.INFO)
    logging.info("הגעתי לפה!")
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        rishon_id = request.form.get('rishon_id')
        book_name = request.form.get('book_name')
        publication_place = request.form.get('publication_place')

        supabase.table("books").insert({
            "category_id": category_id,
            "rishon_id": rishon_id,
            "book_name": book_name,
            "publication_place": publication_place
        }).execute()

        return redirect(url_for('app_routes.home'))

    # שליפת אפשרויות לרשימות הנפתחות
    try:
        categories = supabase.table('"Categories"').select("*").execute().data
        rishonim = supabase.table('"Rishonim"').select("*").execute().data
        logging.basicConfig(level=logging.INFO)
        logging.info("הגעתי לפה!!")

        logging.basicConfig(level=logging.INFO)
        logging.info("ראשונים:", len(rishonim), rishonim)

    except Exception as e:
        print("שגיאה בשליפת קטגוריות או ראשונים:", e)
        categories = []
        rishonim = []

    return render_template('add_book.html', categories=categories, rishonim=rishonim)
