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
    with open('settings.json', "r") as s:
        settings = json.load(s)
    ignore_keys = [settings][0]["settings"]["ignore"]
    key_amount = len([settings][0]["settings"]["ignore"])

    # Get the data from the content.json
    ####################################################################################################################
    with open('content.json', "r") as f:
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
