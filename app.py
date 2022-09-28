from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime, timedelta
import json

app = Flask(__name__, static_url_path="/static")
week_key = ""


@app.route("/", methods=["POST", "GET"])
def index():
    # Das Datum des ersten und des letzten Tages der aktuellen Woche wird berechnet und als String formatiert.
    week_start = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
    week_i1 = week_start
    week_end = week_start + timedelta(days=7)
    week_i2 = week_end
    week_end = week_end.strftime("%d.%m.%Y")
    week_start = week_start.strftime("%d.%m. bis ")

    with open('content.json', "r+") as f:
        d = json.load(f)
        f.close()
        i = week_i1
        n = 0
        x_list = []
        while i < week_i2:
            j = i.strftime("%d.%m.%Y")
            x = str(d["content-file"][n][j]["content"])
            x_list.append(x)
            i += timedelta(days=1)
            j = i.strftime("%d.%m.%Y")
            n += 1
        return_mo = x_list[0]
        return_di = x_list[1]
        return_mi = x_list[2]
        return_do = x_list[3]
        return_fr = x_list[4]
        return_sa = x_list[5]
        return_so = x_list[6]

        return render_template("index.html", week_start=week_start, week_end=week_end, return_mo=return_mo,
                               return_di=return_di, return_mi=return_mi, return_do=return_do, return_fr=return_fr,
                               return_sa=return_sa, return_so=return_so)


def save_info(week_key, planned_date_key):
    content = request.form.get(week_key)
    if content == "":
        return redirect("/")
    else:
        date = planned_date_key
        temp_dic = {}
        temp_dic[date] = {}
        temp_dic[date]["content"] = content
        temp_dic[date]["weekday"] = week_key
        with open('content.json', 'r+') as f:
            file_data = json.load(f)
            if date in [file_data][0]["content-file"][0]:
                print(date)
                [file_data][0]["content-file"][0].update(temp_dic)
                f.seek(0)
                json.dump(file_data, f, indent=4)
            else:
                file_data["content-file"].append(temp_dic)
                f.seek(0)
                json.dump(file_data, f, indent=4)
        return redirect("/")


@app.route("/mo", methods=["POST", "GET"])
def save_mo():
    week_key = "mo"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/di", methods=["POST"])
def save_di():
    week_key = "di"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=1)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/mi", methods=["POST"])
def save_mi():
    week_key = "mi"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=2)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/do", methods=["POST"])
def save_do():
    week_key = "do"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=3)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/fr", methods=["POST"])
def save_fr():
    week_key = "fr"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=4)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/sa", methods=["POST"])
def save_sa():
    week_key = "sa"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=5)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/so", methods=["POST"])
def save_so():
    week_key = "so"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=6)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/About")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/stats")
def stats():
    return render_template("stats.html")


if __name__ == "__main__":
    app.run(debug=True)
