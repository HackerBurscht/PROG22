# Python libraries
####################################################################################################################
# general
from flask import Flask, render_template, url_for, request, redirect
import json

# numbers and time
from datetime import datetime, timedelta
from collections import Counter
from random import sample

# python files
from data_management.data_handler import get_data, get_lost_meals, save_info, rng_plan_task
from data_management.settings import json_check_task, clear_all, save_ignore_task, change_key_task, change_key_to_task
from data_management.graph import graph_data

# init and necessary global values
####################################################################################################################
app = Flask(__name__, static_url_path="/static")
display_week = 0  # Changes the shown week on the index page. Set to 0 at the beginning to show the current week.
display_day = 0  # Changes the shown day on the stats page. Set to 0 at the beginning to show the current day.
forgotten_meals = []  # Contains all the meals, which haven't been prepared in a while
max_lst = []  # Contains the most frequent meals and weekdays combinations.
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


# The most common used variables in this file
########################################################################################################################
# meals_only = []                Contains al meals as strings. With duplicates
# past_meals_only = []           Contains al meals as strings which are in the past. Without duplicates.
# meals_lst_as_int = []          Contains all meals, sorted by date and stored as an integer.
# days_lst_as_int = []           Contains all weekdays, sorted by date and stored as an integer.
# weekly_meals = []              Contains all meals, from a calendar week saved as a string but without dates.
# monthly_meals = []             Contains all meals, from a month saved as a string.
# seasonal_meals = []            Contains all meals, from a season saved as a string.
# not_in_last_two_weeks = []     Contains all meals, which haven't been prepared in the last two weeks.
# max_meals = 0                  Contains all meals planned. One per day. As integer.
# div_meals = 0                  Contains all different meals without duplicates. As integer.
# most_meal, most_meal_amount = 0, 0  Contains the meal which have been eaten  the most and the amount
# meals_only_without_duplicates = []  Contains all meals as string without duplicates.


@app.route("/", methods=["POST", "GET"])
def index():
    data_set = get_data()
    max_meals = data_set["max_meals"]
    div_meals = data_set["div_meals"]
    most_meal = data_set["most_meal"]
    most_meal_amount = data_set["most_meal_amount"]
    d = data_set["d"]

    # Set the current or selected week and create values to return on the index page:
    ####################################################################################################################
    week_start = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
    visible = False
    if display_week != 0:
        week_start = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(
            days=display_week * 7)
        visible = True
    week_start_display = week_start.strftime("%d.%m.")
    week_end_display = week_start + timedelta(days=6)
    week_end_display = week_end_display.strftime("%d.%m.%Y")

    # Create necessary variables for this function.
    ####################################################################################################################
    end = len([d][0]["content-file"])  # Used to determine the lenght of "d" and as a value for the "range"-function.
    meal_and_date = []  # Contains all the meals and date combos from "d".
    test_date_dt = week_start  # Is used to loop trhough all the dates in "d"

    # Loops through all the items in "d". Looks for values which are the same as the desired weekday.
    # Saves the meal from "d":
    # If the meal is equal to "-" or the date is missing, saves returns a placeholder.
    for x in range(0, 7):
        temp_lst = []
        test_date = test_date_dt.strftime("%d.%m.%Y")
        for i in range(0, end):
            for key, value in d["content-file"][i].items():
                n_con = str(d["content-file"][i][key]["content"])
                if test_date == key:
                    if n_con == "-":
                        n_con = ". . . . . . . . . . . "
                    temp_lst.append(n_con)
        meal_and_date.append(temp_lst)
        test_date_dt += timedelta(days=1)

    # Checks if there are 7 lists in the list. If an index is missing, a new list with a placeholder is inserted.
    for i in range(0, 7):
        if not meal_and_date[i]:
            meal_and_date[i] = [". . . . . . . . . . . "]

    # Flattens the list and returns it as an unnested list.
    clean_lst = []
    for sublist in meal_and_date:
        for meal in sublist:
            clean_lst.append(meal)

    return render_template("index.html", week_start_display=week_start_display, week_end_display=week_end_display,
                           return_mo=clean_lst[0], return_di=clean_lst[1], return_mi=clean_lst[2],
                           return_do=clean_lst[3],
                           return_fr=clean_lst[4], return_sa=clean_lst[5], return_so=clean_lst[6], max_meals=max_meals,
                           div_meals=div_meals, most_meal=most_meal, most_meal_amount=most_meal_amount, visible=visible)


