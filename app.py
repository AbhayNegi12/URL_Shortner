from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(6), unique=True, nullable=False)

def generate_short_url():
    # Generate a random 6-character hexadecimal string
    short_url = secrets.token_hex(3)[:6] 
    return short_url

# Create the tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        existing_url = URL.query.filter_by(original_url=original_url).first()
        if existing_url:
            return render_template('index.html', short_url=existing_url.short_url)
        short_url = generate_short_url()
        new_url = URL(original_url=original_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(link.original_url)

if __name__ == '__main__':
    app.run(debug=True)
