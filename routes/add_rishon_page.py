from flask import Blueprint, render_template, request, redirect, url_for, flash
import json

add_bp = Blueprint('add', __name__)

@add_bp.route('/add', methods=['GET', 'POST'])
def add_rishon():
    with open("categories.json", encoding="utf-8") as f:
        category_tree = json.load(f)

    if request.method == 'POST':
        # בדיקה שחובה: רק קטגוריה עליונה
        if not request.form.get("main_category"):
            return "Main category is required", 400

        # בנה את הנתיב לפי מה שנשלח בפועל
        category_parts = [request.form.get(part) for part in [
            "main_category", "sub_category", "tractate", "text_type"
        ] if request.form.get(part)]

        category_path = " > ".join(category_parts)

        # שדות נוספים שנדרשים
        try:
            new_rishon = {
                "main_category": request.form.get("main_category"),
                "sub_category": request.form.get("sub_category", ""),
                "sub_sub_category": request.form.get("sub_sub_category", ""),
                "sub_sub_sub_category": request.form.get("sub_sub_sub_category", ""),
                "book_name": request.form.get("book_name"),
                "author_name": request.form.get("author_name"),
                "author_nickname": request.form.get("author_nickname"),
                "region": request.form.get("region"),
                "publication": request.form.get("published")
                }
        except KeyError as e:
            return f"Missing required field: {e.args[0]}", 400

        # כתיבה לקובץ JSON
        with open("data.json", "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(new_rishon)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()

        flash("הראשון נוסף בהצלחה!")
        return redirect(url_for('add.add_rishon'))

    return render_template('add_rishon.html', category_tree=category_tree)
