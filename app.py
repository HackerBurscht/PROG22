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
display_week = 0        # Changes the shown week on the index page. Set to 0 at the beginning to show the current week.
forgotten_meals = []    # Contains all the meals, which haven't been prepared in a while
weekday = {             # Is used in different functions to get easy access to the weekdays inside the lists or dict.
    "0": "mo",
    "1": "di",
    "2": "mi",
    "3": "do",
    "4": "fr",
    "5": "sa",
    "6": "so"
}

# The most common used variables in this file
########################################################################################################################
# meals_only = []                Contains al meals as strings. With duplicates
# meals_lst_as_int = []          Contains all meals, sorted by date and stored as an integer.
# days_lst_as_int = []           Contains all weekdays, sorted by date and stored as an integer.
# weekly_meals = []              Contains all meals, from a calendar week saved as a string but without dates.
# monthly_meals = []             Contains all meals, from a month saved as a string.
# seasonal_meals = []            Contains all meals, from a season saved as a string.
# not_in_last_two_weeks = []     Contains all meals, which haven't been prepared in the last two weeks.
# max_meals = 0                  Contains all meals planned. One per day. As integer.
#                                Used mostly to measure the length of the json.
# div_meals = 0                  Contains all different meals without duplicates. As integer.
# most_meal, most_meal_amount = 0, 0  Contains the meal which have been eaten  the most and the amount
# meals_only_without_duplicates = []  Contains alls meals as string without duplicates.

# user commands
########################################################################################################################
# The following commands  can be used in the web app. They just have to be entered as "meals" on the planning page.
# "r" :   changes the day to a random meal
# "f" :   changes the day to a forgotten meal
# "-" :   keeps the day unplanned.


def get_data():
    # Get the data for
    ####################################################################################################################
    with open('content.json', "r") as f:
        d = json.load(f)
    f.close()

    meals_only = []                             # Contains al meals as strings. With duplicates
    range_end = len([d][0]["content-file"])     # Gets the length of the json file

    for i in range(0, range_end):
        temp_lst = []
        for key, value in d["content-file"][i].items():
            n_con = d["content-file"][i][key]["content"]
            temp_lst.append(n_con)
            meals_only.append(n_con)

    meals_only = [value for value in meals_only if value != "-"]
    # removes the placeholder "-", as mentioned under "user commands"
    # https://www.delftstack.com/howto/python/python-list-remove-all/

    max_meals = len([d][0]["content-file"])
    div_meals = len(Counter(meals_only).keys())
    most_meal, most_meal_amount = Counter(meals_only).most_common(1)[0]
    # Counter inspired by https://datagy.io/python-count-unique-values-list/
    # most_common()-How-To from https://www.delftstack.com/howto/python/python-counter-most-common/
    # delivers a tuple inside a dict
    meals_only_without_duplicates = [*set(meals_only)]
    # It first removes the duplicates and returns a dictionary which has to be converted to list
    # From www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/

    return max_meals, div_meals, most_meal, most_meal_amount, meals_only, d, meals_only_without_duplicates


@app.route("/", methods=["POST", "GET"])
def index():
    max_meals, div_meals, most_meal, most_meal_amount, meals_only, d, meals_only_without_duplicates = get_data()
    #https://www.geeksforgeeks.org/python-return-statement/

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
    week_i1 = week_start

    # Read the json files and extract the correct values:
    ####################################################################################################################
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
    if content is not None:
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
                    [file_data][0]["content-file"][i].update(temp_dic)
                    f.seek(0)
                    json.dump(file_data, f, indent=4)
                    f.truncate()
                    # f.truncate fixes a bug, which appeared whenever a content-item was deleted,
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

    return redirect("/")