@app.route("/save", methods=["POST", "GET"])
def save():
    # Create the necessary variables and check if the data is correct.
    # Then the data is passed on to the "save_info" function.
    ####################################################################################################################
    for i in range(0, 7):
        week_key = weekday.get(str(i))
        content = request.form.get(week_key)
        planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=i)
        planned_date_key = planned_date_key + timedelta(days=display_week * 7)
        planned_date_key = planned_date_key.strftime("%d.%m.%Y")
        save_info(week_key, planned_date_key, content)
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


# Opens stats page.
########################################################################################################################
@app.route("/stats")
def stats():
    data_set = get_data()
    max_meals = data_set["max_meals"]
    div_meals = data_set["div_meals"]
    most_meal = data_set["most_meal"]
    most_meal_amount = data_set["most_meal_amount"]
    meals_only = data_set["meals_only"]

    visible_l = False  # Definiert ob Navigation-Buttons auf der Stats-Page angezeigt werden sollen. True=Yes
    visible_r = False  # Definiert ob Navigation-Buttons auf der Stats-Page angezeigt werden sollen. True=Yes
    meal_data = sorted(Counter(meals_only).keys())  # Used to return the values to a table inside the html file.

    # Get Values to display the meals which haven't been prepared in the last 30 days.
    # By calling the "get_lost_meals" function and trying to display those. If not possible return a msg to the user.
    ####################################################################################################################

    try:
        forgotten_meals = get_lost_meals()
        remember_items = []
        for n in range(0, 3):
            remember_items.append(forgotten_meals[n])
    except:
        remember_items = ["Du hast noch nicht genügend unterschiedliche Gerichte gekocht oder zu wenige geplant."]

    # Get Values to display the meals which haven't been prepared in the last 30 days.
    # By calling the "get_lost_meals" function and trying to display those. If not possible return a msg to the user.
    ####################################################################################################################
    if not max_lst:
        max_combo_weekly()

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

    return render_template("stats.html", max_meals=max_meals, div_meals=div_meals, most_meal=most_meal,
                           most_meal_amount=most_meal_amount, meal_data=meal_data, remember_items=remember_items,
                           day_c=day_c, meal_c=meal_c, quote_c=quote_c, visible_l=visible_l, visible_r=visible_r,
                           top15=top15, not15=not15, graph_visible=graph_visible)


# Chooses 7 random meals from "content.json" and delivers them to the save-function.
########################################################################################################################
@app.route("/rng_plan")
def rng_plan():
    rng_plan_task(display_week)
    return redirect("/")


# Chooses meals which haven't been prepared in the last 30 days and delivers them to the save-function.
# Function is only possible, when there are more than 45 meals planned and when there are enough
# different meals in the past.
########################################################################################################################
@app.route("/forgot")
def forgot():
    forgotten_meals = get_lost_meals()
    try:
        for i in range(0, 7):
            week_key = weekday.get(str(i))
            content = forgotten_meals[i]
            planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=i)
            planned_date_key = planned_date_key + timedelta(days=display_week * 7)
            planned_date_key = planned_date_key.strftime("%d.%m.%Y")
            save_info(week_key, planned_date_key, content)
            i += 1
    except:
        print("Func: forgot() - Error while delivering the forgotten meals to the save function.")
    return redirect("/")


