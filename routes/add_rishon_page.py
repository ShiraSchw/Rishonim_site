from flask import Blueprint, render_template, request, redirect, url_for, flash
import json
import os

add_bp = Blueprint('add', __name__)

@add_bp.route('/add', methods=['GET', 'POST'])
def add_rishon():
    # קריאה לעץ הקטגוריות
    with open("categories.json", encoding="utf-8") as f:
        category_tree = json.load(f)

    if request.method == 'POST':
        # בדיקה בסיסית
        if not request.form.get("main_category"):
            flash("חובה לבחור קטגוריה ראשית.", "error")
            return redirect(url_for('add.add_rishon'))

        # בניית האובייקט של ה'ראשון'
        new_rishon = {
            "main_category": request.form.get("main_category"),
            "sub_category": request.form.get("sub_category", ""),
            "sub_sub_category": request.form.get("sub_sub_category", ""),
            "sub_sub_sub_category": request.form.get("sub_sub_sub_category", ""),
            "book_name": request.form.get("book_name", ""),
            "author_name": request.form.get("author_name", ""),
            "author_nickname": request.form.get("author_nickname", ""),
            "region": request.form.get("region", ""),
            "publication": request.form.get("published", "")
        }

        # קריאה ל־data.json ושמירה
        try:
            if not os.path.exists("data.json"):
                data = []
            else:
                with open("data.json", "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = []

            data.append(new_rishon)

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            flash("הראשון נוסף בהצלחה!", "success")
            return redirect(url_for('app_routes.add.add_rishon'))

        except Exception as e:
            flash(f"שגיאה בשמירת הנתונים: {str(e)}", "error")
            return redirect(url_for('app_routes.add.add_rishon'))

    # GET רגיל
    return render_template('add_rishon.html', category_tree=category_tree)
