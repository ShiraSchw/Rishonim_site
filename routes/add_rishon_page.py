from flask import Blueprint, render_template, request, redirect, url_for, flash
import json
import os

from routes.constants import CATEGORY_FILE, DATA_FILE, RISHONIM_FILE

add_bp = Blueprint('add', __name__)

@add_bp.route('/add', methods=['GET', 'POST'])
def add_rishon():
    with open(RISHONIM_FILE, encoding='utf-8') as f:
        rishonim_data = json.load(f)

    rishon_names = list(rishonim_data.keys())

    with open(CATEGORY_FILE, encoding="utf-8") as f:
        category_tree = json.load(f)

    if request.method == 'POST':
        if not request.form.get("main_category"):
            flash("חובה לבחור קטגוריה ראשית.", "error")
            return redirect(url_for('add.add_rishon'))

        new_rishon = {
            "main_category": request.form.get("main_category"),
            "sub_category": request.form.get("sub_category", ""),
            "sub_sub_category": request.form.get("sub_sub_category", ""),
            "sub_sub_sub_category": request.form.get("sub_sub_sub_category", ""),
            "book_name": request.form.get("book_name", ""),
            "author_name": request.form.get("author_name", ""),
            "publication": request.form.get("published", "")
        }

        try:
            if not os.path.exists(DATA_FILE):
                data = []
            else:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = []

            data.append(new_rishon)

            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            flash("הראשון נוסף בהצלחה!", "success")
            return redirect(url_for('add.add_rishon'))

        except Exception as e:
            flash(f"שגיאה בשמירת הנתונים: {str(e)}", "error")
            return redirect(url_for('add.add_rishon'))

    # אם זו בקשת GET רגילה
    return render_template('add_rishon.html', category_tree=category_tree, rishon_options=rishon_names)