# Creates the necessary values, which are used to display the day-statistics on the stas-page.
########################################################################################################################
def max_combo_weekly():
    data_set = get_data()
    meals_only = data_set["meals_only"]
    d = data_set["d"]

    if len(meals_only) >= 7:
        clean_data = []  # Empty list. Used to store values inside the function.
        end = len([d][0]["content-file"])  # Determines the length of "d" and used for the "range"-function.

        # The meal and weekday values from "d" get saved inside "clean_data" as lists.
        for i in range(0, end):
            temp_lst_2 = []
            for key, value in d["content-file"][i].items():
                n_con = d["content-file"][i][key]["content"]
                n_day = d["content-file"][i][key]["weekday"]
                temp_lst_2.append(n_con)
                temp_lst_2.append(n_day)
                clean_data.append(temp_lst_2)

        sum_clean_data = len(clean_data)  # Sum of all entries in the clean_data list

        # Checks which meal is most often prepared on each weekday. Uses "meals_only".
        # -> Checks which "weekday"-"content"-combos occurs most often.
        for i in range(7):
            max_kombi = 0
            max_kombi_meal = ""
            y = weekday.get(str(i))
            for j in range(len(meals_only)):
                x = meals_only[j]
                test_sum = sum([all(z in i for z in [x, y]) for i in clean_data])
                if test_sum > max_kombi:
                    max_kombi = test_sum
                    max_kombi_meal = x
                    n = sum([x in a for a in clean_data])  # n equals the amount of x. eg: 17 times "pasta"
                    m = sum([y in a for a in clean_data])  # m equals the amount of y. eg: 4 times "Monday"
            # Calculates the lift for the most frequent combinations.
            meal_lift = round((max_kombi / sum_clean_data) / (n / sum_clean_data) / (m / sum_clean_data), 3)

            # Saves the amount of the meal, the most prepared meal, the amount of the combination appearing and the lift
            # as a list inside the "max_lst" list.
            temp = [y, max_kombi_meal, max_kombi, meal_lift]
            max_lst.append(temp)


# Subtracts 1 to the "display_day" variable. Which is used to determine the day shown on the stats page.
########################################################################################################################
@app.route("/prev_combo")
def prev_day():
    global display_day
    if display_day != 0:
        display_day -= 1
    return redirect("/stats")


# Adds 1 to the "display_day" variable. Which is used to determine the day shown on the stats page.
########################################################################################################################
@app.route("/next_combo")
def next_day():
    global display_day
    if display_day != 6:
        display_day += 1
    return redirect("/stats")


# Loads about page
########################################################################################################################
@app.route("/About")
def about():
    return render_template("about.html")


# Loads profil page
########################################################################################################################
@app.route("/profil")
def profil():
    # Saves placeholder text for the forms.
    key_to_change = "Chips"
    key_to_change_to = "Pommes"
    return render_template("profil.html", key_to_change=key_to_change, key_to_change_to=key_to_change_to)


# Saves values which should be ignored from the settings page into the settings.json file
########################################################################################################################
@app.route("/save_ignore", methods=["POST", "GET"])
def save_ignore():
    save_ignore_task()
    return redirect("/profil")


# Reloads the stats page and displays new meal which haven't been prepared in a while.
########################################################################################################################
@app.route("/refresh_f_meals")
def refresh_f_meals():
    forgotten_meals = get_lost_meals()
    max_combo_weekly()
    return redirect("/stats")


# Resets content.json and settings.json
########################################################################################################################
@app.route("/data_reset")
def data_reset():
    clear_all()
    return render_template("profil.html")


# Saves values which should be replaced in the settings.json
########################################################################################################################
@app.route("/change_key", methods=["POST", "GET"])
def change_key():
    key_to_change = change_key_task()
    return render_template("profil.html", key_to_change=key_to_change)


# Gets the value which should replace the value from change_key() and changes this value in the "content.json" file.
########################################################################################################################
@app.route("/change_key_to", methods=["POST", "GET"])
def change_key_to():
    key_to_change, key_to_change_to = change_key_to_task()
    return render_template("profil.html", key_to_change=key_to_change, key_to_change_to=key_to_change_to)