@app.route("/save", methods=["POST", "GET"])
def save():
    # Create the necessary variables and check if the data is correct.
    # Then the data is passed on to the "save_info" function.
    ####################################################################################################################
    for i in range(0, 7):
        try:
            week_key = weekday.get(str(i))
            content = request.form.get(week_key)
            planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=i)
            planned_date_key = planned_date_key + timedelta(days=display_week * 7)
            planned_date_key = planned_date_key.strftime("%d.%m.%Y")
            save_info(week_key, planned_date_key, content)
            print(week_key)
        except:
            print("Func: save() - Error")
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
    max_meals, div_meals, most_meal, most_meal_amount, meals_only, d, meals_only_without_duplicates = get_data()

    meal_data = sorted(Counter(meals_only).keys())  # Used to return the values to a table inside the html file.

    # Get Values to display the meals which haven't been prepared in the last 30 days.
    # By calling the "get_lost_meals" function and trying to display those. If not possible return a msg to the user.
    ####################################################################################################################
    forgotten_meals.clear()     # Clears the list and creates a new one. In case some forgotten meals have been planned.
    get_lost_meals()
    try:
        remember_items = []
        for n in range(0, 3):
            remember_items.append(forgotten_meals[n])
    except:
        remember_items = ["Du hast noch nicht genügend unterschiedliche Gerichte gekocht oder zu wenige geplant."]

    #affinity_analysis()

    return render_template("stats.html", max_meals=max_meals, div_meals=div_meals, most_meal=most_meal,
                           most_meal_amount=most_meal_amount, meal_data=meal_data, remember_items=remember_items)


# Chooses 7 random meals from "content.json" and delivers them to the save-function.
########################################################################################################################
@app.route("/rng_plan")
def rng_plan():
    max_meals, div_meals, most_meal, most_meal_amount, meals_only, d, meals_only_without_duplicates = get_data()

    try:
        subset = sample(Counter(meals_only).keys(), 7)
        # How-Two from machinelearningmastery.com/how-to-generate-random-numbers-in-python/
        for i in range(0, 7):
            week_key = weekday.get(str(i))
            content = subset[i]
            planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=i)
            planned_date_key = planned_date_key + timedelta(days=display_week * 7)
            planned_date_key = planned_date_key.strftime("%d.%m.%Y")
            save_info(week_key, planned_date_key, content)
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


# Get Values to display the meals which haven't been prepared in the last 30 days.
# Works only if there are more than 45 meals planned in the "content.json"-file
########################################################################################################################
def get_lost_meals():
    max_meals, div_meals, most_meal, most_meal_amount, meals_only, d, meals_only_without_duplicates = get_data()

    forgotten_meals.clear()     # Clears the list and creates a new one. In case some forgotten meals have been planned.
    today_plus7 = datetime.today() + timedelta(days=7)
    past = today_plus7 - timedelta(days=37)
    recently = []
    not_used = []

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

        for element in meals_only:
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


