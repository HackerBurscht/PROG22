# Python libraries
####################################################################################################################
# numbers and time
from datetime import datetime, timedelta

# python files
from py_files.data_handler import get_data


def user_data_index(display_week):
    ''' Loads data from content.json and calculates necessary values.
        Gets data by calling get_data().
        Calculates the desired week with the "display_week" parameter.
        Checks if each date in the current week has a corresponding value stored in content.json.
        If not, a placeholder value is assigned.

        parameters:
        display_week: Contains the value of the selected week. Used to decide which data is returned.

        return:
        display_data (Dict containing multiple values)
    '''
    display_data = {}
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

    display_data["week_start_display"] = week_start_display
    display_data["week_end_display"] = week_end_display
    display_data["return_mo"] = clean_lst[0]
    display_data["return_di"] = clean_lst[1]
    display_data["return_mi"] = clean_lst[2]
    display_data["return_do"] = clean_lst[3]
    display_data["return_fr"] = clean_lst[4]
    display_data["return_sa"] = clean_lst[5]
    display_data["return_so"] = clean_lst[6]
    display_data["max_meals"] = max_meals
    display_data["div_meals"] = div_meals
    display_data["most_meal"] = most_meal
    display_data["most_meal_amount"] = most_meal_amount
    display_data["visible"] = visible

    return display_data

