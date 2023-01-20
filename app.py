# Python libraries
####################################################################################################################
# general
from flask import Flask, render_template, url_for, request, redirect

# numbers and time
from datetime import datetime, timedelta
from collections import Counter

# python files
from py_files.data_handler import get_data, get_lost_meals, max_combo_weekly
from py_files.read_user_data import user_data_index
from py_files.save_process import save_info, rng_plan_task
from py_files.settings import json_check_task, clear_all, save_ignore_task, change_key_task, change_key_to_task
from py_files.graph import graph_data

# init and necessary global values
####################################################################################################################
app = Flask(__name__, static_url_path="/static")
display_week = 0  # Changes the shown week on the index page. Set to 0 at the beginning to show the current week.
display_day = 0  # Changes the shown day on the stats page. Set to 0 at the beginning to show the current day.
forgotten_meals = []  # Contains all the meals, which haven't been prepared in a while
remember_items_copy = []
weekday = {  # Is used in different functions to get easy access to the weekdays inside the lists or dict.
    "0": "mo",
    "1": "di",
    "2": "mi",
    "3": "do",
    "4": "fr",
    "5": "sa",
    "6": "so"
}
weekday_long = {  # Is used in different functions to get easy access to the weekdays inside the lists or dict.
    "0": "Montag",
    "1": "Dienstag",
    "2": "Mittwoch",
    "3": "Donnerstag",
    "4": "Freitag",
    "5": "Samstag",
    "6": "Sonntag"
}

"""
The most common used variables in this file

meals_only = []                Contains al meals as strings. With duplicates
past_meals_only = []           Contains al meals as strings which are in the past. Without duplicates.
meals_lst_as_int = []          Contains all meals, sorted by date and stored as an integer.
days_lst_as_int = []           Contains all weekdays, sorted by date and stored as an integer.
weekly_meals = []              Contains all meals, from a calendar week saved as a string but without dates.
monthly_meals = []             Contains all meals, from a month saved as a string.
seasonal_meals = []            Contains all meals, from a season saved as a string.
not_in_last_two_weeks = []     Contains all meals, which haven't been prepared in the last two weeks.
max_meals = 0                  Contains all meals planned. One per day. As integer.
div_meals = 0                  Contains all different meals without duplicates. As integer.
most_meal, most_meal_amount = 0, 0  Contains the meal which have been eaten  the most and the amount
meals_only_without_duplicates = []  Contains all meals as string without duplicates.
"""


@app.route("/")
def index():
    """
    Calls the user_data_index() with the current value in display_week and
    afterwards returns the index.html to the user.
    """

    display_data = user_data_index(display_week)
    return render_template(
        "index.html",
        week_start_display=display_data["week_start_display"],
        week_end_display=display_data["week_end_display"],
        return_mo=display_data["return_mo"],
        return_di=display_data["return_di"],
        return_mi=display_data["return_mi"],
        return_do=display_data["return_do"],
        return_fr=display_data["return_fr"],
        return_sa=display_data["return_sa"],
        return_so=display_data["return_so"],
        max_meals=display_data["max_meals"],
        div_meals=display_data["div_meals"],
        most_meal=display_data["most_meal"],
        most_meal_amount=display_data["most_meal_amount"],
        visible=display_data["visible"])


@app.route("/save", methods=["POST", "GET"])
def save():
    """
    Create the necessary variables and check if the data is correct.
    Then the data is passed on to the "save_info" function.
    """
    for i in range(0, 7):
        week_key = weekday.get(str(i))
        content = request.form.get(week_key)
        planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=i)
        planned_date_key = planned_date_key + timedelta(days=display_week * 7)
        planned_date_key = planned_date_key.strftime("%d.%m.%Y")
        save_info(planned_date_key, content)
    return redirect("/")


@app.route("/next")
def next_week():
    """
    Adds 1 to the "display_week" variable. Which is used to determine the week to show on the index page
    """
    global display_week
    display_week += 1
    return redirect("/")


@app.route("/prev")
def prev_week():
    """
    Subtracts 1 to the "display_week" variable. Which is used to determine the week to show on the index page
    """
    global display_week
    display_week -= 1
    return redirect("/")


@app.route("/current_week")
def current_week():
    """
    Sets "display_week" back to "0". Changes the shown week back to the current week.
    """
    global display_week
    display_week = 0
    return redirect("/")


