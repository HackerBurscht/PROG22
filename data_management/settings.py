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


# Checks if the json files are present.
# Adapted from https://stackoverflow.com/questions/32991069/python-checking-for-json-files-and-creating-one-if-needed
########################################################################################################################
def json_check_task():
    files = {  # Is used to check if the files are existing.
        "0": "content.json",
        "1": "settings.json"
    }
    for i in range(0, len(files)):
        json_names = files.get(str(i))
        if os.access("json_files/", os.R_OK):
            print(json_names, "exists and is readable")
        else:
            print(json_names, "is missing or is not readable")
            with open(json_names, 'w') as file:
                file.write(json.dumps({}))
            if json_names == "settings.json":
                with open("json_files/settings.json", "r+") as s:
                    x = {"settings": {"ignore": []}, "replace": []}
                    s.truncate(0)
                    json.dump(x, s)
            if json_names == "content.json":
                with open("json_files/content.json", "r+") as f:
                    y = {"content-file": []}
                    f.truncate(0)
                    json.dump(y, f)
            print(json_names, "has been created")


# Resets content.json and settings.json
########################################################################################################################
def clear_all():
    with open("json_files/settings.json", "r+") as s:
        x = {"settings": {"ignore": []}, "replace": []}
        s.truncate(0)
        json.dump(x, s)

    with open("json_files/content.json", "r+") as f:
        y = {"content-file": []}
        print(y)
        f.truncate(0)
        json.dump(y, f)


# Saves values which should be ignored from the settings page into the settings.json file
########################################################################################################################
def save_ignore_task():
    ignore_value = request.form.get("ignore")
    with open("json_files/settings.json", "r+") as s:
        settings = json.load(s)
        [settings][0]["settings"]["ignore"].append(ignore_value)
        s.seek(0)
        json.dump(settings, s, indent=4)


# Saves values which should be replaced in the settings.json
########################################################################################################################
def change_key_task():
    # Get input from the user by accessing the value inside the form
    key_to_change = request.form.get("change1")
    # Opens the settings file and adds the value to the file
    with open("json_files/settings.json", "r+") as s:
        settings = json.load(s)
        try:
            [settings][0]["replace"].pop(0)
        except:
            pass
        [settings][0]["replace"].append(key_to_change)
        s.seek(0)
        json.dump(settings, s, indent=4)

    return key_to_change


# Gets the value which should replace the value from change_key() and changes this value in the "content.json" file.
########################################################################################################################
def change_key_to_task():
    # Get input from the user by accessing the value inside the form
    key_to_change_to = request.form.get("change2")

    # Loads the settings file and gets the value which should be changed.
    with open("json_files/settings.json", "r+") as s:
        settings = json.load(s)
        old_value = [settings][0]["replace"]
    old_value = str(old_value).strip("[]'")

    # Loads the content file and replaced all the matching values inside.
    with open("json_files/content.json", "r+") as f:
        d = json.load(f)
        end = len([d][0]["content-file"])
        for j in range(0, end):
            for key, value in d["content-file"][j].items():
                if old_value == str(d["content-file"][j][key]["content"]):
                    d["content-file"][j][key]["content"] = key_to_change_to
        f.seek(0)
        json.dump(d, f, indent=4)
        f.truncate()

    # Loads the settings file again and deletes the value which has been replaced.
    with open("json_files/settings.json", "r+") as s:
        settings = json.load(s)
        try:
            [settings][0]["replace"].pop(0)
            s.truncate(0)
            s.seek(0)
            json.dump(settings, s, indent=4)
        except:
            pass

    # Changes the placeholder back to normal
    key_to_change = "Chips"
    key_to_change_to = "Pommes"

    return key_to_change, key_to_change_to
