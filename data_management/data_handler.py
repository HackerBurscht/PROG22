# Python libraries
####################################################################################################################
# general
from flask import Flask, render_template, url_for, request, redirect
import json
import os

# numbers and time
from datetime import datetime, timedelta
from collections import Counter
from random import sample

weekday = {  # Is used in different functions to get easy access to the weekdays inside the lists or dict.
    "0": "mo",
    "1": "di",
    "2": "mi",
    "3": "do",
    "4": "fr",
    "5": "sa",
    "6": "so"
}

# Get the data from the json-files and prepares it to be used in other functions.
########################################################################################################################
def get_data():
    data_set = {
        "max_meals": "0",
        "div_meals": "0",
        "most_meal": "none",
        "most_meal_amount": "0",
        "meals_only": "none",
        "meals_only_without_duplicates": "none",
        "d": "empty",
    }

    # Loads data from setting.json
    with open("json_files/settings.json", "r") as s:
        settings = json.load(s)
    ignore_keys = [settings][0]["settings"]["ignore"]
    key_amount = len([settings][0]["settings"]["ignore"])

    # Get the data from the content.json
    ####################################################################################################################
    with open("json_files/content.json", "r") as f:
        d = json.load(f)

    meals_only = []  # Contains al meals as strings. With duplicates
    range_end = len([d][0]["content-file"])  # Gets the length of the json file

    for i in range(0, range_end):
        for key, value in d["content-file"][i].items():
            n_con = d["content-file"][i][key]["content"]
            meals_only.append(n_con)
    meals_only = [value for value in meals_only if value != "-"]
    # removes the placeholder "-", as mentioned under "user commands"
    # https://www.delftstack.com/howto/python/python-list-remove-all/
    for i in range(0, key_amount):
        meals_only = [value for value in meals_only if value != ignore_keys[i]]
    # removes all the keys, which should be ignored, from the settings-file.
    max_meals = len([d][0]["content-file"])
    div_meals = len(Counter(meals_only).keys())
    meals_only_without_duplicates = [*set(meals_only)]
    # It first removes the duplicates by creating a set and returns a dictionary which has to be converted to list
    # From www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/

    if len(d["content-file"]) >= 7:
        most_meal, most_meal_amount = Counter(meals_only).most_common(1)[0]
        # Counter inspired by https://datagy.io/python-count-unique-values-list/
        # most_common()-How-To from https://www.delftstack.com/howto/python/python-counter-most-common/
        # delivers a tuple inside a dict
    else:
        most_meal = "nichts"
        most_meal_amount = "0"

    data_set["max_meals"] = max_meals
    data_set["div_meals"] = div_meals
    data_set["most_meal"] = most_meal
    data_set["most_meal_amount"] = most_meal_amount
    data_set["meals_only"] = meals_only
    data_set["meals_only_without_duplicates"] = meals_only_without_duplicates
    data_set["d"] = d

    return data_set


def save_info(week_key, planned_date_key, content):
    # Checks whether something is stored in the "content" variable.
    # If its emtpy nothing happens, and the user is redirected.
    # If the value is "r" a random meal from "meals_only_without_duplicates" gets generated
    # and used as a value for "content".
    # If the value is "f" the "get_lost_meals" function gets called and
    # the first value of "forgotten_meals" used as a value for "content".
    print(content,week_key,planned_date_key)
    if content == "":
        return redirect("/")
    if content == "r":
        data_set = get_data()
        meals_only_without_duplicates = data_set["meals_only_without_duplicates"]
        try:
            rng_content = sample(Counter(meals_only_without_duplicates).keys(), 1)
            content = rng_content[0]
        except:
            print("Dataset is too small, missing or corrupted.")
    if content == "f":
        forgotten_meals = get_lost_meals()
        try:
            content = forgotten_meals[0]
        except:
            print("Dataset is too small, missing or corrupted.")
    if content is not None:
        date = planned_date_key
        temp_dic = {}
        temp_dic[date] = {}
        temp_dic[date]["content"] = content
        temp_dic[date]["weekday"] = week_key
        date_updated = 0

        with open("json_files/content.json", "r+") as f:
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

        if date_updated == 0:
            with open("json_files/content.json", "r+") as f:
                file_data["content-file"].append(temp_dic)
                f.seek(0)
                json.dump(file_data, f, indent=4)


# Get Values to display the meals which haven't been prepared in the last 30 days.
# Works only if there are more than 45 meals planned in the "content.json"-file
########################################################################################################################
def get_lost_meals():
    forgotten_meals = []  # Contains all the meals, which haven't been prepared in a while
    data_set = get_data()
    meals_only = data_set["meals_only"]
    d = data_set["d"]

    forgotten_meals.clear()  # Clears the list and creates a new one. In case some forgotten meals have been planned.
    week_end = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(
        days=6)  # Last day of week.
    past = week_end - timedelta(days=37)
    recently = []  # Contains all meals which have been prepared in the last 37 days.
    not_used = []  # Contains al meals which have not been used in the last 37 days.
    past_meals_only = []  # Contains al meals as strings which are in the past. Without duplicates.

    max_len = len([d][0]["content-file"])  # Determines the length of "d" and used for the "range"-function.

    if max_len >= 45:
        # Gets all meals.
        # If the date is in the past, appends it to the "past_meals_only" list.
        # If the date is between the past and the current weeks last day, appends it to the "recently" list.
        for i in range(0, max_len):
            for date, meal in d["content-file"][i].items():
                n_con = d["content-file"][i][date]["content"]
                date_checked = datetime.strptime(date, "%d.%m.%Y")
                if date_checked <= week_end:
                    past_meals_only.append(n_con)
                if past <= date_checked <= week_end:
                    recently.append(n_con)

        # Removes duplicates from the "past_meals_only" list.
        past_meals_only = [*set(past_meals_only)]

        # Loads data from setting.json and removes the values which should be ignored.
        with open('json_files/settings.json', "r") as s:
            settings = json.load(s)
        ignore_keys = [settings][0]["settings"]["ignore"]
        key_amount = len([settings][0]["settings"]["ignore"])

        for i in range(0, key_amount):
            past_meals_only = [value for value in meals_only if value != ignore_keys[i]]
        # removes all the keys, which should be ignored, from the settings-file.

        # Adds all elements from the past, which are not in the "recently-list", to a new list.
        for element in past_meals_only:
            if element not in recently:
                not_used.append(element)
        # Thanks to www.geeksforgeeks.org/python-difference-two-lists/

        # Takes 7 random values from the not used meals and adds them to a new list, which is used to return
        # the meals to the user.
        try:
            subset = sample(not_used, 7)
            for item in subset:
                forgotten_meals.append(item)
        except:
            print("Error creating a subset with the forgotten meals. Possible cause: 'Amount of items < than 7' "
                  "Fix: Add more different meals.")
    if max_len < 45:
        print("Not enough data available.")

    return forgotten_meals


# Chooses 7 random meals from "content.json" and delivers them to the save-function.
########################################################################################################################
def rng_plan_task(display_week):
    try:
        data_set = get_data()
        meals_only_without_duplicates = data_set["meals_only_without_duplicates"]
        subset = sample(meals_only_without_duplicates, 7)
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
