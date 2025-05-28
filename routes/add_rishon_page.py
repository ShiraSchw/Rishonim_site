from flask import Blueprint, render_template, request, redirect
import json

add_bp = Blueprint('add', __name__)

@add_bp.route('/add', methods=['GET', 'POST'])
def add_rishon():
    with open("categories.json", encoding="utf-8") as f:
        category_tree = json.load(f)

    if request.method == 'POST':
        new_entry = {
            "סיווג הספר": request.form["category_path"],
            "שם הספר": request.form["book_name"],
            "שם הסופר": request.form["author_name"],
            "כינוי הסופר": request.form["author_nickname"],
            "שיוך": request.form["origin"],
            "היכן פורסם": request.form["published"]
        }

        with open("data.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(new_entry)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)

        return redirect('/')

    return render_template('add_rishon.html', category_tree=category_tree)
