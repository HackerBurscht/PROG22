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