@app.route("/stats")
def stats():
    """
    Calls get_data(), get_lost_meals, max_combo_weekly and graph_data().
    Afterwards tries to return those values to the user by returning stats.html
    """
    data_set = get_data()
    max_meals = data_set["max_meals"]
    div_meals = data_set["div_meals"]
    most_meal = data_set["most_meal"]
    most_meal_amount = data_set["most_meal_amount"]
    meals_only = data_set["meals_only"]

    visible_l = False  # Definiert ob Navigation-Buttons auf der Stats-Page angezeigt werden sollen. True=Yes
    visible_r = False  # Definiert ob Navigation-Buttons auf der Stats-Page angezeigt werden sollen. True=Yes
    meal_data = sorted(Counter(meals_only).keys())  # Used to return the values to a table inside the html file.
    max_lst = []  # Contains the most frequent meals and weekdays combinations.

    # Get Values to display the meals which haven't been prepared in the last 30 days.
    # By calling the "get_lost_meals" function and trying to display those. If not possible return a msg to the user.
    ####################################################################################################################
    global remember_items_copy
    remember_items = []

    if display_day == 0:
        forgotten_meals = get_lost_meals()
        if len(forgotten_meals) > 3:
            for n in range(0, 3):
                remember_items.append(forgotten_meals[n])
        else:
            remember_items = ["Du hast noch nicht genügend unterschiedliche Gerichte gekocht oder zu wenige geplant."]
        remember_items_copy = remember_items

    elif display_day != 0:
        if len(remember_items_copy) == 3:
            for n in range(0, 3):
                remember_items.append(remember_items_copy[n])
        else:
            remember_items = ["Du hast noch nicht genügend unterschiedliche Gerichte gekocht oder zu wenige geplant."]

    max_lst = max_combo_weekly()

    try:
        day_c = weekday_long.get(str(display_day))
        meal_c = max_lst[display_day][1]
        if max_lst[display_day][3] > 6:
            quote_c = "Es scheint einen starken Zusammenhang zu geben."
        elif max_lst[display_day][3] > 4:
            quote_c = "Es scheint einen Zusammenhang zu geben."
        elif max_lst[display_day][3] > 2:
            quote_c = "Es scheint einen schwachen Zusammenhang zu geben."
        else:
            quote_c = "Dies scheint mir aber ein Zufall zu sein."
        if display_day > 0:
            visible_l = True
        if display_day < 6:
            visible_r = True

    except:
        day_c = "Es kann noch keine Analyse gemacht werden. Mehr unterschiedliche Daten sollten hinzugefügt werden."
        meal_c, quote_c = "", ""
        visible_l, visible_r = False, False

    # Tries to create values for the graph on the stats-page, by calling the "graph_data"-function.
    # Returns "graph_visible = False" if not possible.
    ####################################################################################################################

    try:
        top15, not15 = graph_data()
        graph_visible = True
    except:
        graph_visible = False
        top15 = []
        not15 = []

    return render_template(
        "stats.html",
        max_meals=max_meals,
        div_meals=div_meals,
        most_meal=most_meal,
        most_meal_amount=most_meal_amount,
        meal_data=meal_data,
        remember_items=remember_items,
        day_c=day_c,
        meal_c=meal_c,
        quote_c=quote_c,
        visible_l=visible_l,
        visible_r=visible_r,
        top15=top15,
        not15=not15,
        graph_visible=graph_visible)


@app.route("/rng_plan")
def rng_plan():
    """
    Chooses 7 random meals from "content.json" and delivers them to the save-function.
    """
    rng_plan_task(display_week)
    return redirect("/")


@app.route("/forgot")
def forgot():
    """
    Chooses meals which haven't been prepared in the last 30 days and delivers them to the save-function.
    Function is only possible, when there are more than 45 meals planned and when there are enough
    different meals in the past.
    """
    forgotten_meals = get_lost_meals()
    try:
        for i in range(0, 7):
            content = forgotten_meals[i]
            planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=i)
            planned_date_key = planned_date_key + timedelta(days=display_week * 7)
            planned_date_key = planned_date_key.strftime("%d.%m.%Y")
            save_info(planned_date_key, content)
            i += 1
    except:
        print("Func: forgot() - Error while delivering the forgotten meals to the save function.")
    return redirect("/")


@app.route("/prev_combo")
def prev_day():
    """
    Subtracts 1 to the "display_day" variable. Which is used to determine the day shown on the stats page.
    """
    global display_day
    if display_day != 0:
        display_day -= 1
    return redirect("/stats")


@app.route("/next_combo")
def next_day():
    """
    Adds 1 to the "display_day" variable. Which is used to determine the day shown on the stats page.
    """
    global display_day
    if display_day != 6:
        display_day += 1
    return redirect("/stats")


@app.route("/profil")
def profil():
    """
    Returns profil.html and saves the default placeholder.
    """
    key_to_change = "Chips"         # Saves placeholder text for the forms.
    key_to_change_to = "Pommes"     # Saves placeholder text for the forms.
    return render_template("profil.html", key_to_change=key_to_change, key_to_change_to=key_to_change_to)


@app.route("/save_ignore", methods=["POST", "GET"])
def save_ignore():
    """
    Saves values which should be ignored from the settings page into the settings.json file
    """
    save_ignore_task()
    return redirect("/profil")


@app.route("/refresh_f_meals")
def refresh_f_meals():
    """
    Reloads the stats page and displays new meal which haven't been prepared in a while. If the current display week
    isn't = 0, then saves the values in a global variable. Because it shouldn't  reload all the data
    on every page refresh.
    """
    global remember_items_copy
    forgotten_meals = get_lost_meals()
    if display_day != 0:
        if len(forgotten_meals) >= 3:
            remember_items_copy = []
            for n in range(0, 3):
                remember_items_copy.append(forgotten_meals[n])
    return redirect("/stats")


@app.route("/data_reset")
def data_reset():
    """
    Resets content.json and settings.json by calling clear_all()
    """
    clear_all()
    return render_template("profil.html")


@app.route("/change_key", methods=["POST", "GET"])
def change_key():
    """
    Saves values which should be replaced in the settings.json
    """
    key_to_change = change_key_task()
    return render_template("profil.html", key_to_change=key_to_change)


@app.route("/change_key_to", methods=["POST", "GET"])
def change_key_to():
    """
    Gets the value which should replace the value from change_key() and changes this value in the "content.json" file.
    """
    key_to_change, key_to_change_to = change_key_to_task()
    return render_template("profil.html", key_to_change=key_to_change, key_to_change_to=key_to_change_to)


if __name__ == "__main__":
    # Checks if the json files are present by calling the "json_check" function with the filenames from the dict.
    json_check_task()
    app.run(debug=True, port=5001)
