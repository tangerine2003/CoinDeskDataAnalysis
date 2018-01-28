import pandas as pd
import json
import requests
from pandas.io.json import json_normalize
import datetime
import matplotlib.pyplot as plt

historical_url ='https://api.coindesk.com/v1/bpi/historical/close.json?start=2017-01-01&end=2017-12-31'
#yesterday_url = Request('https://api.coindesk.com/v1/bpi/historical/close.json?for=yesterday')
#current_price_url = Request('https://api.coindesk.com/v1/bpi/currentprice/USD.json')

def api_connect(url):
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return "error"

def model_hist_data(data: object) -> object:
    result = json_normalize(data)
    col_to_drop = ['disclaimer', 'time.updated', 'time.updatedISO']
    data = result.drop(col_to_drop, 1)
    data = pd.melt(data, var_name="Date", value_name="Price")
    data['Date'] = data['Date'].map(lambda x: x.lstrip('bpi.'))
    return data



######################################################################
# Start of Main
######################################################################


data = api_connect(historical_url)

data = model_hist_data(data)


plt.figure();

print(data)



#df = pd.read_json(result)


#print(data)

#api_connect(yesterday_url)
#api_connect(current_price_url)
