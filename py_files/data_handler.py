# Python libraries
####################################################################################################################
# general
import json

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


def get_data():
    ''' Loads data from content.json and calculates assigns this data to multiple variables. Which in return can
        easily be used in other functions.
        First creates an empty dictionary.
        Afterwards reads values from settings.json and gets data from content.json.
        Calculates all the different meals, ignores duplicates,  the amount of all meals,
        the amount of all different meals, and the most occurring meal type including the amount

        parameters:

        return:
        data_set(Dict containing multiple values)
    '''
    data_set = {
        "max_meals": "",
        "div_meals": "",
        "most_meal": "",
        "most_meal_amount": "",
        "meals_only": "",
        "meals_only_without_duplicates": "",
        "d": "",
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

    # Create variable with only the different meals and without duplicates.
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


def get_lost_meals():
    ''' Calculates all the meals which haven't been prepared in the last 30 days. Works only if
        there are more than 45 meals planned in the "content.json"-file
        Firstly gets data, by calling get_data().
        Checks if there are more than 45 entries in content.json by checking the length of "d".
        Saves all meals which are in the past in a list.
        Saves all meals which have recently been prepared in a list.
        Removes the recent meals from the past meals.
        Takes seven random entries from hte past meals and saves those in "forgotten_meals"

        parameters:

        return:
        forgotten_meals (List containing multiple values)
    '''
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
        forgotten_meals.append("empty")

    return forgotten_meals


# Creates the necessary values, which are used to display the day-statistics on the stas-page.
def max_combo_weekly():
    ''' Creates all the necessary values, which are needed to display the day/meal combinations on stats.html.
        Firstly gets data, by calling get_data().
        Gets alls meals by "meals_only" and assigns each date the corresponding weekday.
        Saves those values in a new list (clean_data).
        Calculates the appearing combinations and their frequency.
        (For more information check the readme or google "affinity analysis")

        parameters:

        return:
        max_lst (List containing multiple values)
    '''
    max_lst = []
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
                dt_date_key = datetime.strptime(key, "%d.%M.%Y").date()
                dt_weekday = dt_date_key.weekday()
                n_day = weekday.get(str(dt_weekday))
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

    return max_lst
