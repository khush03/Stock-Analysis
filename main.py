from datetime import datetime
import csv
import math
import difflib

start_date = ""
end_date = ""
date_range = []
final_stock_list = []
current_stock = {}
stock_name_list = []

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
        start_date_input = input("From which date you want to start? (eg. 20-jan-2019):-")
        try:
            start_date = datetime.strptime(start_date_input, "%d-%b-%Y")
            break
        except:
            print("Invalid date format, please provide required date format & valid date.")
    while True:
        global end_date
        end_date_input = input("Till which date you want to analyze? (eg. 20-jan-2019):-")
        try:
            end_date = datetime.strptime(end_date_input, "%d-%b-%Y")
            break
        except:
            print("Invalid date format, please provide required date format & valid date.")
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
    stock_name_list.append(stock_data[0].lower())
    final_stock_list.append(new_stock)

def is_stock_present(stock_name):
    for element in final_stock_list:
        if element['stock_name'].lower() == stock_name.lower():
            return element
    return False

def string_check(stock_name):
    stock_matches = difflib.get_close_matches(stock_name, stock_name_list)
    if stock_matches:
        for stock in final_stock_list:
            if stock['stock_name'].lower() == stock_matches[0].lower():
                return stock
    return False

def get_price_list_for_date_range():
    temp_list = []
    for stat in current_stock["stock_stats"]:
        curr_date = datetime.strptime(stat['date'], "%d-%b-%Y")
        if start_date <= curr_date <= end_date:
            temp_list.append(stat)
    return temp_list
# ------------------------------------- [END] STOCK METHODS -----------------------------

# ------------------------------------- [START] STATS CALCULATION -----------------------
def mean_calculate(item_list):
    len_items = len(item_list)
    if len_items==0:
        return 0
    sum = 0
    for item in item_list:
        sum = sum + item['value']
    mean = sum/len_items
    return mean

def standard_deviation_calculation(item_list):
    if len(item_list)==0:
        return 0
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
    final_min_index = final_max_index = min_price_index = max_price_index = 0
    max_diff = 0
    price_obj_list = get_price_list_for_date_range()
    len_arr = len(price_obj_list)
    if not len_arr:
        return [None, None, 0]
    for index in range(1, len_arr):
        if price_obj_list[index]['value'] < price_obj_list[min_price_index]['value']:
            min_price_index = max_price_index = index
        elif price_obj_list[index]['value'] > price_obj_list[max_price_index]['value']:
            max_price_index = index
        if (price_obj_list[max_price_index]['value'] - price_obj_list[min_price_index]['value']) > max_diff:
            final_min_index = min_price_index
            final_max_index = max_price_index
            max_diff = price_obj_list[max_price_index]['value'] - price_obj_list[min_price_index]['value']
    buy_date = price_obj_list[final_min_index]['date']
    sell_date = price_obj_list[final_max_index]['date']
    profit = max_diff * 100
    return [buy_date, sell_date, profit]
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
                    while True:
                        user_approval = input("Oops! Do you mean '" + stock_info['stock_name'] + "':? (Y/N)")

                        if user_approval.lower() not in ["y", "n"]:
                            print("Inavlid input. Please enter Y/N")
                        elif user_approval == 'Y' or user_approval == 'y':
                            len_stock_stat = len(current_stock['stock_stats'])
                            if len_stock_stat == 1 and current_stock['stock_stats'][0]['value'] == 0:
                                print("Insufficient data for '" + current_stock['stock_name'] + "' ,stock value not provided!!")
                                break
                            else:
                                proceed_for_stock()
                                break
                        else:
                            break
            else:
                current_stock = stock_info
                len_stock_stat = len(current_stock['stock_stats'])
                if len_stock_stat == 1 and current_stock['stock_stats'][0]['value'] == 0:
                    print("Insufficient data for '" + current_stock['stock_name'] + "' ,stock value not provided!!")
                else:
                    proceed_for_stock()
        except Exception as e:
            print("Something went wrong, please try again!!", str(e))
        no_flag = False
        while True:
            exit_input = input("Do you want to continue? (Y/N) :")
            if exit_input.lower() not in ['y','n']:
                print("Invalid input. Please enter Y/N")
            elif exit_input.lower()=="y":
                break
            else:
                no_flag = True
                break
        if no_flag:
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