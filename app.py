from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__, static_url_path="/static")  # Fick mein Leben. 5 Stunden für ein IMG.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mealy.db"
db = SQLAlchemy(app)
week_key = ""


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    weekday = db.Column(db.String(2), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    planned_date = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    # Das Datum des ersten und des letzten Tages, der aktuellen Woche, wird berechnet und als String formatiert.
    week_start = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
    week_end = week_start + timedelta(days=7)
    week_end = week_end.strftime("%d.%m.%Y")
    week_start = week_start.strftime("%d.%m. bis ")


    item_mo = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
    item_mo = item_mo.strftime("%d.%m.%Y")
    ph_mo = Meal.query.filter_by(planned_date=item_mo)
    print(ph_mo)


    if request.method == "POST":
        pass

    else:
        all_content = Meal.query.order_by(Meal.date_created).all()
        return render_template("index.html", pass_week_start=week_start, pass_week_end=week_end, ph_mo=ph_mo)


def savedb(week_key, planned_date_key):
    content = request.form.get(week_key)
    if content == "":
        return redirect("/")
    elif content != "":
        new_content = Meal(content=content, weekday=week_key, planned_date=planned_date_key)

    try:
        db.session.add(new_content)
        db.session.commit()
    except:
        return "Gab nen Fehler"


@app.route("/mo", methods=["POST", "GET"])
def save_mo():
    week_key = "mo"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    savedb(week_key, planned_date_key)
    return redirect("/")


@app.route("/di", methods=["POST"])
def save_di():
    week_key = "di"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=1)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    savedb(week_key, planned_date_key)
    return redirect("/")


@app.route("/mi", methods=["POST"])
def save_mi():
    week_key = "mi"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=2)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    savedb(week_key, planned_date_key)
    return redirect("/")


@app.route("/do", methods=["POST"])
def save_do():
    week_key = "do"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=3)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    savedb(week_key, planned_date_key)
    return redirect("/")


@app.route("/fr", methods=["POST"])
def save_fr():
    week_key = "fr"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=4)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    savedb(week_key, planned_date_key)
    return redirect("/")


@app.route("/sa", methods=["POST"])
def save_sa():
    week_key = "sa"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=5)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    savedb(week_key, planned_date_key)
    return redirect("/")


@app.route("/so", methods=["POST"])
def save_so():
    week_key = "so"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=6)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    savedb(week_key, planned_date_key)
    return redirect("/")

@app.route("/About")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