def affinity_analysis():
    # Step 1:
    # Get all meals and related weekdays and save that info as a list inside a list.
    # And creates a new list containing only the different meals without duplicates.
    ####################################################################################################################
    with open('content.json', "r") as f:
        dirty_data = json.load(f)
        f.close()

    clean_data = []

    start = 0
    end = len([dirty_data][0]["content-file"])
    while start < end:
        temp_lst = []
        for key, value in dirty_data["content-file"][start].items():
            n_con = dirty_data["content-file"][start][key]["content"]
            n_day = dirty_data["content-file"][start][key]["weekday"]
            temp_lst.append(n_con)
            temp_lst.append(n_day)
            clean_data.append(temp_lst)

        start += 1

    # Step 1-1:
    # Prepare more data to carry out further possible analyses and identify patterns.
    ####################################################################################################################
    meals_lst_as_int = []  # Contains all meals, sorted by date and stored as an integer.
    days_lst_as_int = []  # Contains all weekdays, sorted by date and stored as an integer.
    weekly_meals = []  # Contains all meals, from a calendar week saved as a string.
    monthly_meals = []  # Contains all meals, from a month saved as a string.
    seasonal_meals = []  # Contains all meals, from a season saved as a string.
    not_in_last_two_weeks = []  # Contains all meals, which havent been prepared in the last two weeks.

    # meals and weekdays to integer
    ####################################################################################################################
    start = 0
    while start < end:
        temp_lst = []
        for key, value in dirty_data["content-file"][start].items():
            n_con = dirty_data["content-file"][start][key]["content"]
            n_day = dirty_data["content-file"][start][key]["weekday"]
            temp_lst.append(n_con)
            temp_lst.append(n_day)
            meals_lst_as_int.append(n_con)
            days_lst_as_int.append(n_day)
        start += 1

    temp_meals = meals_lst_as_int
    temp_meals_set = list(set(temp_meals))
    temp_days = days_lst_as_int
    temp_days_set = list(set(temp_days))

    meals_lst_as_int = [temp_meals_set.index(x) + 1 for x in temp_meals]
    days_lst_as_int = [temp_days_set.index(x) + 1 for x in temp_days]

    print("Mahlzeiten als Int: ", meals_lst_as_int)
    print("Wochentage als Int: ", days_lst_as_int)
    print(len(days_lst_as_int))
    print(len(meals_lst_as_int))

    # weekly meals without date
    ####################################################################################################################
    start = 0
    temp_lst_2 = []
    while start < end:
        temp_lst = []
        for key, value in dirty_data["content-file"][start].items():
            n_con = dirty_data["content-file"][start][key]["content"]
            n_day = dirty_data["content-file"][start][key]["weekday"]
            temp_lst.append(n_con)
            temp_lst.append(n_day)
            temp_lst_2.append(n_con)
        start += 1

    weekly_meals.append([temp_lst_2[x:x + 7] for x in range(0, len(temp_lst_2), 7)])
    # From stackoverflow.com/questions/15890743/how-can-you-split-a-list-every-x-elements-and-add-those-x-amount-of-elements-to

    print("Weekly meals: ", weekly_meals)

    # Step 2:
    # Calculate the total amount of each meal, weekday, and meal/weekday-combination.
    ####################################################################################################################

    # Test example
    x = "Fisch"
    y = "mo"

    sum_x = sum([x in i for i in clean_data])  # Sum of x in clean_data
    sum_y = sum([y in i for i in clean_data])  # Sum of y in clean_data
    sum_xy = sum([all(z in i for z in [x, y]) for i in clean_data])  # Sum of the x and y combination
    sum_clean_data = len(clean_data)  # Sum of all entries in the clean_data list

    print("Gesamtmenge von Items in clean_data: ", sum_clean_data)
    print(sum_x, "mal", x)
    print(sum_y, "mal", y)
    print("Kombi von", x, "und", y, ": ", sum_xy)

    support = sum_xy / sum_clean_data
    confidence = support / (sum_x / sum_clean_data)
    lift = confidence / (sum_y / sum_clean_data)
    if confidence == 1:
        conviction = 0
    else:
        conviction = (1 - (sum_y / len(clean_data))) / (1 - confidence)

    print("Support = {}".format(round(support, 2)))
    print("Confidence = {}".format(round(confidence, 2)))
    print("Lift= {}".format(round(lift, 2)))
    print("Conviction={}".format(round(conviction, 2)))

    max_lst = []
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
        print(y, "häufigste Kombi mit:", max_kombi_meal, "erscheint: ", max_kombi, "mal")
        print("S= ", round(max_kombi / sum_clean_data, 2))
        print("C= ", round((max_kombi / sum_clean_data) / (n / sum_clean_data), 3))
        print("L= ", round((max_kombi / sum_clean_data) / (n / sum_clean_data) / (m / sum_clean_data), 3))

        temp = [y]
        temp.append(max_kombi_meal)
        temp.append(max_kombi)
        max_lst.append(temp)
    print(max_lst)

    print()
    print("why?")
    max_lst = []
    for i in range(7):
        y = weekday.get(str(i))
        for j in range(len(meals_only)):
            temp = []
            x = meals_only[j]
            max_kombi = sum([all(z in i for z in [x, y]) for i in clean_data])
            n = sum([x in a for a in clean_data])  # n equals the amount of x. eg: 17 times "pasta"
            m = sum([y in a for a in clean_data])  # m equals the amount of y. eg: 4 times "Monday"
            l = round((max_kombi / sum_clean_data) / (n / sum_clean_data) / (m / sum_clean_data), 3)
            if l > 1:
                temp.append(x)
                temp.append(y)
                temp.append(l)
                max_lst.append(temp)
    print(max_lst)

if __name__ == "__main__":
    app.run(debug=True)