# def affinity_analysis():
#     max_meals, div_meals, most_meal, most_meal_amount, meals_only, d, meals_only_without_duplicates = get_data()
#
#     # Step 1-1:
#     # Prepare more data to carry out further possible analyses and identify patterns.
#     ####################################################################################################################
#     clean_data = []
#     meals_lst_as_int = []  # Contains all meals, sorted by date and stored as an integer.
#     days_lst_as_int = []  # Contains all weekdays, sorted by date and stored as an integer.
#     weekly_meals = []  # Contains all meals, from a calendar week saved as a string.
#     monthly_meals = []  # Contains all meals, from a month saved as a string.
#     seasonal_meals = []  # Contains all meals, from a season saved as a string.
#     not_in_last_two_weeks = []  # Contains all meals, which haven't been prepared in the last two weeks.
#
#     # Gets multiple values which are need for further analysis
#     # meals and weekdays to integer, weekly meals without date, clean_data
#     ####################################################################################################################
#     end = len([d][0]["content-file"])
#     temp_lst = []
#     for i in range(0, end):
#         for key, value in d["content-file"][i].items():
#             n_con = d["content-file"][i][key]["content"]
#             n_day = d["content-file"][i][key]["weekday"]
#             meals_lst_as_int.append(n_con)
#             days_lst_as_int.append(n_day)
#             temp_lst.append(n_con)
#
#     temp_meals = meals_lst_as_int
#     temp_meals_set = list(set(temp_meals))
#     temp_days = days_lst_as_int
#     temp_days_set = list(set(temp_days))
#
#     meals_lst_as_int = [temp_meals_set.index(x) + 1 for x in temp_meals]
#     days_lst_as_int = [temp_days_set.index(x) + 1 for x in temp_days]
#
#     weekly_meals.append([temp_lst[x:x + 7] for x in range(0, len(temp_lst), 7)])
#     # From stackoverflow.com/questions/15890743/how-can-you-split-a-list-every-x-elements-and-add-those-x-amount-of-elements-to
#
#     print("Mahlzeiten als Int: ", meals_lst_as_int)
#     print("Wochentage als Int: ", days_lst_as_int)
#     print("Anzahl Tage: ", len(days_lst_as_int))
#     print("Anzahl Meals: ", len(meals_lst_as_int))
#     print("Weekly meals: ", weekly_meals)

# Step 2:
# Calculate the total amount of each meal, weekday, and meal/weekday-combination.
####################################################################################################################

# Test example
# x = "Spaghetti"
# y = "mo"

# sum_x = sum([x in i for i in clean_data])  # Sum of x in clean_data
# sum_y = sum([y in i for i in clean_data])  # Sum of y in clean_data
# sum_xy = sum([all(z in i for z in [x, y]) for i in clean_data])  # Sum of the x and y combination
# sum_clean_data = len(clean_data)  # Sum of all entries in the clean_data list

# support = sum_xy / sum_clean_data
# confidence = support / (sum_x / sum_clean_data)
# lift = confidence / (sum_y / sum_clean_data)
# if confidence == 1:
#     conviction = 0
# else:
#     conviction = (1 - (sum_y / len(d))) / (1 - confidence)
# print("###############################################################################################")
# print("Testergebnisse:")
# print("Gesamtmenge von Items in clean_data: ", sum_clean_data)
# print(sum_x, "mal", x)
# print(sum_y, "mal", y)
# print("Kombi von", x, "und", y, ": ", sum_xy)
# print("Support = {}".format(round(support, 2)))
# print("Confidence = {}".format(round(confidence, 2)))
# print("Lift= {}".format(round(lift, 2)))
# print("Conviction={}".format(round(conviction, 2)))
# print("###############################################################################################")

# print()
# print("why?")
# max_lst = []
# for i in range(7):
#     y = weekday.get(str(i))
#     for j in range(len(meals_only)):
#         temp = []
#         x = meals_only[j]
#         max_kombi = sum([all(z in i for z in [x, y]) for i in clean_data])
#         n = sum([x in a for a in clean_data])  # n equals the amount of x. eg: 17 times "pasta"
#         m = sum([y in a for a in clean_data])  # m equals the amount of y. eg: 4 times "Monday"
#         l = round((max_kombi / sum_clean_data) / (n / sum_clean_data) / (m / sum_clean_data), 3)
#         if l > 1:
#             temp.append(x)
#             temp.append(y)
#             temp.append(l)
#             max_lst.append(temp)
# print(max_lst)

if __name__ == "__main__":
    # Checks if the json files are present by calling the "json_check" function with the filenames from the dict.
    json_check_task()
    app.run(debug=True)
