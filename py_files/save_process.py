# Python libraries
####################################################################################################################
import json

# numbers and time
from datetime import datetime, timedelta
from collections import Counter
from random import sample

# python files
from py_files.data_handler import get_data, get_lost_meals


def save_info(planned_date_key, content):
    ''' Takes two parameters planned_date_key and content and stores those in content.json
        Checks if content is empty. If yes: Returns.
        Checks if content is "r". If yes, takes a random value from content.json.
        Checks if content is "f". If yes, takes a value from get_lost_meals()
        Stores the input data and the possible generated data in content.json.

        parameters:
        planned_date_key: Contains the date, with the content value should be saved.
        content: The value of the content, which should be stored.

        return:
        Returns to the last task.
    '''
    if content == "":
        return
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


def rng_plan_task(display_week):
    ''' Takes display_week and takes seven random values from content.json.
        Gets data by calling get_data().
        Takes 7 random values from meals_only_without_duplicates.
        Saves those values by calling save_info()

        parameters:
        display_week: Contains the value of the current week.

        return:
        Returns to the last task.
    '''
    try:
        data_set = get_data()
        meals_only_without_duplicates = data_set["meals_only_without_duplicates"]
        subset = sample(meals_only_without_duplicates, 7)
        # How-Two from machinelearningmastery.com/how-to-generate-random-numbers-in-python/
        for i in range(0, 7):
            content = subset[i]
            planned_date_key = datetime.today() - timedelta(days=datetime.today().weekday() % 7) + timedelta(days=i)
            planned_date_key = planned_date_key + timedelta(days=display_week * 7)
            planned_date_key = planned_date_key.strftime("%d.%m.%Y")
            save_info(planned_date_key, content)
    except:
        print("Dataset is too small, missing or corrupted.")