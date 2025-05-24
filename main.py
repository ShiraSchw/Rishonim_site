from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    rishonim = load_data()

    tree = {}
    for r in rishonim:
        a = r['main_category']
        b = r.get('sub_category')
        c = r.get('sub_sub_category')
        d = r.get('sub_sub_sub_category')

        tree.setdefault(a, {})
        if b:
            tree[a].setdefault(b, {})
            if c:
                tree[a][b].setdefault(c, {})
                if d:
                    tree[a][b][c].setdefault(d, [])
                    tree[a][b][c][d].append(r)
                else:
                    tree[a][b][c].setdefault('_books', []).append(r)
            else:
                tree[a][b].setdefault('_books', []).append(r)
        else:
            tree[a].setdefault('_books', []).append(r)

    return render_template("index.html", tree=tree)


@app.route('/add', methods=['GET', 'POST'])
def add_rishon():
    if request.method == 'POST':
        new_rishon = {
            'main_category': request.form['main_category'],
            'sub_category': request.form.get('sub_category'),
            'sub_sub_category': request.form.get('sub_sub_category'),
            'sub_sub_sub_category': request.form.get('sub_sub_sub_category'),
            'book_name': request.form['book_name'],
            'author_name': request.form['author_name'],
            'author_nickname': request.form['author_nickname'],
            'region': request.form['region'],
            'publication': request.form['publication']
        }
        data = load_data()
        data.append(new_rishon)
        save_data(data)
        return redirect('/')
    return render_template("add_rishon.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
