import csv
from datetime import date, timedelta
import re
import math


start_date = []
end_date = []
final_stock_list = []
current_stock = {}

month_days = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
month_names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
date_coversion = {'jan': 1,'feb': 2,'mar': 3,'apr': 4,'may': 5,'jun': 6,'jul': 7,'aug': 8,'sep': 9,'oct': 10,'nov':11,'dec':12 }

# ------------------------------------- [START] CSV METHODS -----------------------------
def read_data():
    with open('stock_picker.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        next(reader, None)
        for row in reader:
            update_stock_list(row)
# ------------------------------------- [END] CSV METHODS -------------------------------

# ------------------------------------- [START] DATE METHODS ----------------------------
def get_dates():
    while True:
        global start_date
        start_date_input = input("From which date you want to start? (eg. 20-jan-19):-")
        if is_date_valid(start_date_input):
            start_date = date_conversion_in_required_format(start_date_input)
            break
        else:
            print("Invalid date format, please provide required date format & valid date.")
    while True:
        global end_date
        end_date_input = input("Till which date you want to analyze? (eg. 20-jan-19):-")
        if is_date_valid(end_date_input):
            end_date = date_conversion_in_required_format(end_date_input)
            break
        else:
            print("Invalid date format, please provide required date format & valid date.")

def is_date_valid(date):
    if not date:
        return False
    else:
        date_values = date.split("-")
        if len(date_values) != 3:
            return False
        if not date_values[0] in month_days:
            return False
        if not date_values[1].lower() in month_names:
            return False
        return True

def date_conversion_in_required_format(date_given):
    month = re.findall('[a-zA-Z]+', date_given, re.IGNORECASE)
    month_val = "".join(month).lower()
    date_given = date_given.lower().replace(month_val, str(date_coversion[month_val]))
    date_given = list(map(int, date_given.split("-")))
    return date_given

def is_date_in_range(date):
    parsed_date = date_conversion_in_required_format(date)
    parsed_date_timestamp = get_parsed_date_timestamp(parsed_date)
    start_date_timestamp = get_parsed_date_timestamp(start_date)
    end_date_timestamp = get_parsed_date_timestamp(end_date)
    print('dates parsed ', parsed_date_timestamp, ' start ', start_date_timestamp, ' end ', end_date_timestamp)
    if start_date_timestamp <= parsed_date_timestamp <= end_date_timestamp:
        return True
    return False

def get_parsed_date_timestamp(date_list):
    result = str(date_list[2])
    if date_list[1] < 10:
        result = result + '0' + str(date_list[1])
    else:
        result = result + str(date_list[1])
    if date_list[0] < 10:
        result = result + '0' + str(date_list[0])
    else:
        result = result + str(date_list[0])
    return int(result)
# ------------------------------------- [END] DATE METHODS ------------------------------

# ------------------------------------- [START] STOCK METHODS ---------------------------
def update_stock_list(stock_data):
    if len(final_stock_list) > 0:
        for item in final_stock_list:
            if item["stock_name"] == stock_data[0]:
                item["stock_stats"].append({
                    "date": stock_data[1],
                    "value": float(stock_data[2])
                })
                stats_len = len(item["stock_stats"])
                if not stock_data[2] and stats_len > 1:
                    item["stock_stats"][stats_len-1]['value'] = item["stock_stats"][stats_len-2]['value']
                elif not item["stock_stats"][0]['value'] and stats_len == 2:
                    item["stock_stats"][0]['value'] = item["stock_stats"][1]['value']
                return
    new_stock = {
        "stock_name": stock_data[0],
        "stock_stats": [
            {
                "date": stock_data[1],
                "value": float(stock_data[2]) if stock_data[2] else 0
            }
        ]
    }
    final_stock_list.append(new_stock)

def is_stock_present(stock_name):
    for element in final_stock_list:
        if element['stock_name'].lower() == stock_name.lower():
            return element
    return False

def string_check(stock_name):
    for stock in final_stock_list:
        if (stock['stock_name'].lower().find(stock_name.lower()) != -1):
            return stock
    return False

def get_price_list_for_date_range():
    temp_list = []
    for stat in current_stock["stock_stats"]:
        if is_date_in_range(stat['date']):
            temp_list.append(stat)
    return temp_list
# ------------------------------------- [END] STOCK METHODS -----------------------------

# ------------------------------------- [START] STATS CALCULATION -----------------------
def mean_calculate(item_list):
    len_items = len(item_list)
    sum = 0
    for item in item_list:
        sum = sum + item['value']
    mean = sum/len_items
    return mean

def standard_deviation_calculation(item_list):
    sum_squares = 0
    squared_values_to_find_mean = []
    mean_val = mean_calculate(item_list)
    for item in item_list:
        diff = item['value'] - mean_val
        squared_values_to_find_mean.append(diff * diff)
    len_list = len(squared_values_to_find_mean)
    for val in squared_values_to_find_mean:
        sum_squares = sum_squares + val
    mean_for_standard_deviation = sum_squares/len_list
    standard_deviation_val = math.sqrt(mean_for_standard_deviation)
    return standard_deviation_val

def get_stock_dates_with_profit():
    profit = 0
    buy_date = ''
    sell_date = ''
    price_obj_list = get_price_list_for_date_range()
    list_len = len(price_obj_list)
    for i in range(list_len):
        for j in range(i, list_len):
            if (price_obj_list[j]['value'] - price_obj_list[i]['value']) > profit:
                buy_date = price_obj_list[i]['date']
                sell_date = price_obj_list[j]['date']
                profit = price_obj_list[j]['value'] - price_obj_list[i]['value']
    return [buy_date if buy_date else None, sell_date if sell_date else None, profit if profit else 0]
# ------------------------------------- [END] STATS CALCULATION -------------------------

# ------------------------------------- [START] OTHER -----------------------------------
def get_input():
    while True:
        try:
            stock_name = input("Welcome Agent! Which stock you need to process?:-")
            stock_info = is_stock_present(stock_name)
            global current_stock
            if not stock_info:
                stock_info = string_check(stock_name)
                if not stock_info:
                    print("We couldnt find any stock with this name, please try again!!")
                else:
                    current_stock = stock_info
                    user_approval = input("Oops! Do you mean '" + stock_info['stock_name'] + "':? (Y/N)")
                    if user_approval == 'Y' or user_approval == 'y':
                        len_stock_stat = len(current_stock['stock_stats'])
                        if len_stock_stat == 1 and current_stock['stock_stats'][0]['value'] == 0:
                            print("Insufficient data for '" + current_stock['stock_name'] + "' ,stock value not provided!!")
                        else:
                            proceed_for_stock()
            else:
                current_stock = stock_info
                len_stock_stat = len(current_stock['stock_stats'])
                if len_stock_stat == 1 and current_stock['stock_stats'][0]['value'] == 0:
                    print("Insufficient data for '" + current_stock['stock_name'] + "' ,stock value not provided!!")
                else:
                    proceed_for_stock()
        except Exception as e:
            print("Something went wrong, please try again!!", str(e))

        exit_input = input("Do you want to continue? (Y/N) :")
        if exit_input != 'Y' and exit_input != 'y':
            break

def proceed_for_stock():
    get_dates()
    price_list = get_price_list_for_date_range()
    stock_predicted_data = get_stock_dates_with_profit()
    print("Here is your result :- ")
    print("Mean : ", mean_calculate(price_list), "\nStd. : ", standard_deviation_calculation(price_list), "\nBuy Date : ", stock_predicted_data[0], "\nSell Date : ", stock_predicted_data[1], "\nProfit : Rs.", stock_predicted_data[2])
# ------------------------------------- [END] OTHER -------------------------------------

read_data()
get_input()
