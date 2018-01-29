import pandas as pd
import json
import requests
from pandas.io.json import json_normalize
import datetime
import matplotlib.pyplot as plt

#historical_url ='https://api.coindesk.com/v1/bpi/historical/close.json?start=2017-01-01&end=2017-12-31'
#yesterday_url = 'https://api.coindesk.com/v1/bpi/historical/close.json?for=yesterday'
historical_url ='https://api.coindesk.com/v1/bpi/historical/close.json?start=2017-01-01&end='

now = datetime.datetime.now()

def api_connect(url):
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return "error"

def model_hist_data(data):
    result = json_normalize(data)
    col_to_drop = ['disclaimer', 'time.updated', 'time.updatedISO']
    data = result.drop(col_to_drop, 1)
    data = pd.melt(data, var_name="Date", value_name="Price")
    data['Date'] = data['Date'].map(lambda x: x.lstrip('bpi.'))
    data['Date'] = pd.to_datetime(data['Date'])
    return data


######################################################################
# Start of Main
######################################################################

today = now.strftime("%Y-%m-%d")

hist_data = api_connect(historical_url + today)
hist_data = model_hist_data(hist_data)
hist_data.plot(x='Date', y='Price')
plt.show()
