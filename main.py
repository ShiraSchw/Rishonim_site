from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rishonim.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Rishon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    book_name = db.Column(db.String(100))
    author_name = db.Column(db.String(100))
    author_nickname = db.Column(db.String(100))
    region = db.Column(db.String(100))
    publication = db.Column(db.String(100))

@app.route('/')
def index():
    rishonim = Rishon.query.all()
    return render_template("index.html", rishonim=rishonim)

@app.route('/add', methods=['GET', 'POST'])
def add_rishon():
    if request.method == 'POST':
        new_rishon = Rishon(
            category=request.form['category'],
            book_name=request.form['book_name'],
            author_name=request.form['author_name'],
            author_nickname=request.form['author_nickname'],
            region=request.form['region'],
            publication=request.form['publication']
        )
        db.session.add(new_rishon)
        db.session.commit()
        return redirect('/')
    return render_template("add_rishon.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=10000)

