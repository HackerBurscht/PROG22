from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maindatabase.db"
db = SQLAlchemy(app)

class meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nuullable=1)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


def __repr__(self):
    return "<Task %r>" % self.id

@app.route("/")

def index():
    return render_template("index.html")

if __name__ == "__name__":
    app.run(debug=True)

