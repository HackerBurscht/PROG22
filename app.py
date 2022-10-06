# Python libraries
####################################################################################################################
# general
from flask import Flask, render_template, url_for, request, redirect
import json

# numbers and time
from datetime import datetime, timedelta
from collections import Counter
from random import sample

# init and necessary global values
####################################################################################################################
app = Flask(__name__, static_url_path="/static")

display_week = 0
forgotten_meals = []
weekday = {
    "0": "mo",
    "1": "di",
    "2": "mi",
    "3": "do",
    "4": "fr",
    "5": "sa",
    "6": "so"
}


@app.route("/", methods=["POST", "GET"])
def index():
    # Get Values to display the header-statistics on the index page:
    ####################################################################################################################
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

    # Set the current or selected week and create values to return on the index page:
    ####################################################################################################################
    if display_week == 0:
        week_start = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
        week_end = week_start + timedelta(days=7)
        week_i1 = week_start
        week_i2 = week_end
        week_start_display = week_start.strftime("%d.%m.")
        week_end_display = week_start + timedelta(days=6)
        week_end_display = week_end_display.strftime("%d.%m.%Y")
        visible = False
    else:
        week_start = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(
            days=display_week * 7)
        week_end = week_start + timedelta(days=7)
        week_i1 = week_start
        week_i2 = week_end
        week_start_display = week_start.strftime("%d.%m.")
        week_end_display = week_start + timedelta(days=6)
        week_end_display = week_end_display.strftime("%d.%m.%Y")
        visible = True

    # Read the json files and extract the correct values:
    ####################################################################################################################
    with open('content.json', "r+") as f:
        d = json.load(f)
    f.close()
    x_list = []
    start = 0
    end = len([d][0]["content-file"])
    test_date_dt = week_i1
    for x in range(0, 7):
        test_date = test_date_dt.strftime("%d.%m.%Y")
        while start < end:
            if test_date in d["content-file"][start]:
                found_content = str(d["content-file"][start][test_date]["content"])
                x_list.append(found_content)
            start += 1
        start = 0
        test_date_dt += timedelta(days=1)

    while len(x_list) != 7:
        x_list.append(". . . . . . . . . . . ")

    return render_template("index.html", week_start_display=week_start_display, week_end_display=week_end_display,
                           return_mo=x_list[0], return_di=x_list[1], return_mi=x_list[2], return_do=x_list[3],
                           return_fr=x_list[4], return_sa=x_list[5], return_so=x_list[6], max_meals=max_meals,
                           div_meals=div_meals, most_meal=most_meal, most_meal_amount=most_meal_amount, visible=visible)


def save_info(week_key, planned_date_key, content):
    if content == "":
        return redirect("/")
    else:
        date = planned_date_key
        temp_dic = {}
        temp_dic[date] = {}
        temp_dic[date]["content"] = content
        temp_dic[date]["weekday"] = week_key
        date_updated = 0

        with open("content.json", "r+") as f:
            file_data = json.load(f)
            len_content_in_file_data = (len([file_data][0]["content-file"]))
            i = 0
            while i < len_content_in_file_data:
                if date in [file_data][0]["content-file"][i]:
                    for key, value in file_data["content-file"][i].items():
                        found_date = key
                    item_to_delete = file_data["content-file"][i][found_date]["content"]
                    [file_data][0]["content-file"][i].update(temp_dic)
                    f.seek(0)
                    json.dump(file_data, f, indent=4)
                    f.truncate()
                    # f.truncate fixes a bug, which appeared whenever an content-item was deleted,
                    # which only appeared once in the json-file. Thanks to Klaus D. from :
                    # https://stackoverflow.com/q/57408057/20071071
                    date_updated = 1
                i += 1
            f.close()

        if date_updated == 0:
            with open("content.json", "r+") as f:
                file_data["content-file"].append(temp_dic)
                f.seek(0)
                json.dump(file_data, f, indent=4)
            f.close()

        with open("meals.json", "r+") as f2:
            check_data = json.load(f2)
            if date_updated == 1:
                check_data.remove(item_to_delete)
                f2.seek(0)
                json.dump(check_data, f2)
                f2.truncate()
            check_data.append(content)
            f2.seek(0)
            json.dump(check_data, f2, indent=1)
        f2.close()
        return redirect("/")


@app.route("/save", methods=["POST", "GET"])
def save():
    # Create the necessary variables and check if the data is correct.
    # Then the data is passed on to the "save_info" function.
    ####################################################################################################################
    i = 0
    while i <= 6:
        try:
            week_key = weekday.get(str(i))
            content = request.form.get(week_key)
            planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=i)
            planned_date_key = planned_date_key + timedelta(days=display_week * 7)
            planned_date_key = planned_date_key.strftime("%d.%m.%Y")
            if content is not None:
                save_info(week_key, planned_date_key, content)
            else:
                print("Content is Null")
        except:
            print("Working on some problems...")
        i += 1
    return redirect("/")


# Adds 1 to the "display_week" variable. Which is used to determine the week to show on the index page
########################################################################################################################
@app.route("/next")
def next_week():
    global display_week
    display_week += 1
    return redirect("/")


