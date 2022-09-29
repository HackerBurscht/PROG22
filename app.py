from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime, timedelta
from collections import Counter
import json

app = Flask(__name__, static_url_path="/static")
week_key = ""
display_week = 0


@app.route("/", methods=["POST", "GET"])
def index():
    with open('content.json', "r") as f, open("meals.json", "r") as f2:
        d = json.load(f)
        f.close()
        d2 = json.load(f2)
        f2.close()

    max_meals = len([d][0]["content-file"])
    div_meals = len(Counter(d2).keys())
    most_meal, most_meal_amount = Counter(d2).most_common(1)[0]
    # Counter inspired by https://datagy.io/python-count-unique-values-list/
    # most_common()-How-To from https://www.delftstack.com/howto/python/python-counter-most-common/
    # delivers a tuple inside a dict

    if display_week == 0:
        week_start = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
        week_end = week_start + timedelta(days=7)
        week_i1 = week_start
        week_i2 = week_end
        week_end_display = week_end.strftime("%d.%m.%Y")
        week_start_display = week_start.strftime("%d.%m.")

    else:
        week_start = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(
            days=display_week * 7)
        week_end = week_start + timedelta(days=7)
        week_i1 = week_start
        week_i2 = week_end
        week_end_display = week_end.strftime("%d.%m.%Y")
        week_start_display = week_start.strftime("%d.%m.")

    i = week_i1
    n = 0 + display_week * 7
    x_list = []

    while i < week_i2:
        j = i.strftime("%d.%m.%Y")
        try:
            x_list.append(str(d["content-file"][n][j]["content"]))
        except:
            x_list.append(". . . . . . . . . . . ")
        i += timedelta(days=1)
        n += 1

    return render_template("index.html", week_start_display=week_start_display, week_end_display=week_end_display,
                           return_mo=x_list[0], return_di=x_list[1], return_mi=x_list[2], return_do=x_list[3],
                           return_fr=x_list[4], return_sa=x_list[5], return_so=x_list[6], max_meals=max_meals,
                           div_meals=div_meals, most_meal=most_meal, most_meal_amount=most_meal_amount)


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

        with open("content.json", "r+") as f:
            file_data = json.load(f)
            max = (len([file_data][0]["content-file"]))
            i = 0
            while i < max:
                if date in [file_data][0]["content-file"][i]:
                    [file_data][0]["content-file"][i].update(temp_dic)
                    f.seek(0)
                    json.dump(file_data, f, indent=4)
                i += 1
            else:
                file_data["content-file"].append(temp_dic)
                f.seek(0)
                json.dump(file_data, f, indent=4)
        f.close()
        with open("meals.json", "r+") as f2:
            load = json.load(f2)
            load.append(content)
            f2.seek(0)
            json.dump(load, f2)
        f2.close()
        return redirect("/")


@app.route("/mo", methods=["POST", "GET"])
def save_mo():
    week_key = "mo"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
    planned_date_key = planned_date_key + timedelta(days=display_week * 7)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/di", methods=["POST"])
def save_di():
    week_key = "di"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=1)
    planned_date_key = planned_date_key + timedelta(days=display_week * 7)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/mi", methods=["POST"])
def save_mi():
    week_key = "mi"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=2)
    planned_date_key = planned_date_key + timedelta(days=display_week * 7)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/do", methods=["POST"])
def save_do():
    week_key = "do"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=3)
    planned_date_key = planned_date_key + timedelta(days=display_week * 7)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/fr", methods=["POST"])
def save_fr():
    week_key = "fr"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=4)
    planned_date_key = planned_date_key + timedelta(days=display_week * 7)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/sa", methods=["POST"])
def save_sa():
    week_key = "sa"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=5)
    planned_date_key = planned_date_key + timedelta(days=display_week * 7)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/so", methods=["POST"])
def save_so():
    week_key = "so"
    planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=6)
    planned_date_key = planned_date_key + timedelta(days=display_week * 7)
    planned_date_key = planned_date_key.strftime("%d.%m.%Y")
    save_info(week_key, planned_date_key)
    return redirect("/")


@app.route("/next")
def next_week():
    global display_week
    display_week += 1
    return redirect("/")


@app.route("/prev")
def prev_week():
    global display_week
    display_week -= 1
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
