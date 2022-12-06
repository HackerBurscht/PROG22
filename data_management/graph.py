# Python libraries
####################################################################################################################
# numbers and time
from collections import Counter
# python files
from data_management.data_handler import get_data


# Creates the necessary values, which are used to display the horizontal bar chart on the stats-page.
########################################################################################################################
def graph_data():
    data_set = get_data()
    meals_only = data_set["meals_only"]

    # Creates three empty lists, which are used to temporarily save values from "d".
    data_x = []
    data_y = []
    result_complete = []

    # Counts all the different meals in "meals_only" and appends the content to "data_x" and the amount to "data_y"
    for meal, amount in Counter(meals_only).most_common():
        data_x.append(meal)
        data_y.append(amount)

    # Get the min and max amount value by accessing the first and last value in "data_y"
    max = data_y[0]
    min = data_y[-1]

    # Saves the "meal", the "amount" and the standardised value as a list inside the list.
    for meal, amount in Counter(meals_only).most_common():
        result = []
        norm = round((amount - min) / (max - min), 2)  # Transforms the amount to a standardised value between 0 and 1.
        result.append(meal)
        result.append(norm)
        result.append(amount)
        result_complete.append(result)

    # Turn the complete list in two. The first one contains only the first 15 entries and the second the rest.
    not15 = result_complete[16:len(result_complete)]
    top15 = result_complete[0:15]

    return top15, not15
