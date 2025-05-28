from flask import Blueprint, render_template, request, redirect, url_for
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
            new_entry = {
                "סיווג הספר": category_path,
                "שם הספר": request.form["book_name"],
                "שם הסופר": request.form["author_name"],
                "כינוי הסופר": request.form["author_nickname"],
                "שיוך": request.form["region"],
                "היכן פורסם": request.form["published"]
            }
        except KeyError as e:
            return f"Missing required field: {e.args[0]}", 400

        # כתיבה לקובץ JSON
        with open("data.json", "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(new_entry)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)

        return redirect(url_for("app_routes.home.index"))

    return render_template('add_rishon.html', category_tree=category_tree)
