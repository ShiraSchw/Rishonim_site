from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# בסיס נתונים בזיכרון
rishonim_data = {
    "מסכתות": {
        "זרעים": {
            "ברכות": {
                "תלמוד": []
            }
        }
    }
}

@app.route('/')
def index():
    return render_template("index.html", data=rishonim_data)

@app.route('/add', methods=['GET', 'POST'])
def add_rishon():
    if request.method == 'POST':
        # נתונים מהטופס
        category = request.form['category']
        sub_category = request.form['sub_category']
        section = request.form['section']
        sub_section = request.form['sub_section']

        rishon = {
            'סיווג הספר': request.form['classification'],
            'שם הספר': request.form['book_name'],
            'שם הסופר': request.form['author_name'],
            'כינוי הסופר': request.form['author_nickname'],
            'שיוך': request.form['region'],
            'היכן פורסם': request.form['published']
        }

        # הוספה למקום הנכון
        rishonim_data.setdefault(category, {}).setdefault(sub_category, {}).setdefault(section, {}).setdefault(sub_section, []).append(rishon)
        return redirect(url_for('index'))

    return render_template("add_rishon.html")

if __name__ == '__main__':
    app.run(debug=True)
