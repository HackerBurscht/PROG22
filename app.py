from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_url_path="/static")  # Fick mein Leben. 5 Stunden für ein IMG.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mealy.db"
db = SQLAlchemy(app)


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    weekday = db.Column(db.String(2), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        content = request.form.get("form_mo")
        if content == "":
            return redirect("/")
        elif content != "":
            new_content = Meal(content=content, weekday="Mo")

        try:
            db.session.add(new_content)
            db.session.commit()
            return redirect("/")
        except:
            return "Gab nen Fehler"

    else:
        all_content = Meal.query.order_by(Meal.date_created).all()
        return render_template("index.html")


@app.route("/About")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