# Subtracts 1 to the "display_week" variable. Which is used to determine the week to show on the index page
########################################################################################################################
@app.route("/prev")
def prev_week():
    global display_week
    display_week -= 1
    return redirect("/")


# Sets "display_week" back to "0". Changes the shown week back to the current week.
########################################################################################################################
@app.route("/current_week")
def current_week():
    global display_week
    display_week = 0
    return redirect("/")


# Loads about page
########################################################################################################################
@app.route("/About")
def about():
    return render_template("about.html")


# Loads contact page
########################################################################################################################
@app.route("/contact")
def contact():
    return render_template("contact.html")


# Opens stats page.
########################################################################################################################
@app.route("/stats")
def stats():
    # Loads data from both json files and prepares them to be used in this function.
    ####################################################################################################################
    with open('content.json', "r") as f, open("meals.json", "r") as f2:
        d = json.load(f)
        f.close()
        d2 = json.load(f2)
    f2.close()
    # Get Values to display the header-statistics on the stats page:
    ####################################################################################################################
    max_meals = len([d][0]["content-file"])
    div_meals = len(Counter(d2).keys())
    most_meal, most_meal_amount = Counter(d2).most_common(1)[0]
    meal_data = Counter(d2).keys()
    # Get Values to display the meals which haven't been prepared in the last 30 days.
    # By calling the "get_lost_meals" function and trying to display those. If not possible return a msg to the user.
    ####################################################################################################################
    forgotten_meals.clear()
    get_lost_meals()
    try:
        remember_items = []
        for n in range(0, 3):
            remember_items.append(forgotten_meals[n])
    except:
        remember_items = ["Du hast noch nicht genügend unterschiedliche Gerichte gekocht oder zu wenige geplant."]

    return render_template("stats.html", max_meals=max_meals, div_meals=div_meals, most_meal=most_meal,
                           most_meal_amount=most_meal_amount, meal_data=meal_data, remember_items=remember_items)


# Chooses random meals from "meals.json" and delivers them to the save-function.
########################################################################################################################
@app.route("/rng_plan")
def rng_plan():
    with open("meals.json", "r") as f:
        d = json.load(f)
    f.close()
    try:
        subset = sample(Counter(d).keys(), 7)
        # How-Two from machinelearningmastery.com/how-to-generate-random-numbers-in-python/
        i = 0
        while i <= 6:
            week_key = weekday.get(str(i))
            content = subset[i]
            planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=i)
            planned_date_key = planned_date_key + timedelta(days=display_week * 7)
            planned_date_key = planned_date_key.strftime("%d.%m.%Y")
            save_info(week_key, planned_date_key, content)
            i += 1
    except:
        print("Dataset is too small, missing or corrupted.")
    return redirect("/")


# Chooses meals which haven't been prepared in the last 30 days and delivers them to the save-function.
# Function is only possible, when there are more than 45 meals planned and when there are enough
# different meals in the past.
########################################################################################################################
@app.route("/forgot")
def forgot():
    get_lost_meals()

    try:
        i = 0
        while i <= 6:
            week_key = weekday.get(str(i))
            content = forgotten_meals[i]
            planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=i)
            planned_date_key = planned_date_key + timedelta(days=display_week * 7)
            planned_date_key = planned_date_key.strftime("%d.%m.%Y")
            save_info(week_key, planned_date_key, content)
            i += 1

    except:
        print("Error while delivering the forgotten meals to the save function.")

    return redirect("/")


# Get Values to display the meals which haven't been prepared in the last 30 days.
# Works only if there are more than 45 meals planned in the "content.json"-file
########################################################################################################################
def get_lost_meals():
    with open('content.json', "r") as f, open("meals.json", "r") as f2:
        d = json.load(f)
        f.close()
        d2 = json.load(f2)
    f2.close()

    today_plus7 = datetime.today() + timedelta(days=7)
    past = today_plus7 - timedelta(days=37)
    recently = []
    all_meals = []
    not_used = []

    for key in Counter(d2).keys():
        all_meals.append(key)

    max_len = len([d][0]["content-file"])
    if max_len >= 45:
        start = 0
        for x in range(0, 37):
            past_str = past.strftime("%d.%m.%Y")
            while start < max_len:
                if past_str in d["content-file"][start]:
                    found_past_meal = str(d["content-file"][start][past_str]["content"])
                    recently.append(found_past_meal)
                start += 1
            start = 0
            past += timedelta(days=1)

        for element in all_meals:
            if element not in recently:
                not_used.append(element)
        # Thanks to www.geeksforgeeks.org/python-difference-two-lists/

        try:
            subset = sample(not_used, 7)
            for item in subset:
                forgotten_meals.append(item)
        except:
            print("Error creating a subset with the forgotten meals. Possible cause: 'Amount of items < than 7' "
                  "Fix: Add more different meals.")

    if max_len < 45:
        print("Not enough data available.")




if __name__ == "__main__":
    app.run(debug=True)
