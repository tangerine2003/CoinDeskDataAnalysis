import pandas as pd
import json
import requests
from pandas.io.json import json_normalize
import datetime
import time
import os

current_price_url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'

error_counter = 0

def api_connect(url):
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        error_handler(today, response.status_code, "No Description")
        return 1

def create_file(date):
    e_file = open(date + ".txt", "w+")
    e_file.write(date + "," + message + "," + description)
    e_file.close()


def model_data(data):
    result = json_normalize(data)
    col_to_drop = ['disclaimer', 'bpi.USD.description', 'bpi.USD.rate', 'time.updatedISO', 'time.updateduk']
    data = result.drop(col_to_drop, 1)
    data.columns = ['Type', 'USD_Rate', 'Updated_Date_Time']
    return data

def error_handler(date, message, description, count):
    if os.path.isfile('/Error_Log.txt'):
        e_file = open("Error_Log.txt", "a+")
        e_file.write(date + "," + message + "," + description)
        e_file.close()
    else:
        e_file = open("Error_Log.txt", "w+")
        e_file.write(date + "," + message + "," + description)
        e_file.close()

    count += 1

    return count


######################################################################
# Start of Main
######################################################################

today = datetime.datetime.now().strftime("%Y-%m-%d")

while error_counter < 10:

    try:
        if today == datetime.datetime.now().strftime("%Y-%m-%d"):
            if os.path.isfile('./' + today + '.txt'):
                curr_data = api_connect(current_price_url)
            else:
                create_file(today)
                curr_data = api_connect(current_price_url)
                #checked_today = True
        else:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            create_file(today)
            curr_data = api_connect(current_price_url)
    except:
        error_counter += error_counter(today, "outfile_unreachable", "to reach the output file", error_counter)

    if type(curr_data) != 'int':
        curr_data = model_data(curr_data)
        curr_data.to_csv(today + '.txt', header=None, index=None, sep=',', mode='a')
    else:
        error_counter = curr_data + error_counter

    time.sleep(60)

